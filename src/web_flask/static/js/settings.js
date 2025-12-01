(function () {
    const successAlert = document.getElementById('successAlert');
    const successMessage = document.getElementById('successMessage');
    const errorAlert = document.getElementById('errorAlert');
    const errorMessage = document.getElementById('errorMessage');
    const connectionBadge = document.getElementById('connectionBadge');

    function showSuccess(msg) {
        successMessage.textContent = msg || 'Operation successful.';
        successAlert.classList.remove('d-none');
        errorAlert.classList.add('d-none');
    }

    function showError(msg) {
        errorMessage.textContent = msg || 'Something went wrong.';
        errorAlert.classList.remove('d-none');
        successAlert.classList.add('d-none');
    }

    function setConnectionStatus(ok, msg) {
        if (ok) {
            connectionBadge.className = 'badge bg-success';
            connectionBadge.textContent = msg || 'Connected';
        } else {
            connectionBadge.className = 'badge bg-danger';
            connectionBadge.textContent = msg || 'Not connected';
        }
    }

    // --- LOGIN ACTIONS ---

    const btnVerify = document.getElementById('btnVerify');
    const btnSaveKey = document.getElementById('btnSaveKey');
    const btnUpdateEmails = document.getElementById('btnUpdateEmails');

    function getLoginPayload() {
        return {
            user: document.getElementById('user').value.trim(),
            pass: document.getElementById('appKey').value.trim(),  // used only for save
            server: document.getElementById('server').value
        };
    }


    btnVerify.addEventListener('click', async () => {
        const payload = getLoginPayload();
        if (!payload.user) {
            showError('Username is required to verify login.');
            return;
        }
        try {
            const resp = await fetch('{{ url_for("api.check_email_account") }}', {
                method: 'GET',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    user: payload.user,
                    server: payload.server
                    // pass intentionally omitted – backend pulls appkey from DB
                })
            });
            const data = await resp.json();
            if (resp.ok && data.ok) {
                showSuccess(data.msg || 'Login verified successfully.');
                setConnectionStatus(true, 'Connected');
            } else {
                showError(data.msg || 'Login verification failed.');
                setConnectionStatus(false, 'Not connected');
            }
        } catch (err) {
            console.error(err);
            showError('Network error while verifying login.');
        }
    });


    btnSaveKey.addEventListener('click', async () => {
        const payload = getLoginPayload();
        if (!payload.user || !payload.pass) {
            showError('Username and app key are required to save.');
            return;
        }
        try {
            const resp = await fetch('{{ url_for("api.add_email") }}', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    user: payload.user,
                    password: payload.pass,
                    server: payload.server
                })
            });
            const data = await resp.json();
            if (resp.ok && data.ok) {
                showSuccess(data.msg || 'App key saved and login verified.');
                setConnectionStatus(true, 'Connected');
            } else {
                showError(data.msg || 'Failed to save app key.');
                setConnectionStatus(false, 'Not connected');
            }
        } catch (err) {
            console.error(err);
            showError('Network error while saving app key.');
        }
    });


    btnUpdateEmails.addEventListener('click', async () => {
        const server = document.getElementById('server').value;
        try {
            const resp = await fetch('{{ url_for("api.emails_update") }}', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ server })
            });
            const data = await resp.json();
            if (resp.ok && data.ok) {
                showSuccess(data.msg || 'Emails updated successfully.');
            } else {
                showError(data.msg || 'Failed to update emails.');
            }
        } catch (err) {
            console.error(err);
            showError('Network error while updating emails.');
        }
    });

    document.addEventListener('DOMContentLoaded', async function () {
        const payload = getLoginPayload();
        try {
            const resp = await fetch('{{ url_for("api.check_email_account") }}', {
                method: 'GET',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({
                    user: payload.user,
                    server: payload.server
                })
            });
            const data = await resp.json();
            setConnectionStatus(!!data.ok, data.msg);
        } catch (e) {
            console.error(e);
            setConnectionStatus(false, 'Unknown');
        }
    });


    // --- CATEGORIES UI / LOGIC ---

    const categoriesBody = document.getElementById('categoriesBody');
    const btnAddCategory = document.getElementById('btnAddCategory');

    function renderCategoryRow(cat) {
        const tr = document.createElement('tr');
        tr.dataset.name = cat.name || '';

        tr.innerHTML = `
            <td>
                <input type="text" class="form-control category-name" value="${cat.name || ''}" ${cat.name ? 'readonly' : ''}>
            </td>
            <td>
                <textarea class="form-control category-emails" rows="2"
                    placeholder="user@example.com, @domain.com">${(cat.emails || []).join(', ')}</textarea>
            </td>
            <td>
                <input type="number" min="0" class="form-control category-days"
                       value="${cat.days_until_delete != null ? cat.days_until_delete : ''}"
                       placeholder="e.g., 30">
            </td>
            <td class="text-end">
                <div class="btn-group" role="group">
                    <button type="button" class="btn btn-sm btn-outline-primary btn-save-category">
                        Save
                    </button>
                    <button type="button" class="btn btn-sm btn-outline-danger btn-delete-category">
                        Delete
                    </button>
                </div>
            </td>
        `;
        return tr;
    }

    async function loadCategories() {
        categoriesBody.innerHTML = `
            <tr><td colspan="4" class="text-center text-muted py-3">
                Loading categories...
            </td></tr>
        `;
        try {
            const resp = await fetch('{{ url_for("api.categories_list") }}');
            const data = await resp.json();
            if (!resp.ok || !data.ok) {
                throw new Error(data.msg || 'Failed to load categories');
            }
            const categories = data.categories || [];
            categoriesBody.innerHTML = '';
            if (!categories.length) {
                categoriesBody.innerHTML = `
                    <tr><td colspan="4" class="text-center text-muted py-3">
                        No categories yet. Click "Add Category" to create one.
                    </td></tr>
                `;
            } else {
                categories.forEach(cat => {
                    categoriesBody.appendChild(renderCategoryRow(cat));
                });
            }
        } catch (err) {
            console.error(err);
            categoriesBody.innerHTML = `
                <tr><td colspan="4" class="text-center text-danger py-3">
                    Failed to load categories.
                </td></tr>
            `;
        }
    }

    btnAddCategory.addEventListener('click', () => {
        const tr = renderCategoryRow({ name: '', emails: [], days_until_delete: '' });
        categoriesBody.prepend(tr);
    });

    // Event delegation for Save/Delete buttons
    categoriesBody.addEventListener('click', async (e) => {
        const target = e.target;
        const row = target.closest('tr');
        if (!row) return;

        if (target.classList.contains('btn-save-category')) {
            const nameInput = row.querySelector('.category-name');
            const emailsInput = row.querySelector('.category-emails');
            const daysInput = row.querySelector('.category-days');

            const name = nameInput.value.trim();
            const emails = emailsInput.value.split(',')
                .map(s => s.trim())
                .filter(Boolean);
            const days = daysInput.value.trim();

            if (!name) {
                showError('Category name is required.');
                return;
            }

            try {
                const resp = await fetch('{{ url_for("api.categories_upsert") }}', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name,
                        emails,
                        days_until_delete: days || null
                    })
                });
                const data = await resp.json();
                if (resp.ok && data.ok) {
                    showSuccess('Category saved.');
                    // Re-render from server so we have consistent state
                    loadCategories();
                } else {
                    showError(data.msg || 'Failed to save category.');
                }
            } catch (err) {
                console.error(err);
                showError('Network error while saving category.');
            }
        }

        if (target.classList.contains('btn-delete-category')) {
            const nameInput = row.querySelector('.category-name');
            const name = (nameInput.value || '').trim();
            if (!name) {
                // If it's a brand new unsaved row, just remove it
                row.remove();
                return;
            }
            if (!confirm(`Delete category "${name}"? This cannot be undone.`)) {
                return;
            }
            try {
                const resp = await fetch(
                    '{{ url_for("api.categories_delete", name="__NAME__") }}'.replace('__NAME__', encodeURIComponent(name)),
                    { method: 'DELETE' }
                );
                const data = await resp.json();
                if (resp.ok && data.ok) {
                    showSuccess('Category deleted.');
                    row.remove();
                    if (!categoriesBody.children.length) {
                        loadCategories();
                    }
                } else {
                    showError(data.msg || 'Failed to delete category.');
                }
            } catch (err) {
                console.error(err);
                showError('Network error while deleting category.');
            }
        }
    });

    // Initial load
    loadCategories();
})();