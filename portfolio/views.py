from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages as flash
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

from .forms import (
    ContactForm,
    # Dashboard forms
    HeroForm, HeroStatForm, AboutSectionForm, CoreValueForm,
    ServiceForm, ProjectForm, TestimonialForm, SiteSettingsForm,
    CVProfileForm, CVEducationForm, CVExperienceForm, CVSkillForm,
    CVLanguageForm, CVCertificationForm,
)
from .models import (
    # Public content models
    Project, Testimonial, Service, ContactMessage, SiteSettings,
    # Dashboard models
    Hero, HeroStat, AboutSection, CoreValue,
    CVProfile, CVEducation, CVExperience, CVSkill, CVLanguage, CVCertification,
)


# ==========================================================
# HELPER
# ==========================================================
def _category_filters(projects):
    """(value, label) pairs for the categories actually in use, in model order.
    Used to build filter buttons that always match the real project categories."""
    used = {p.category for p in projects}
    return [(value, label) for value, label in Project.CATEGORY_CHOICES if value in used]


def _unread_count():
    """Small helper — sidebar badge needs this on every dashboard page."""
    return ContactMessage.objects.filter(is_read=False).count()


# ==========================================================
# AUTH — LOGIN / LOGOUT
# ==========================================================
@csrf_protect
def login_view(request):
    """Custom branded login for the dashboard."""
    # Already logged in? Send straight to dashboard
    if request.user.is_authenticated:
        return redirect('portfolio:dash_home')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                # ?next= support
                next_url = request.GET.get('next') or request.POST.get('next') or 'portfolio:dash_home'
                return redirect(next_url)
            else:
                error = 'This account is disabled.'
        else:
            error = 'Invalid username or password.'

    return render(request, 'dashboard/login.html', {'error': error})


def logout_view(request):
    """Logout and redirect to login page."""
    auth_logout(request)
    return redirect('portfolio:login')


# ==========================================================
# PUBLIC PAGE VIEWS
# ==========================================================
def index(request):
    """Homepage — pulls ALL content from the database."""
    hero = Hero.load()
    about = AboutSection.load()
    site = SiteSettings.load()

    featured_projects = list(
        Project.objects.filter(is_active=True, is_featured=True)[:6]
    )
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    services = Service.objects.filter(is_active=True)
    hero_stats = HeroStat.objects.all()
    core_values = CoreValue.objects.filter(is_active=True)

    context = {
        'hero': hero,
        'about': about,
        'site': site,
        'hero_stats': hero_stats,
        'core_values': core_values,
        'services': services,
        'projects': featured_projects,
        'categories': _category_filters(featured_projects),
        'testimonials': testimonials,
        'form': ContactForm(),
    }
    return render(request, 'index.html', context)


def portfolio(request):
    """Portfolio page — all projects, grouped by category."""
    all_projects = Project.objects.filter(is_active=True)

    context = {
        'site': SiteSettings.load(),
        'cv_profile': CVProfile.load(),
        'hero_stats': HeroStat.objects.all(),
        'skills': CVSkill.objects.all()[:4],
        'services': Service.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True),
        'projects': all_projects,
        'categories': _category_filters(all_projects),
        'graphics_projects': all_projects.filter(category='graphics'),
        'software_projects': all_projects.filter(category='software'),
        'robotics_projects': all_projects.filter(category='robotics'),
    }
    return render(request, 'pages/portfolio.html', context)


def cv(request):
    """CV / Resume page — all content from database."""
    context = {
        'site': SiteSettings.load(),
        'cv_profile': CVProfile.load(),
        'educations': CVEducation.objects.all(),
        'experiences': CVExperience.objects.all(),
        'skills': CVSkill.objects.all(),
        'languages': CVLanguage.objects.all(),
        'certifications': CVCertification.objects.all(),
        'projects': Project.objects.filter(is_active=True)[:4],
        'services': Service.objects.filter(is_active=True),
        'form': ContactForm(),
    }
    return render(request, 'pages/cv.html', context)


# ==========================================================
# CONTACT FORM HANDLER (AJAX + normal fallback)
# ==========================================================
@require_POST
@csrf_protect
def contact(request):
    """
    Handles contact form submissions from:
      - Homepage (#contact)
      - CV page (#contact)
      - Portfolio page (#contact, if added)
    Supports AJAX (JSON) and normal POST (redirect + flash message).
    """
    form = ContactForm(request.POST)
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    referer = request.META.get('HTTP_REFERER') or '/'

    if form.is_valid():
        contact_msg = form.save()

        # Email notification (silent failure if email not configured)
        try:
            send_mail(
                subject=f"[MOLA TECH] New Contact: {contact_msg.subject}",
                message=(
                    f"Name:    {contact_msg.name}\n"
                    f"Email:   {contact_msg.email}\n"
                    f"Subject: {contact_msg.subject}\n\n"
                    f"Message:\n{contact_msg.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

        success_message = "Thanks for reaching out! We'll get back to you soon."

        if is_ajax:
            return JsonResponse({'success': True, 'message': success_message})

        flash.success(request, success_message)
        return redirect(referer)

    # ----- INVALID FORM -----
    if is_ajax:
        first_error = next(iter(form.errors.values()))[0] if form.errors else 'Please check the form.'
        return JsonResponse(
            {
                'success': False,
                'message': str(first_error),
                'errors': form.errors.get_json_data(),
            },
            status=400,
        )

    flash.error(request, 'Please correct the errors below and try again.')
    return redirect(referer)


# ==========================================================
# DASHBOARD — OVERVIEW
# ==========================================================
@login_required
def dashboard_home(request):
    """Dashboard overview with live counts + recent activity."""
    context = {
        'title': 'Dashboard Overview',
        'unread_count': _unread_count(),
        'counts': {
            'projects': Project.objects.count(),
            'services': Service.objects.count(),
            'testimonials': Testimonial.objects.count(),
            'unread': ContactMessage.objects.filter(is_read=False).count(),
        },
        'recent_projects': Project.objects.all()[:5],
        'recent_messages': ContactMessage.objects.all()[:5],
    }
    return render(request, 'dashboard/home.html', context)


# ==========================================================
# DASHBOARD — HERO SECTION
# ==========================================================
@login_required
def dash_hero(request):
    """Edit hero section + manage hero stat counters."""
    hero = Hero.load()

    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES, instance=hero)
        if form.is_valid():
            form.save()
            flash.success(request, 'Hero section updated successfully.')
            return redirect('portfolio:dash_hero')
    else:
        form = HeroForm(instance=hero)

    return render(request, 'dashboard/hero.html', {
        'title': 'Hero Section',
        'unread_count': _unread_count(),
        'form': form,
        'hero': hero,
        'stats': HeroStat.objects.all(),
    })


@login_required
def dash_herostat_add(request):
    """Add a hero stat counter."""
    if request.method == 'POST':
        form = HeroStatForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Stat added.')
            return redirect('portfolio:dash_hero')
    else:
        form = HeroStatForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Hero Stat',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_hero',
    })


@login_required
def dash_herostat_edit(request, pk):
    """Edit an existing hero stat counter."""
    obj = get_object_or_404(HeroStat, pk=pk)
    if request.method == 'POST':
        form = HeroStatForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Stat updated.')
            return redirect('portfolio:dash_hero')
    else:
        form = HeroStatForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Hero Stat',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_hero',
    })


@login_required
def dash_herostat_delete(request, pk):
    """Delete a hero stat counter."""
    get_object_or_404(HeroStat, pk=pk).delete()
    flash.success(request, 'Stat deleted.')
    return redirect('portfolio:dash_hero')


# ==========================================================
# DASHBOARD — ABOUT SECTION
# ==========================================================
@login_required
def dash_about(request):
    """Edit about section + manage core values."""
    about = AboutSection.load()

    if request.method == 'POST':
        form = AboutSectionForm(request.POST, instance=about)
        if form.is_valid():
            form.save()
            flash.success(request, 'About section updated.')
            return redirect('portfolio:dash_about')
    else:
        form = AboutSectionForm(instance=about)

    return render(request, 'dashboard/about.html', {
        'title': 'About Section',
        'unread_count': _unread_count(),
        'form': form,
        'values': CoreValue.objects.all(),
    })


@login_required
def dash_value_add(request):
    """Add a core value card."""
    if request.method == 'POST':
        form = CoreValueForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Core value added.')
            return redirect('portfolio:dash_about')
    else:
        form = CoreValueForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Core Value',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_about',
    })


@login_required
def dash_value_edit(request, pk):
    """Edit a core value card."""
    obj = get_object_or_404(CoreValue, pk=pk)
    if request.method == 'POST':
        form = CoreValueForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Core value updated.')
            return redirect('portfolio:dash_about')
    else:
        form = CoreValueForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Core Value',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_about',
    })


@login_required
def dash_value_delete(request, pk):
    """Delete a core value card."""
    get_object_or_404(CoreValue, pk=pk).delete()
    flash.success(request, 'Core value deleted.')
    return redirect('portfolio:dash_about')


# ==========================================================
# DASHBOARD — SERVICES
# ==========================================================
@login_required
def dash_services(request):
    """List all services."""
    return render(request, 'dashboard/services.html', {
        'title': 'Services',
        'unread_count': _unread_count(),
        'services': Service.objects.all(),
    })


@login_required
def dash_service_add(request):
    """Add a new service."""
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Service added.')
            return redirect('portfolio:dash_services')
    else:
        form = ServiceForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Service',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_services',
    })


@login_required
def dash_service_edit(request, pk):
    """Edit an existing service."""
    obj = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Service updated.')
            return redirect('portfolio:dash_services')
    else:
        form = ServiceForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Service',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_services',
    })


@login_required
def dash_service_delete(request, pk):
    """Delete a service."""
    get_object_or_404(Service, pk=pk).delete()
    flash.success(request, 'Service deleted.')
    return redirect('portfolio:dash_services')


# ==========================================================
# DASHBOARD — PORTFOLIO (PROJECTS)
# ==========================================================
@login_required
def dash_portfolio(request):
    """List all projects."""
    return render(request, 'dashboard/portfolio.html', {
        'title': 'Portfolio',
        'unread_count': _unread_count(),
        'projects': Project.objects.all(),
    })


@login_required
def dash_project_add(request):
    """Add a new project."""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            flash.success(request, 'Project added.')
            return redirect('portfolio:dash_portfolio')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/portfolio_form.html', {
        'title': 'Add Project',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_portfolio',
    })


@login_required
def dash_project_edit(request, pk):
    """Edit an existing project."""
    obj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Project updated.')
            return redirect('portfolio:dash_portfolio')
    else:
        form = ProjectForm(instance=obj)
    return render(request, 'dashboard/portfolio_form.html', {
        'title': 'Edit Project',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_portfolio',
        'project': obj,
    })


@login_required
def dash_project_delete(request, pk):
    """Delete a project."""
    get_object_or_404(Project, pk=pk).delete()
    flash.success(request, 'Project deleted.')
    return redirect('portfolio:dash_portfolio')


# ==========================================================
# DASHBOARD — TESTIMONIALS
# ==========================================================
@login_required
def dash_testimonials(request):
    """List all testimonials."""
    return render(request, 'dashboard/testimonials.html', {
        'title': 'Testimonials',
        'unread_count': _unread_count(),
        'testimonials': Testimonial.objects.all(),
    })


@login_required
def dash_testimonial_add(request):
    """Add a new testimonial."""
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            flash.success(request, 'Testimonial added.')
            return redirect('portfolio:dash_testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Testimonial',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_testimonials',
    })


@login_required
def dash_testimonial_edit(request, pk):
    """Edit an existing testimonial."""
    obj = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Testimonial updated.')
            return redirect('portfolio:dash_testimonials')
    else:
        form = TestimonialForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Testimonial',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_testimonials',
    })


@login_required
def dash_testimonial_delete(request, pk):
    """Delete a testimonial."""
    get_object_or_404(Testimonial, pk=pk).delete()
    flash.success(request, 'Testimonial deleted.')
    return redirect('portfolio:dash_testimonials')


# ==========================================================
# DASHBOARD — CV MANAGER
# ==========================================================
@login_required
def dash_cv(request):
    """CV manager — edit profile header + all CV sub-sections."""
    profile = CVProfile.load()

    if request.method == 'POST':
        form = CVProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            flash.success(request, 'CV profile updated.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVProfileForm(instance=profile)

    return render(request, 'dashboard/cv.html', {
        'title': 'CV Manager',
        'unread_count': _unread_count(),
        'form': form,
        'educations': CVEducation.objects.all(),
        'experiences': CVExperience.objects.all(),
        'skills': CVSkill.objects.all(),
        'languages': CVLanguage.objects.all(),
        'certifications': CVCertification.objects.all(),
    })


# --- CV Education ---
@login_required
def dash_education_add(request):
    """Add a CV education entry."""
    if request.method == 'POST':
        form = CVEducationForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Education entry added.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVEducationForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Education',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_education_edit(request, pk):
    """Edit a CV education entry."""
    obj = get_object_or_404(CVEducation, pk=pk)
    if request.method == 'POST':
        form = CVEducationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Education entry updated.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVEducationForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Education',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_education_delete(request, pk):
    """Delete a CV education entry."""
    get_object_or_404(CVEducation, pk=pk).delete()
    flash.success(request, 'Education entry deleted.')
    return redirect('portfolio:dash_cv')


# --- CV Experience ---
@login_required
def dash_experience_add(request):
    """Add a CV experience entry."""
    if request.method == 'POST':
        form = CVExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Experience entry added.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVExperienceForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Experience',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_experience_edit(request, pk):
    """Edit a CV experience entry."""
    obj = get_object_or_404(CVExperience, pk=pk)
    if request.method == 'POST':
        form = CVExperienceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Experience entry updated.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVExperienceForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Experience',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_experience_delete(request, pk):
    """Delete a CV experience entry."""
    get_object_or_404(CVExperience, pk=pk).delete()
    flash.success(request, 'Experience entry deleted.')
    return redirect('portfolio:dash_cv')


# --- CV Skill ---
@login_required
def dash_skill_add(request):
    """Add a CV skill."""
    if request.method == 'POST':
        form = CVSkillForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Skill added.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVSkillForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Skill',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_skill_edit(request, pk):
    """Edit a CV skill."""
    obj = get_object_or_404(CVSkill, pk=pk)
    if request.method == 'POST':
        form = CVSkillForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Skill updated.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVSkillForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Skill',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_skill_delete(request, pk):
    """Delete a CV skill."""
    get_object_or_404(CVSkill, pk=pk).delete()
    flash.success(request, 'Skill deleted.')
    return redirect('portfolio:dash_cv')


# --- CV Language ---
@login_required
def dash_language_add(request):
    """Add a CV language."""
    if request.method == 'POST':
        form = CVLanguageForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Language added.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVLanguageForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Language',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_language_edit(request, pk):
    """Edit a CV language."""
    obj = get_object_or_404(CVLanguage, pk=pk)
    if request.method == 'POST':
        form = CVLanguageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Language updated.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVLanguageForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Language',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_language_delete(request, pk):
    """Delete a CV language."""
    get_object_or_404(CVLanguage, pk=pk).delete()
    flash.success(request, 'Language deleted.')
    return redirect('portfolio:dash_cv')


# --- CV Certification ---
@login_required
def dash_cert_add(request):
    """Add a CV certification."""
    if request.method == 'POST':
        form = CVCertificationForm(request.POST)
        if form.is_valid():
            form.save()
            flash.success(request, 'Certification added.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVCertificationForm()
    return render(request, 'dashboard/form.html', {
        'title': 'Add Certification',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_cert_edit(request, pk):
    """Edit a CV certification."""
    obj = get_object_or_404(CVCertification, pk=pk)
    if request.method == 'POST':
        form = CVCertificationForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Certification updated.')
            return redirect('portfolio:dash_cv')
    else:
        form = CVCertificationForm(instance=obj)
    return render(request, 'dashboard/form.html', {
        'title': 'Edit Certification',
        'unread_count': _unread_count(),
        'form': form,
        'back_url': 'portfolio:dash_cv',
    })


@login_required
def dash_cert_delete(request, pk):
    """Delete a CV certification."""
    get_object_or_404(CVCertification, pk=pk).delete()
    flash.success(request, 'Certification deleted.')
    return redirect('portfolio:dash_cv')


# ==========================================================
# DASHBOARD — CONTACT INFO (SiteSettings)
# ==========================================================
@login_required
def dash_contact_info(request):
    """Edit contact info, working hours, social links."""
    site = SiteSettings.load()

    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=site)
        if form.is_valid():
            form.save()
            flash.success(request, 'Contact info updated.')
            return redirect('portfolio:dash_contact_info')
    else:
        form = SiteSettingsForm(instance=site)

    return render(request, 'dashboard/contact_info.html', {
        'title': 'Contact Info',
        'unread_count': _unread_count(),
        'form': form,
        'site': site,
    })


# ==========================================================
# DASHBOARD — BRANDING
# ==========================================================
@login_required
def dash_branding(request):
    """Branding page — shows current identity settings."""
    site = SiteSettings.load()
    return render(request, 'dashboard/branding.html', {
        'title': 'Branding',
        'unread_count': _unread_count(),
        'site': site,
    })


# ==========================================================
# DASHBOARD — MESSAGES (inbox)
# ==========================================================
@login_required
def dash_messages(request):
    """Inbox — list all contact messages."""
    return render(request, 'dashboard/messages.html', {
        'title': 'Messages',
        'unread_count': _unread_count(),
        'messages_list': ContactMessage.objects.all(),
    })


@login_required
def dash_message_detail(request, pk):
    """View a single message — marks it as read automatically."""
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save(update_fields=['is_read'])
    return render(request, 'dashboard/message_detail.html', {
        'title': 'Message',
        'unread_count': _unread_count(),
        'msg': msg,
    })


@login_required
def dash_message_delete(request, pk):
    """Delete a contact message."""
    get_object_or_404(ContactMessage, pk=pk).delete()
    flash.success(request, 'Message deleted.')
    return redirect('portfolio:dash_messages')