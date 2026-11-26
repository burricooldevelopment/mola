document.addEventListener('DOMContentLoaded', function () {

    /* --------------------------------------------------
       1. THEME TOGGLE (dark / light mode)
       -------------------------------------------------- */
    const modeToggle = document.getElementById('modeToggle');
    const savedTheme = localStorage.getItem('mola-cv-theme');

    // Apply saved theme on load
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (modeToggle) modeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    if (modeToggle) {
        modeToggle.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            modeToggle.innerHTML = isDark
                ? '<i class="fas fa-sun"></i>'
                : '<i class="fas fa-moon"></i>';
            localStorage.setItem('mola-cv-theme', isDark ? 'dark' : 'light');
        });
    }

    /* --------------------------------------------------
       2. DOWNLOAD PDF BUTTON
       -------------------------------------------------- */
    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function () {
            // Make sure Home page is active before printing
            showPage('home');

            // Small delay to let the page re-render
            setTimeout(() => {
                window.print();
            }, 300);
        });
    }

    /* --------------------------------------------------
       3. NAV PAGE SWITCHING
       -------------------------------------------------- */
    const navLinks = document.querySelectorAll('.nav-link');
    const pages = document.querySelectorAll('.page');

    function showPage(pageId) {
        // Hide all pages
        pages.forEach(p => p.classList.remove('active'));
        // Show target
        const target = document.getElementById(pageId);
        if (target) target.classList.add('active');
        // Update active nav link
        navLinks.forEach(link => {
            link.classList.toggle('active', link.dataset.page === pageId);
        });
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // If it's an in-page section (services/contact)
            if (href.startsWith('#')) {
                e.preventDefault();
                const pageId = this.dataset.page;
                if (pageId) {
                    showPage(pageId);
                }
                // Also close any open mobile nav if any
            }
            // If it's a Django URL (index / portfolio) — let it navigate normally
        });
    });

    /* --------------------------------------------------
       4. CONTACT FORM — validation + AJAX
       -------------------------------------------------- */
    const contactForm = document.querySelector('#contact .contact-form');
    const submitBtn = contactForm ? contactForm.querySelector('.submit-btn') : null;

    if (contactForm && submitBtn) {
        // Wrap inputs in a <form> dynamically if not already a form
        // (Original markup uses a div; we convert it in JS)
        if (contactForm.tagName.toLowerCase() !== 'form') {
            const form = document.createElement('form');
            form.className = contactForm.className;
            form.id = 'cvContactForm';
            form.method = 'POST';
            form.action = '/contact/'; // will be replaced by Django URL below
            form.innerHTML = contactForm.innerHTML;
            contactForm.replaceWith(form);
            // re-query
            initContactForm(form);
        } else {
            initContactForm(contactForm);
        }
    }

    function initContactForm(form) {
        const btn = form.querySelector('.submit-btn') || form.querySelector('button[type="submit"]');
        const nameInput = form.querySelector('#name, [name="name"]');
        const emailInput = form.querySelector('#email, [name="email"]');
        const subjectInput = form.querySelector('#subject, [name="subject"]');
        const messageInput = form.querySelector('#message, [name="message"]');

        // Add a status element
        let statusEl = form.querySelector('.form-status');
        if (!statusEl) {
            statusEl = document.createElement('div');
            statusEl.className = 'form-status';
            statusEl.style.marginTop = '10px';
            statusEl.style.fontSize = '14px';
            statusEl.style.fontWeight = '600';
            form.appendChild(statusEl);
        }

        // Ensure inputs have proper names for Django
        if (nameInput && !nameInput.name) nameInput.name = 'name';
        if (emailInput && !emailInput.name) emailInput.name = 'email';
        if (subjectInput && !subjectInput.name) subjectInput.name = 'subject';
        if (messageInput && !messageInput.name) messageInput.name = 'message';

        // Add CSRF token if not present (Django will reject without it)
        if (!form.querySelector('[name="csrfmiddlewaretoken"]')) {
            const csrfToken = getCookie('csrftoken');
            if (csrfToken) {
                const hidden = document.createElement('input');
                hidden.type = 'hidden';
                hidden.name = 'csrfmiddlewaretoken';
                hidden.value = csrfToken;
                form.insertBefore(hidden, form.firstChild);
            }
        }

        // Submit handler
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            const name = nameInput ? nameInput.value.trim() : '';
            const email = emailInput ? emailInput.value.trim() : '';
            const subject = subjectInput ? subjectInput.value.trim() : '';
            const message = messageInput ? messageInput.value.trim() : '';

            // Validation
            if (!name || !email || !subject || !message) {
                setStatus('Please fill in all fields.', 'error');
                return;
            }
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                setStatus('Please enter a valid email address.', 'error');
                return;
            }

            // Loading state
            const originalHTML = btn ? btn.innerHTML : '';
            if (btn) {
                btn.disabled = true;
                btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            }

            const formData = new FormData(form);
            const csrfToken = form.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';

            fetch(form.action || '/contact/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(async (res) => {
                const data = await res.json().catch(() => ({}));
                if (res.ok && data.success) {
                    setStatus(data.message || 'Message sent successfully!', 'success');
                    form.reset();
                } else {
                    setStatus(data.message || 'Something went wrong. Please try again.', 'error');
                }
            })
            .catch(() => {
                setStatus('Network error. Please try again later.', 'error');
            })
            .finally(() => {
                if (btn) {
                    btn.disabled = false;
                    btn.innerHTML = originalHTML;
                }
            });
        });

        function setStatus(msg, type) {
            if (!statusEl) return;
            statusEl.textContent = msg;
            statusEl.style.color = type === 'success' ? '#16a34a' : '#dc2626';
            // auto-clear after 6s
            setTimeout(() => {
                if (statusEl.textContent === msg) {
                    statusEl.textContent = '';
                }
            }, 6000);
        }
    }

    /* --------------------------------------------------
       5. CSRF COOKIE HELPER
       -------------------------------------------------- */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    /* --------------------------------------------------
       6. SMOOTH SCROLL FOR IN-PAGE ANCHORS (fallback)
       -------------------------------------------------- */
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#' || href.length < 2) return;
            const target = document.querySelector(href);
            if (!target) return;
            // only smooth-scroll if target exists on the same page
            e.preventDefault();
            const top = target.getBoundingClientRect().top + window.scrollY - 80;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });

    /* --------------------------------------------------
       7. KEYBOARD SHORTCUTS
       -------------------------------------------------- */
    document.addEventListener('keydown', function (e) {
        // Ctrl/Cmd + P → download PDF (respect browser default too)
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            // Let browser handle print natively
            // (no need to override, but we ensure home is active)
            showPage('home');
        }
        // Esc → go home page
        if (e.key === 'Escape') {
            showPage('home');
        }
    });

    /* --------------------------------------------------
       8. ACTIVE NAV SYNC ON LOAD
       -------------------------------------------------- */
    // If URL has a hash matching a page id, activate it
    const hash = window.location.hash.replace('#', '');
    if (hash && document.getElementById(hash)) {
        showPage(hash);
    }

    /* --------------------------------------------------
       9. PRINT HANDLING (ensures nav & controls hidden)
       -------------------------------------------------- */
    window.addEventListener('beforeprint', function () {
        // Ensure only the active page prints
        pages.forEach(p => {
            if (!p.classList.contains('active')) {
                p.style.display = 'none';
            }
        });
    });

    window.addEventListener('afterprint', function () {
        // Restore display
        pages.forEach(p => {
            p.style.display = '';
        });
    });

});