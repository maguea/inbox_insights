# src/web_flask/retention.py  (fix the imports)
import os, json, threading, time, re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

from src.lib.account.create_accounts import _check_env, _login
from src.lib.email_scraper.email_consts import EMAIL_CONST
from src.lib.email_scraper.email_scraper import Gather
from src.lib.account.categories import load_categories


CACHE_PATH = Path("cached_emails.json")

# ---------- helpers ----------

def _extract_email(addr_field: str) -> str:
    """
    Extract pure email from strings like:
      'Name <user@corp.com>' -> 'user@corp.com'
      'user@corp.com'        -> 'user@corp.com'
    """
    if not addr_field:
        return ""
    addr_field = addr_field.strip()
    m = re.search(r"<([^>]+)>", addr_field)
    if m:
        return m.group(1).strip().lower()
    return addr_field.strip().lower()

def _email_domain(addr_field: str) -> str:
    email = _extract_email(addr_field)
    if "@" in email:
        return email.split("@", 1)[1]
    return ""

def _matches_category(email_obj: dict, cat: dict) -> bool:
    """
    Match by exact sender email OR by domain membership.
    email_obj['sender'] is like 'Name <user@corp.com>' or 'user@corp.com'.
    cat has keys: name, emails, domains, shared, days_until_delete
    """
    sender = email_obj.get("sender") or ""
    sender_email = _extract_email(sender)
    sender_domain = _email_domain(sender)

    emails = [e.strip().lower() for e in cat.get("emails", []) if e]
    domains = [d.strip().lower() for d in cat.get("domains", []) if d]

    if sender_email and sender_email in emails:
        return True
    if sender_domain and sender_domain in domains:
        return True
    return False

def _parse_cached_date(date_str: str) -> datetime | None:
    """
    Cached emails store 'date' like 'Oct 1, 2025' per Gather._get_date_info()
    We parse it into a UTC datetime with no time component.
    """
    if not date_str:
        return None
    try:
        # Support non-zero-padded day values
        parts = date_str.replace(",", "").split()
        if len(parts) == 3 and parts[1].isdigit() and len(parts[1]) == 1:
            date_str = f"{parts[0]} {int(parts[1]):02d}, {parts[2]}"
        return datetime.strptime(date_str, "%b %d, %Y").replace(tzinfo=timezone.utc)
    except Exception:
        return None

def _email_age_days(email_obj: dict) -> int:
    dt = _parse_cached_date(email_obj.get("date"))
    if not dt:
        return 10**6  # Treat unknown as very old so it's eligible if a category requires deletion
    return (datetime.now(timezone.utc) - dt).days

# ---------- local cache purge ----------

def purge_local_cache_by_categories() -> tuple[int, int]:
    """
    Remove items from cached_emails.json that exceed their category's days_until_delete.
    Returns (removed_count, kept_count).
    """
    if not CACHE_PATH.exists():
        return 0, 0

    categories = load_categories()  # pulls from .env (CATEGORIES)
    with CACHE_PATH.open("r", encoding="utf-8") as f:
        items = json.load(f)

    keep, removed = [], []
    for em in items:
        remove_flag = False
        for cat in categories:
            days = int(cat.get("days_until_delete", 0) or 0)
            if days <= 0:
                continue
            if _matches_category(em, cat) and _email_age_days(em) >= days:
                remove_flag = True
                break
        (removed if remove_flag else keep).append(em)

    if len(keep) != len(items):
        with CACHE_PATH.open("w", encoding="utf-8") as f:
            json.dump(keep, f, indent=2)

    return len(items) - len(keep), len(keep)

# ---------- IMAP purge ----------

def _imap_delete_for_category(cat: dict) -> int:
    """
    Deletes messages on the IMAP server that match the category’s senders/domains
    AND are older than the retention window.

    Because cached emails don't store IMAP UIDs, we do conservative server-side
    searches per sender/domain and mark matching messages as \\Deleted, then EXPUNGE.
    """
    days = int(cat.get("days_until_delete", 0) or 0)
    if days <= 0:
        return 0

    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%d-%b-%Y")  # e.g., '01-Nov-2025'

    emails = [e.strip().lower() for e in cat.get("emails", []) if e]
    domains = [d.strip().lower() for d in cat.get("domains", []) if d]

    load_dotenv()
    if not _check_env():
        return 0

    user = os.getenv("CLIENT_USER")
    pw = os.getenv("CLIENT_PASS")
    server = os.getenv("CLIENT_SERVER")

    # Verify basic connectivity (EMAIL_CONST codes)
    if _login(user, pw) != EMAIL_CONST.LOGIN_SUCCESS:
        return 0

    g = Gather(user, pw, server)
    g._connect()
    try:
        total_deleted = 0

        def search_and_flag(term: str) -> int:
            # IMAP FROM matches substring in the From header.
            # Compose: (UNDELETED) BEFORE cutoff FROM "term"
            status, data = g.conn.search(None, "(UNDELETED)", "BEFORE", cutoff, "FROM", f'"{term}"')
            if status != "OK" or not data or not data[0]:
                return 0
            ids = data[0].split()
            if not ids:
                return 0
            deleted_here = 0
            for eid in ids:
                try:
                    g.conn.store(eid, "+FLAGS", r"(\Deleted)")
                    deleted_here += 1
                except Exception:
                    pass
            return deleted_here

        # Exact emails
        for em_addr in emails:
            total_deleted += search_and_flag(em_addr)

        # Domains (search by '@domain' for simplicity)
        for dom in domains:
            term = dom if dom.startswith("@") else f"@{dom}"
            total_deleted += search_and_flag(term)

        try:
            g.conn.expunge()
        except Exception:
            pass

        return total_deleted
    finally:
        g._disconnect()

def purge_imap_by_categories() -> int:
    categories = load_categories()
    deleted = 0
    for cat in categories:
        deleted += _imap_delete_for_category(cat)
    return deleted

# ---------- scheduler ----------

def _daily_scheduler_loop(run_imap: bool):
    """
    Run once shortly after startup, then every ~24h.
    """
    # small initial delay so the app can boot
    time.sleep(10)
    while True:
        try:
            removed_local, kept_local = purge_local_cache_by_categories()
            imap_deleted = purge_imap_by_categories() if run_imap else 0
            print(f"[Retention] Local removed={removed_local}, kept={kept_local}; IMAP deleted={imap_deleted}")
        except Exception as e:
            print(f"[Retention] Error: {e}")
        # sleep ~24h
        time.sleep(60 * 60 * 24)

def start_retention_daemon(run_imap: bool = False):
    """
    Call this once from your Flask app startup.
    Set run_imap=True to also delete on the server (dangerous; get user consent).
    """
    t = threading.Thread(target=_daily_scheduler_loop, args=(run_imap,), daemon=True)
    t.start()
