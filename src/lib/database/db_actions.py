from datetime import datetime as dt
from datetime import timezone as tz

from src.lib import EMAIL_CONST, DB_CONST
from src.lib.database.db_conn import DB_Connection


class DB_Actions:
    conn = DB_Connection()

    # ---------- login ----------

    def _get_pass(self, user_id):
        """
        gets password for user
        """
        query = "SELECT user_pass FROM public.user_data WHERE user_id = %s"
        password = self.conn._get(query=query, args=(user_id,))
        try:
            return password[0][0]
        except Exception:
            return None

    def _add_new_user(self, user_id, password):
        """
        add a new credential to the db
        """
        query = """
            INSERT INTO public.user_data (user_id, user_pass, priv_cats)
            VALUES (%s, %s, %s)
        """  # TODO: hashing?
        return self.conn._set(query, (user_id, password, "{}",))

    # ---------- get helpers ----------

    def _gather_data_by_user(self, user_id):
        """
        Gather all emails by user_id.
        """
        query = "SELECT * FROM public.email_data WHERE user_id = %s"
        data = self.conn._get(query, (user_id,))
        return [list(t) for t in data]

    def _gather_data_by_sender(self, user_id, sender_id):
        """
        Gather all emails by sender for a user.
        """
        query = """
            SELECT * FROM public.email_data
            WHERE user_id = %s AND sender_id = %s
        """
        data = self.conn._get(query, (user_id, sender_id,))
        return [list(t) for t in data]

    def _gather_data_by_category(self, category, limit, offset):
        """
        Gather all emails by category, newest first.
        """
        query = """
            SELECT * FROM public.email_data
            WHERE category = %s
            ORDER BY collected_date DESC
            LIMIT %s OFFSET %s
        """
        data = self.conn._get(query, (category, limit, offset,))
        return [list(t) for t in data]

    def _gather_categories(self, credentials):
        """
        Get category JSON for a user.

        :param credentials: (username, password)
        """
        query = """
            SELECT priv_cats FROM public.user_data
            WHERE user_id = %s AND user_pass = %s
        """  # TODO: hashing?
        data = self.conn._get(query, credentials)
        if not data:
            print("STATUS: empty category")
            print(data)
            return []
        try:
            categories = data[0][0]
        except Exception:
            print("ERROR: category failed to be retrieved")
            categories = None
        return categories

    def _gather_user_key(self, credentials) -> str:
        query = """
            SELECT user_key FROM public.user_data
            WHERE user_id = %s AND user_pass = %s
        """  # TODO: hashing?
        data = self.conn._get(query, credentials)
        return data[0][0]

    def _gather_email(self, uid, eid):
        """
        Get a single email row.

        :param uid: user id (email)
        :param eid: email id
        """
        query = """
            SELECT id, sender_add, category, data, collected_date, delete_date
            FROM public.email_data
            WHERE user_id = %s AND id = %s
            LIMIT 1;
        """
        row = self.conn._get(query, (uid, eid,))

        if not row or not row[0]:
            return None
        return row[0]

    def _gather_email_by_page(self, uid, category, limit, offset):
        """
        Paged email fetch, newest first.

        :param uid: username
        :param category: category string or None / "all"
        :param limit: rows per page
        :param offset: offset
        """
        base = """
            SELECT id, sender_add, category, data, collected_date, delete_date
            FROM public.email_data
            WHERE user_id = %s
        """
        args = [uid]

        if category and category != "all":
            base += " AND category = %s"
            args.append(category)

        base += " ORDER BY collected_date DESC LIMIT %s OFFSET %s"
        args.extend([limit, offset])

        rows = self.conn._get(base, tuple(args))
        return rows

    def _get_cat_by_sender(self, sender):
        query = """
            SELECT category
            FROM public.email_data
            WHERE sender_id = %s
            LIMIT 1;
        """
        rows = self.conn._get(query, (sender,))
        return rows[0][0] if rows else None

    # ---------- set helpers ----------

    def _add_email_data(self, data):
        """
        Insert one email row.

        data tuple layout:
          (user_id, sender_add_json, category, data_json, delete_date)
        """
        query = """
            INSERT INTO public.email_data
                (user_id, sender_add, category, data, delete_date)
            VALUES (%s, %s::jsonb, %s, %s::jsonb, %s)
        """
        result = self.conn._set(query=query, args=data)
        if result == DB_CONST.DB_ERROR:
            print("Unable to write data")

    def _add_categories(self, credentials, cats):
        """
        Save categories JSON into user_data. Upsert by user_id.

        :param credentials: (username, password)
        """
        query = """
            INSERT INTO public.user_data (user_id, user_pass, priv_cats)
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (user_id)
            DO UPDATE SET priv_cats = EXCLUDED.priv_cats
        """  # TODO: hashing?
        data = self.conn._set(query, credentials + (cats,))
        return data

    def _add_email_key(self, credentials, key):
        """
        Save/Update IMAP key for the user.
        """
        query = """
            INSERT INTO public.user_data (user_id, user_pass, user_key)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET user_key = EXCLUDED.user_key
        """
        data = self.conn._set(query, credentials + (key,))
        return data

    # ---------- actions ----------

    def _delete_old_emails(self):
        now = dt.now(tz.utc)
        query = "DELETE FROM public.email_data WHERE delete_date < %s"
        result = self.conn._set(query, (now,))

        now_local_str = now.astimezone().strftime("%m/%d/%Y")
        print(f"All emails past {now_local_str} have been deleted.")

        if result == DB_CONST.DB_ERROR:
            print("Email delete error")

    def _delete_email(self, uid, eid):
        """
        Delete a single email for a user.
        """
        query = """
            DELETE FROM public.email_data
            WHERE user_id = %s AND id = %s
        """
        return self.conn._set(query, (uid, eid,))

    def _categorize(self, user, sender, category):
        query = """
            UPDATE public.email_data
            SET category = %s
            WHERE user_id = %s AND sender_id = %s;
        """
        check = self.conn._set(query, (category, user, sender,))
        print(check)
