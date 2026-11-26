/* ============================================================
   MOLA TECH — Personal Portfolio JavaScript
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {

    /* --------------------------------------------------
       1. PRELOADER
       -------------------------------------------------- */
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => preloader.classList.add('hidden'), 500);
        });
        setTimeout(() => preloader.classList.add('hidden'), 3000);
    }

    /* --------------------------------------------------
       2. SCROLL PROGRESS BAR
       -------------------------------------------------- */
    const scrollProgress = document.getElementById('scrollProgress');
    if (scrollProgress) {
        window.addEventListener('scroll', () => {
            const scrolled = window.scrollY;
            const docHeight = document.documentElement.scrollHeight - window.innerHeight;
            const percent = docHeight > 0 ? (scrolled / docHeight) * 100 : 0;
            scrollProgress.style.width = percent + '%';
        }, { passive: true });
    }

    /* --------------------------------------------------
       3. STICKY HEADER
       -------------------------------------------------- */
    const header = document.getElementById('header');
    if (header) {
        window.addEventListener('scroll', () => {
            header.classList.toggle('scrolled', window.scrollY > 40);
        }, { passive: true });
    }

    /* --------------------------------------------------
       4. MOBILE MENU TOGGLE
       -------------------------------------------------- */
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.getElementById('navLinks');

    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', (e) => {
            e.stopPropagation();
            mobileToggle.classList.toggle('active');
            navLinks.classList.toggle('open');
        });

        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileToggle.classList.remove('active');
                navLinks.classList.remove('open');
            });
        });

        document.addEventListener('click', (e) => {
            if (!navLinks.contains(e.target) && !mobileToggle.contains(e.target)) {
                mobileToggle.classList.remove('active');
                navLinks.classList.remove('open');
            }
        });
    }

    /* --------------------------------------------------
       5. SMOOTH SCROLL + ACTIVE NAV LINK
       -------------------------------------------------- */
    const sections = document.querySelectorAll('section[id]');
    const navItems = document.querySelectorAll('.nav-link');

    function updateActiveNav() {
        let current = 'home';
        sections.forEach(sec => {
            const top = sec.offsetTop - 130;
            if (window.scrollY >= top) current = sec.id;
        });
        navItems.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === '#' + current);
        });
    }
    window.addEventListener('scroll', updateActiveNav, { passive: true });
    updateActiveNav();

    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', function (e) {
            const id = this.getAttribute('href');
            if (id === '#' || id.length < 2) return;
            const target = document.querySelector(id);
            if (!target) return;
            e.preventDefault();
            const top = target.getBoundingClientRect().top + window.scrollY - 80;
            window.scrollTo({ top, behavior: 'smooth' });
        });
    });

    /* --------------------------------------------------
       6. TYPING EFFECT (hero title)
       -------------------------------------------------- */
    const typedText = document.getElementById('typedText');
    if (typedText) {
        const phrases = [
            'Software Engineer',
            'AI & Robotics Developer',
            'Graphics & 3D Designer',
            'Founder of MOLA TECH'
        ];
        let phraseIdx = 0;
        let charIdx = 0;
        let isDeleting = false;

        function typeLoop() {
            const current = phrases[phraseIdx];
            if (isDeleting) {
                charIdx--;
            } else {
                charIdx++;
            }
            typedText.textContent = current.substring(0, charIdx);

            let delay = isDeleting ? 50 : 100;
            if (!isDeleting && charIdx === current.length) {
                delay = 1800;
                isDeleting = true;
            } else if (isDeleting && charIdx === 0) {
                isDeleting = false;
                phraseIdx = (phraseIdx + 1) % phrases.length;
                delay = 400;
            }
            setTimeout(typeLoop, delay);
        }
        typeLoop();
    }

    /* --------------------------------------------------
       7. COUNTER ANIMATION
       -------------------------------------------------- */
    const counters = document.querySelectorAll('.counter');
    let countersStarted = false;

    function startCounters() {
        if (countersStarted || !counters.length) return;
        const stats = document.querySelector('.stats');
        if (!stats) return;

        const rect = stats.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            countersStarted = true;
            counters.forEach(counter => {
                const target = parseInt(counter.dataset.target) || 0;
                const duration = 1800;
                const startTime = performance.now();

                function tick(now) {
                    const elapsed = now - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3);
                    counter.textContent = Math.floor(eased * target);
                    if (progress < 1) {
                        requestAnimationFrame(tick);
                    } else {
                        counter.textContent = target;
                    }
                }
                requestAnimationFrame(tick);
            });
        }
    }
    window.addEventListener('scroll', startCounters, { passive: true });
    startCounters();

    /* --------------------------------------------------
       8. SCROLL REVEAL
       -------------------------------------------------- */
    const revealEls = document.querySelectorAll('.reveal');
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                revealObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -50px 0px' });

    revealEls.forEach(el => revealObserver.observe(el));

    /* --------------------------------------------------
       9. SKILL BARS ANIMATION
       -------------------------------------------------- */
    const skillFills = document.querySelectorAll('.skill-fill');
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fill = entry.target;
                const skill = fill.closest('.skill');
                const percent = skill ? skill.dataset.percent : '0';
                setTimeout(() => {
                    fill.style.width = percent + '%';
                }, 200);
                skillObserver.unobserve(fill);
            }
        });
    }, { threshold: 0.4 });

    skillFills.forEach(fill => skillObserver.observe(fill));

    /* --------------------------------------------------
       10. PORTFOLIO FILTER
       -------------------------------------------------- */
    const filterBtns = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item[data-category]');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;

            portfolioItems.forEach(item => {
                const show = filter === 'all' || item.dataset.category === filter;
                if (show) {
                    item.style.display = '';
                    item.classList.remove('revealed');
                    // force reflow for animation
                    void item.offsetWidth;
                    item.classList.add('revealed');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    /* --------------------------------------------------
       11. PORTFOLIO LIGHTBOX
       -------------------------------------------------- */
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const lightboxClose = document.getElementById('lightboxClose');

    portfolioItems.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            if (!img || !lightbox || !lightboxImg) return;
            lightboxImg.src = img.src;
            lightboxImg.alt = img.alt || 'Preview';
            lightbox.classList.add('open');
            document.body.style.overflow = 'hidden';
        });
    });

    function closeLightbox() {
        if (!lightbox) return;
        lightbox.classList.remove('open');
        document.body.style.overflow = '';
    }

    if (lightboxClose) lightboxClose.addEventListener('click', closeLightbox);
    if (lightbox) {
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) closeLightbox();
        });
    }
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeLightbox();
    });

    /* --------------------------------------------------
       12. TESTIMONIALS SLIDER
       -------------------------------------------------- */
    const track = document.getElementById('testimonialTrack');
    const dots = document.querySelectorAll('#testimonialDots .dot');
    const prevBtn = document.getElementById('prevTestimonial');
    const nextBtn = document.getElementById('nextTestimonial');
    const totalSlides = track ? track.children.length : 0;
    let slideIdx = 0;
    let autoplay;

    function goToSlide(idx) {
        if (!track || totalSlides === 0) return;
        slideIdx = (idx + totalSlides) % totalSlides;
        track.style.transform = `translateX(-${slideIdx * 100}%)`;
        dots.forEach((dot, i) => dot.classList.toggle('active', i === slideIdx));
    }

    function nextSlide() { goToSlide(slideIdx + 1); }
    function prevSlide() { goToSlide(slideIdx - 1); }

    if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); resetAutoplay(); });
    if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); resetAutoplay(); });
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            goToSlide(parseInt(dot.dataset.index));
            resetAutoplay();
        });
    });

    function startAutoplay() {
        if (totalSlides > 1) autoplay = setInterval(nextSlide, 6000);
    }
    function resetAutoplay() {
        clearInterval(autoplay);
        startAutoplay();
    }
    startAutoplay();

    /* Swipe support */
    if (track) {
        let startX = 0;
        let endX = 0;
        track.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        }, { passive: true });

        track.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            const delta = endX - startX;
            if (Math.abs(delta) > 50) {
                delta < 0 ? nextSlide() : prevSlide();
                resetAutoplay();
            }
        }, { passive: true });
    }

    /* --------------------------------------------------
       13. THEME TOGGLE (dark / light)
       -------------------------------------------------- */
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('mola-portfolio-theme');

    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
        if (themeToggle) themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-mode');
            const isLight = document.body.classList.contains('light-mode');
            themeToggle.innerHTML = isLight
                ? '<i class="fa-solid fa-sun"></i>'
                : '<i class="fa-solid fa-moon"></i>';
            localStorage.setItem('mola-portfolio-theme', isLight ? 'light' : 'dark');
        });
    }

    /* --------------------------------------------------
       14. CONTACT FORM (AJAX)
       -------------------------------------------------- */
    const contactForm = document.getElementById('contactForm');
    const formStatus = document.getElementById('formStatus');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const name = contactForm.querySelector('[name="name"]').value.trim();
            const email = contactForm.querySelector('[name="email"]').value.trim();
            const subject = contactForm.querySelector('[name="subject"]').value.trim();
            const message = contactForm.querySelector('[name="message"]').value.trim();
            const submitBtn = contactForm.querySelector('button[type="submit"]');

            if (!name || !email || !subject || !message) {
                showStatus('Please fill in all fields.', 'error');
                return;
            }
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                showStatus('Please enter a valid email address.', 'error');
                return;
            }

            const originalHTML = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';

            const formData = new FormData(contactForm);
            const csrfToken = contactForm.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';

            fetch(contactForm.action, {
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
                    showStatus(data.message || 'Message sent successfully!', 'success');
                    contactForm.reset();
                } else {
                    showStatus(data.message || 'Something went wrong. Please try again.', 'error');
                }
            })
            .catch(() => {
                showStatus('Network error. Please try again later.', 'error');
            })
            .finally(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalHTML;
            });
        });
    }

    function showStatus(msg, type) {
        if (!formStatus) return;
        formStatus.textContent = msg;
        formStatus.className = 'form-status ' + type;
        setTimeout(() => {
            if (formStatus.textContent === msg) {
                formStatus.textContent = '';
                formStatus.className = 'form-status';
            }
        }, 6000);
    }

    /* --------------------------------------------------
       15. BACK TO TOP
       -------------------------------------------------- */
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', () => {
            backToTop.classList.toggle('visible', window.scrollY > 400);
        }, { passive: true });

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* --------------------------------------------------
       16. CURRENT YEAR
       -------------------------------------------------- */
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    /* --------------------------------------------------
       17. CUSTOM CURSOR (desktop only)
       -------------------------------------------------- */
    const cursorDot = document.getElementById('cursorDot');
    const cursorRing = document.getElementById('cursorRing');
    const isDesktop = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

    if (isDesktop && cursorDot && cursorRing) {
        let mouseX = 0, mouseY = 0;
        let ringX = 0, ringY = 0;

        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            document.body.classList.add('cursor-active');
            cursorDot.style.transform = `translate(${mouseX - 4}px, ${mouseY - 4}px)`;
        });

        function animateRing() {
            ringX += (mouseX - ringX) * 0.18;
            ringY += (mouseY - ringY) * 0.18;
            cursorRing.style.transform = `translate(${ringX - 18}px, ${ringY - 18}px)`;
            requestAnimationFrame(animateRing);
        }
        animateRing();

        // Hover effect on interactive elements
        const hoverTargets = 'a, button, .service-card, .portfolio-item, .stat-box';
        document.querySelectorAll(hoverTargets).forEach(el => {
            el.addEventListener('mouseenter', () => {
                cursorRing.style.width = '56px';
                cursorRing.style.height = '56px';
                cursorRing.style.borderColor = 'var(--accent)';
            });
            el.addEventListener('mouseleave', () => {
                cursorRing.style.width = '36px';
                cursorRing.style.height = '36px';
                cursorRing.style.borderColor = 'var(--primary)';
            });
        });
    }

    /* --------------------------------------------------
       18. PARALLAX ORBS
       -------------------------------------------------- */
    const orbs = document.querySelectorAll('.orb');
    if (orbs.length && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        window.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 30;
            const y = (e.clientY / window.innerHeight - 0.5) * 30;
            orbs.forEach((orb, i) => {
                const factor = (i + 1) * 0.6;
                orb.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
            });
        }, { passive: true });
    }

    /* --------------------------------------------------
       19. LAZY IMAGE FADE-IN
       -------------------------------------------------- */
    document.querySelectorAll('.portfolio-item img').forEach(img => {
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.5s ease';
        if (img.complete) {
            img.style.opacity = '1';
        } else {
            img.addEventListener('load', () => { img.style.opacity = '1'; });
            img.addEventListener('error', () => { img.style.opacity = '1'; });
        }
    });

    /* --------------------------------------------------
       20. KEYBOARD SHORTCUTS
       -------------------------------------------------- */
    document.addEventListener('keydown', (e) => {
        // Escape closes mobile menu
        if (e.key === 'Escape' && navLinks && navLinks.classList.contains('open')) {
            navLinks.classList.remove('open');
            if (mobileToggle) mobileToggle.classList.remove('active');
        }
        // Arrow keys navigate testimonials
        if (lightbox && lightbox.classList.contains('open')) return;
        if (e.key === 'ArrowRight' && nextBtn && document.activeElement?.closest('.testimonial-slider')) {
            nextSlide();
            resetAutoplay();
        }
        if (e.key === 'ArrowLeft' && prevBtn && document.activeElement?.closest('.testimonial-slider')) {
            prevSlide();
            resetAutoplay();
        }
    });

});
