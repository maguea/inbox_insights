(function () {
  const listEl = document.getElementById('emailList');
  const sentinel = document.getElementById('loadSentinel');
  const loadMoreBtn = document.getElementById('loadMoreBtn');
  const searchInput = document.getElementById('emailSearch');

  const subjectEl = document.getElementById('emailSubject');
  const senderEl = document.getElementById('emailSender');
  const dateEl = document.getElementById('emailDate');
  const timeEl = document.getElementById('emailTime');
  const placeholder = document.getElementById('panePlaceholder');
  const detailPane = document.getElementById('paneDetail');

  let loading = false;
  let exhausted = false;
  let observer = null;
  let activeId = null;
  let filterText = '';

  function renderEmailBody(emailHtml) {
    const iframe = document.getElementById('emailBodyFrame');
    const doc = iframe.contentDocument || iframe.contentWindow.document;

    doc.open();
    doc.write(`
      <!DOCTYPE html>
      <html>
        <head>
          <base target="_blank">
          <style>
            body {
              font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
              margin: 0;
              padding: 1rem;
            }
          </style>
        </head>
        <body>
          ${emailHtml}
        </body>
      </html>
    `);
    doc.close();
  }

  const escapeHtml = (value) => {
    const str = String(value ?? '');
    return str.replace(/[&<>"']/g, (c) => {
      switch (c) {
        case '&': return '&amp;';
        case '<': return '&lt;';
        case '>': return '&gt;';
        case '"': return '&quot;';
        case "'": return '&#39;';
        default: return c;
      }
    });
  };

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
        listEl.querySelectorAll('.email-item.active')
          .forEach(el => el.classList.remove('active'));
        btn.classList.add('active');

        try {
          const res = await fetch(`/api/emails/${id}`);
          if (!res.ok) throw new Error(`Failed detail ${res.status}`);
          const email = await res.json();

          // ----- map JSON shape -> UI fields -----
          // sender object
          const senderName = email.sender?.sender_name ?? '';
          const senderAddr = email.sender?.sender_addr ?? '';
          const senderDisplay = senderAddr
            ? `${senderName || senderAddr} <${senderAddr}>`
            : (senderName || '(unknown sender)');

          // subject / preview / html body are nested under data
          const subject = email.data?.subject || email.subject || '(no subject)';
          const bodyHtml = email.data?.data || '';      // HTML body
          // const preview = email.data?.preview || email.preview || '';

          // collected_date -> date + time
          let dateText = email.collected_date || '';
          let timeText = '';
          if (email.collected_date) {
            const d = new Date(email.collected_date);
            if (!isNaN(d.getTime())) {
              dateText = d.toLocaleDateString();
              timeText = d.toLocaleTimeString();
            }
          }

          // fill pane
          subjectEl.textContent = subject;
          senderEl.textContent = senderDisplay;
          dateEl.textContent = dateText;
          timeEl.textContent = timeText;

          renderEmailBody(
            bodyHtml || `<p class="text-muted">(No body)</p>`
          );

          placeholder.classList.add('d-none');
          detailPane.classList.remove('d-none');
          detailPane.focus();
        } catch (err) {
          console.error(err);
        }
      });
    });
  };


  // Build and append list items from JSON
  const appendItems = (emails) => {
    if (!emails || emails.length === 0) return;

    emails.forEach(email => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'list-group-item list-group-item-action email-item text-start';
      btn.dataset.emailId = email.id;

      // sender is an object
      const senderName = email.sender?.sender_name
        || email.sender?.sender_addr
        || 'Unknown sender';

      const timestamp = email.timestamp || ''; // may be empty if API doesn't send it

      btn.innerHTML = `
        <div class="d-flex justify-content-between align-items-start mb-1">
          <span class="fw-semibold text-truncate">${escapeHtml(senderName)}</span>
          <small class="text-muted">${escapeHtml(timestamp)}</small>
        </div>
        <div class="small text-muted text-truncate">${escapeHtml(email.subject || '')}</div>
        <div class="small text-muted text-truncate">${escapeHtml(email.preview || '')}</div>
      `;

      // simple client-side filter on newly appended items
      if (filterText) {
        const t = btn.innerText.toLowerCase();
        if (!t.includes(filterText)) return;
      }

      listEl.insertBefore(btn, sentinel);
    });

    attachItemHandlers(listEl);
  };

  const loadPage = async () => {
    if (loading || exhausted) return;
    loading = true;
    setBusy(true);
    try {
      const p = nextPage();
      const res = await fetch(`/api/emails?page=${p}`);
      if (!res.ok) throw new Error(`Failed page ${p}: ${res.status}`);

      const emails = await res.json();

      if (!emails || emails.length === 0) {
        if (p === 1) {
          sentinel.innerHTML = '<span class="text-muted">No emails yet.</span>';
        } else {
          sentinel.innerHTML = '<span class="text-muted">No more emails.</span>';
          exhausted = true;
        }
        setBusy(false);
        loading = false;
        return;
      }

      appendItems(emails);
      bumpPage();
    } catch (err) {
      console.error(err);
      sentinel.innerHTML = '<span class="text-danger">Failed to load.</span>';
    } finally {
      setBusy(false);
      loading = false;
    }
  };

  const setupObserver = () => {
    if (!('IntersectionObserver' in window)) return;

    observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) loadPage();
      });
    }, { root: listEl, threshold: 0.1 });

    observer.observe(sentinel);
  };

  loadMoreBtn.addEventListener('click', loadPage);

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

  document.addEventListener('DOMContentLoaded', () => {
    setupObserver();
    loadPage(); // fetch first page immediately
  });
})();
