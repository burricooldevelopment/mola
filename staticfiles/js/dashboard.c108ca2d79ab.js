document.addEventListener('DOMContentLoaded', function () {

    /* ---------- Sidebar toggle (mobile) ---------- */
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.getElementById('hamburger');
    const sidebarClose = document.getElementById('sidebarClose');

    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    document.body.appendChild(overlay);

    function openSidebar() {
        sidebar.classList.add('open');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    function closeSidebar() {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (hamburger) {
        hamburger.addEventListener('click', function (e) {
            e.stopPropagation();
            sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
        });
    }
    if (sidebarClose) sidebarClose.addEventListener('click', closeSidebar);
    overlay.addEventListener('click', closeSidebar);

    window.addEventListener('resize', function () {
        if (window.innerWidth > 992) closeSidebar();
    });

    /* ---------- User dropdown ---------- */
    const userChip = document.getElementById('userChip');
    const userDropdown = document.querySelector('.user-dropdown');

    if (userChip && userDropdown) {
        userChip.addEventListener('click', function (e) {
            e.stopPropagation();
            userDropdown.classList.toggle('open');
        });
        document.addEventListener('click', function (e) {
            if (!userDropdown.contains(e.target)) {
                userDropdown.classList.remove('open');
            }
        });
    }

    /* ---------- Auto-dismiss toasts ---------- */
    document.querySelectorAll('.toast').forEach(function (toast) {
        setTimeout(function () {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
        }, 4000);
        setTimeout(function () { toast.remove(); }, 4500);
    });

    /* ---------- Animated stat counters ---------- */
    const statValues = document.querySelectorAll('.stat-info h3');
    let countersStarted = false;

    function animateCounters() {
        if (countersStarted) return;
        countersStarted = true;

        statValues.forEach(function (el) {
            const target = parseInt(el.textContent.trim(), 10);
            if (isNaN(target)) return;

            let current = 0;
            const step = Math.max(1, Math.ceil(target / 30));
            const interval = setInterval(function () {
                current += step;
                if (current >= target) {
                    current = target;
                    clearInterval(interval);
                }
                el.textContent = current;
            }, 25);
        });
    }

    const statGrid = document.querySelector('.stat-grid');
    if (statGrid && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.disconnect();
                }
            });
        }, { threshold: 0.3 });
        observer.observe(statGrid);
    } else {
        animateCounters();
    }

    /* ---------- Close dropdowns with Escape ---------- */
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            if (userDropdown) userDropdown.classList.remove('open');
            if (sidebar.classList.contains('open')) closeSidebar();
        }
    });

    /* ---------- Confirm delete shortcuts (fallback for elements without onclick) ---------- */
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(this.getAttribute('data-confirm') || 'Are you sure?')) {
                e.preventDefault();
            }
        });
    });

});