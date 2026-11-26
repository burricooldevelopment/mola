/* ============================================================
   MOLA TECH — Homepage JavaScript (Bootstrap 5 aware)
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- 1. PRELOADER ---------- */
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => setTimeout(() => preloader.classList.add('hidden'), 500));
        // Fail-safe: hide anyway after 3s in case load never fires
        setTimeout(() => preloader.classList.add('hidden'), 3000);
    }

    /* ---------- 2. SCROLL PROGRESS ---------- */
    const scrollProgress = document.getElementById('scrollProgress');
    if (scrollProgress) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            const total = document.documentElement.scrollHeight - window.innerHeight;
            scrollProgress.style.width = (total > 0 ? (scrolled / total) * 100 : 0) + '%';
        }, { passive: true });
    }

    /* ---------- 3. NAVBAR SCROLL ---------- */
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            navbar.classList.toggle('scrolled', window.scrollY > 40);
        }, { passive: true });
    }

    /* ---------- 4. ACTIVE NAV LINK ON SCROLL ---------- */
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.custom-navbar .nav-link');
    function setActiveNav() {
        let current = 'home';
        sections.forEach(s => {
            if (window.scrollY >= s.offsetTop - 140) current = s.id;
        });
        navLinks.forEach(l => {
            // Only hash links get active state
            const href = l.getAttribute('href') || '';
            l.classList.toggle('active', href === '#' + current);
        });
    }
    window.addEventListener('scroll', setActiveNav, { passive: true });
    setActiveNav();

    /* ---------- 5. SMOOTH SCROLL ---------- */
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', function (e) {
            const id = this.getAttribute('href');
            if (!id || id === '#' || id.length < 2) return;
            const target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            const top = target.getBoundingClientRect().top + window.scrollY - 80;
            window.scrollTo({ top, behavior: 'smooth' });

            // Close Bootstrap mobile menu after click
            const collapse = document.getElementById('navMenu');
            if (collapse && collapse.classList.contains('show') && window.bootstrap) {
                const bsCollapse = bootstrap.Collapse.getInstance(collapse)
                    || new bootstrap.Collapse(collapse, { toggle: false });
                bsCollapse.hide();
            }
        });
    });

    /* ---------- 6. REVEAL ANIMATION ---------- */
    const revealEls = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
        const revealObs = new IntersectionObserver((entries) => {
            entries.forEach(e => {
                if (e.isIntersecting) {
                    e.target.classList.add('revealed');
                    revealObs.unobserve(e.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });
        revealEls.forEach(el => revealObs.observe(el));
    } else {
        // Fallback: just show everything
        revealEls.forEach(el => el.classList.add('revealed'));
    }

    /* ---------- 7. COUNTER ---------- */
    let countersStarted = false;
    const counters = document.querySelectorAll('.stat-number');
    function startCounters() {
        if (countersStarted || !counters.length) return;
        const statsBox = document.querySelector('.hero-stats');
        if (!statsBox) return;
        const rect = statsBox.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            countersStarted = true;
            counters.forEach(counter => {
                const target = parseInt(counter.dataset.count, 10) || 0;
                const startTime = performance.now();
                const duration = 1800;
                function tick(now) {
                    const elapsed = now - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    counter.textContent = Math.floor(eased * target);
                    if (progress < 1) requestAnimationFrame(tick);
                    else counter.textContent = target;
                }
                requestAnimationFrame(tick);
            });
        }
    }
    window.addEventListener('scroll', startCounters, { passive: true });
    startCounters();

    /* ---------- 8. PORTFOLIO FILTER ---------- */
    const filterBtns = document.querySelectorAll('.filter-btn');
    const portfolioCols = document.querySelectorAll('.portfolio-col');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const filter = btn.dataset.filter;
            portfolioCols.forEach(col => {
                const cat = col.dataset.category;
                col.classList.toggle('hidden', !(filter === 'all' || cat === filter));
            });
        });
    });

    /* ---------- 9. TESTIMONIAL SLIDER ---------- */
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    const dots = document.querySelectorAll('.testimonial-dots .dot');
    let tIdx = 0;
    let tAuto;

    function goTestimonial(i) {
        if (!testimonialCards.length) return;
        tIdx = (i + testimonialCards.length) % testimonialCards.length;
        testimonialCards.forEach((c, idx) => c.classList.toggle('active', idx === tIdx));
        dots.forEach((d, idx) => d.classList.toggle('active', idx === tIdx));
    }
    function startAuto() {
        if (testimonialCards.length > 1) {
            tAuto = setInterval(() => goTestimonial(tIdx + 1), 5500);
        }
    }
    function resetAuto() {
        clearInterval(tAuto);
        startAuto();
    }

    dots.forEach(d => d.addEventListener('click', () => {
        goTestimonial(parseInt(d.dataset.index, 10));
        resetAuto();
    }));
    startAuto();

    /* ---------- 10. THEME TOGGLE ---------- */
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('mola-theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
        if (themeToggle) themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            const dark = document.body.classList.contains('dark-mode');
            themeToggle.innerHTML = dark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
            localStorage.setItem('mola-theme', dark ? 'dark' : 'light');
        });
    }

    /* ---------- 11. CONTACT FORM (AJAX) ---------- */
    const form = document.getElementById('contactForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const btn = form.querySelector('button[type="submit"]');
            const original = btn.innerHTML;
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';

            const data = new FormData(form);
            const csrfInput = form.querySelector('[name="csrfmiddlewaretoken"]');
            const csrf = csrfInput ? csrfInput.value : '';

            fetch(form.action, {
                method: 'POST',
                body: data,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrf
                }
            })
            .then(async (res) => {
                const json = await res.json().catch(() => ({}));
                if (res.ok && json.success) {
                    showToast(json.message || 'Message sent!', 'success');
                    form.reset();
                } else {
                    showToast(json.message || 'Something went wrong.', 'danger');
                }
            })
            .catch(() => showToast('Network error. Try again.', 'danger'))
            .finally(() => {
                btn.disabled = false;
                btn.innerHTML = original;
            });
        });
    }

    function showToast(msg, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} position-fixed top-0 start-50 translate-middle-x mt-3 shadow`;
        toast.style.zIndex = 100000;
        toast.style.minWidth = '300px';
        toast.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>${msg}`;
        document.body.appendChild(toast);
        setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.4s'; }, 3500);
        setTimeout(() => toast.remove(), 4000);
    }

    /* ---------- 12. BACK TO TOP ---------- */
    const btt = document.getElementById('backToTop');
    if (btt) {
        window.addEventListener('scroll', () => {
            btt.classList.toggle('visible', window.scrollY > 400);
        }, { passive: true });
        btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    /* ---------- 13. YEAR ---------- */
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

});