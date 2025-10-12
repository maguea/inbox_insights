
// static/js/history.js
(function () {
  'use strict';

  function log() {
    if (window && window.console) {
      console.log('[history.js]', ...arguments);
    }
  }
  function err() {
    if (window && window.console) {
      console.error('[history.js]', ...arguments);
    }
  }

  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn, { once: true });
    } else {
      fn();
    }
  }

  ready(function () {
    const listEl = document.getElementById('emailList');
    const searchEl = document.getElementById('emailSearch');
    const placeholder = document.getElementById('panePlaceholder');
    const detail = document.getElementById('paneDetail');
    const subjectEl = document.getElementById('emailSubject');
    const senderEl = document.getElementById('emailSender');
    const dateEl = document.getElementById('emailDate');
    const timeEl = document.getElementById('emailTime');
    const bodyEl = document.getElementById('emailBody');
    const contentEl = document.getElementById('emailContent');

    if (!listEl) {
      err('emailList not found in DOM. Is the scripts block included in base.html? Are IDs correct?');
      return;
    }

    log('initialized');

    const show = (el) => el && el.classList.remove('d-none');
    const hide = (el) => el && el.classList.add('d-none');

    function banner(msg, type = 'danger') {
      const div = document.createElement('div');
      div.className = `alert alert-${type} m-3`;
      div.role = 'alert';
      div.textContent = msg;
      contentEl?.prepend(div);
      setTimeout(() => div.remove(), 5000);
    }

    function clearActive() {
      listEl.querySelectorAll('.email-item.active').forEach(n => n.classList.remove('active'));
    }
    function setActive(btn) {
      btn.classList.add('active');
      btn.scrollIntoView({ block: 'nearest' });
    }

    async function fetchEmail(url) {
      log('fetching', url);
      const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
      if (!res.ok) throw new Error(`Failed to load email: ${res.status}`);
      return res.json();
    }

    function renderEmail(email) {
      subjectEl.textContent = email.subject || '';
      senderEl.textContent = email.sender || '';
      dateEl.textContent = email.date || '';
      timeEl.textContent = email.timestamp || '';
      bodyEl.innerHTML = email.body || '';

    }

    async function openEmail(btn) {
      const url = btn.dataset.detailUrl || (btn.dataset.emailId ? `/api/emails/${btn.dataset.emailId}` : '');
      if (!url) {
        err('No detail URL on item', btn);
        return;
      }

      hide(placeholder);
      hide(detail);

      const loading = document.createElement('div');
      loading.id = 'loadingIndicator';
      loading.className = 'text-center py-5';
      loading.innerHTML = '<div class="spinner-border" role="status"></div><p class="mt-2 text-muted">Loading…</p>';
      detail.parentElement.appendChild(loading);

      try {
        const email = await fetchEmail(url);
        renderEmail(email);
        clearActive();
        setActive(btn);
        show(detail);
      } catch (e) {
        err(e);
        banner(e.message || 'Failed to open email', 'danger');
        show(placeholder);
      } finally {
        loading.remove();
      }
    }

    // Delegated click (with document-level fallback for frameworks that swap DOM)
    document.addEventListener('click', (ev) => {
      const btn = ev.target.closest('.email-item');
      if (btn && document.body.contains(btn)) {
        ev.preventDefault();
        log('click item', btn.dataset.emailId || btn.dataset.detailUrl);
        openEmail(btn);
      }
    });

    // Search filter
    let timer;
    searchEl?.addEventListener('input', (ev) => {
      clearTimeout(timer);
      const q = (ev.target.value || '').toLowerCase().trim();
      timer = setTimeout(() => {
        listEl.querySelectorAll('.email-item').forEach(btn => {
          const text = btn.textContent.toLowerCase();
          btn.classList.toggle('d-none', q && !text.includes(q));
        });
      }, 120);
    });

    // Optional: auto-open first
    const first = listEl.querySelector('.email-item');
    if (first) {
      log('auto-open first');
      openEmail(first);
    }
  });
})();
