(function () {
  const listEl = document.getElementById('emailList');
  const sentinel = document.getElementById('loadSentinel');
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  const searchInput = document.getElementById('emailSearch');

  const subjectEl = document.getElementById('emailSubject');
  const senderEl = document.getElementById('emailSender');
  const dateEl = document.getElementById('emailDate');
  const timeEl = document.getElementById('emailTime');
  const bodyEl = document.getElementById('emailBody');
  const placeholder = document.getElementById('panePlaceholder');
  const detailPane = document.getElementById('paneDetail');

  let loading = false;
  let exhausted = false;
  let observer = null;
  let activeId = null;
  let filterText = '';

  // --- helpers
  const setBusy = (busy) => {
    listEl.setAttribute('aria-busy', busy ? 'true' : 'false');
    sentinel.style.display = busy ? '' : 'none';
  };

  const nextPage = () => parseInt(listEl.dataset.nextPage || '1', 10);

  const bumpPage = () => {
    const p = nextPage();
    listEl.dataset.nextPage = (p + 1).toString();
  };

  const attachItemHandlers = (root) => {
    root.querySelectorAll('.email-item').forEach(btn => {
      btn.addEventListener('click', async () => {
        const id = btn.getAttribute('data-email-id');
        if (!id) return;
        activeId = id;

        // highlight active
        listEl.querySelectorAll('.email-item.active').forEach(el => el.classList.remove('active'));
        btn.classList.add('active');

        // fetch detail JSON
        try {
          const res = await fetch(`/api/emails/${id}`);
          if (!res.ok) throw new Error(`Failed detail ${res.status}`);
          const email = await res.json();

          // fill pane
          subjectEl.textContent = email.subject || '(no subject)';
          senderEl.textContent = email.sender || '';
          dateEl.textContent = email.date || '';
          timeEl.textContent = email.timestamp || '';
          bodyEl.innerHTML = email.body || `<p class="text-muted">(No body)</p>`;

          placeholder.classList.add('d-none');
          detailPane.classList.remove('d-none');
          detailPane.focus();
        } catch (err) {
          console.error(err);
        }
      });
    });
  };

  const appendItems = (html) => {
    const frag = document.createElement('div');
    frag.innerHTML = html;

    // Move children BEFORE sentinel
    const items = Array.from(frag.children);
    items.forEach(ch => {
      // simple client side filter on newly appended items
      if (filterText) {
        const t = ch.innerText.toLowerCase();
        if (!t.includes(filterText)) return;
      }
      listEl.insertBefore(ch, sentinel);
    });

    attachItemHandlers(listEl);
  };

  const loadPage = async () => {
    if (loading || exhausted) return;
    loading = true;
    setBusy(true);
    try {
      const p = nextPage();
      const res = await fetch(`/history/page/${p}`, { headers: { 'X-Requested-With': 'fetch' } });
      if (res.status === 204) {
        exhausted = true;
        sentinel.innerHTML = '<span class="text-muted">No more emails.</span>';
        setBusy(false);
        loading = false;
        return;
      }
      if (!res.ok) throw new Error(`Failed page ${p}: ${res.status}`);
      const html = await res.text();
      appendItems(html);
      bumpPage();
    } catch (err) {
      console.error(err);
      sentinel.innerHTML = '<span class="text-danger">Failed to load.</span>';
    } finally {
      setBusy(false);
      loading = false;
    }
  };

  // IntersectionObserver for infinite scroll
  const setupObserver = () => {
    if (!('IntersectionObserver' in window)) return;

    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) loadPage();
      });
    }, { root: listEl, threshold: 0.1 });

    observer.observe(sentinel);
  };

  // Fallback button
  loadMoreBtn.addEventListener('click', loadPage);

  // Simple client-side filter of rendered items
  const debounce = (fn, ms) => {
    let t = 0;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), ms);
    };
  };

  const applyFilter = () => {
    const q = filterText;
    const all = listEl.querySelectorAll('.email-item');
    all.forEach(el => {
      const text = el.innerText.toLowerCase();
      el.style.display = q ? (text.includes(q) ? '' : 'none') : '';
    });
  };

  searchInput.addEventListener('input', debounce((e) => {
    filterText = (e.target.value || '').toLowerCase().trim();
    applyFilter();
  }, 150));

  // initial boot
  document.addEventListener('DOMContentLoaded', () => {
    setupObserver();
    loadPage(); // fetch first page immediately
  });
})();
