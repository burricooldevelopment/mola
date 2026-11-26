from django.urls import path
from . import views

app_name = 'portfolio'   # templates use {% url 'portfolio:index' %}

urlpatterns = [
    # ==========================================================
    # PUBLIC PAGES
    # ==========================================================
    path('', views.index, name='index'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('cv/', views.cv, name='cv'),
    path('contact/', views.contact, name='contact'),

    # ==========================================================
    # DASHBOARD — OVERVIEW
    # ==========================================================
    path('dashboard/', views.dashboard_home, name='dash_home'),

    # ==========================================================
    # DASHBOARD — HERO SECTION
    # ==========================================================
    path('dashboard/hero/', views.dash_hero, name='dash_hero'),

    # Hero Stats (counter cards)
    path('dashboard/hero/stat/add/',
         views.dash_herostat_add, name='dash_herostat_add'),
    path('dashboard/hero/stat/<int:pk>/edit/',
         views.dash_herostat_edit, name='dash_herostat_edit'),
    path('dashboard/hero/stat/<int:pk>/delete/',
         views.dash_herostat_delete, name='dash_herostat_delete'),

    # ==========================================================
    # DASHBOARD — ABOUT SECTION
    # ==========================================================
    path('dashboard/about/', views.dash_about, name='dash_about'),

    # Core Values
    path('dashboard/about/value/add/',
         views.dash_value_add, name='dash_value_add'),
    path('dashboard/about/value/<int:pk>/edit/',
         views.dash_value_edit, name='dash_value_edit'),
    path('dashboard/about/value/<int:pk>/delete/',
         views.dash_value_delete, name='dash_value_delete'),

    # ==========================================================
    # DASHBOARD — SERVICES
    # ==========================================================
    path('dashboard/services/', views.dash_services, name='dash_services'),
    path('dashboard/services/add/',
         views.dash_service_add, name='dash_service_add'),
    path('dashboard/services/<int:pk>/edit/',
         views.dash_service_edit, name='dash_service_edit'),
    path('dashboard/services/<int:pk>/delete/',
         views.dash_service_delete, name='dash_service_delete'),

    # ==========================================================
    # DASHBOARD — PORTFOLIO (PROJECTS)
    # ==========================================================
    path('dashboard/portfolio/', views.dash_portfolio, name='dash_portfolio'),
    path('dashboard/portfolio/add/',
         views.dash_project_add, name='dash_project_add'),
    path('dashboard/portfolio/<int:pk>/edit/',
         views.dash_project_edit, name='dash_project_edit'),
    path('dashboard/portfolio/<int:pk>/delete/',
         views.dash_project_delete, name='dash_project_delete'),

    # ==========================================================
    # DASHBOARD — TESTIMONIALS
    # ==========================================================
    path('dashboard/testimonials/',
         views.dash_testimonials, name='dash_testimonials'),
    path('dashboard/testimonials/add/',
         views.dash_testimonial_add, name='dash_testimonial_add'),
    path('dashboard/testimonials/<int:pk>/edit/',
         views.dash_testimonial_edit, name='dash_testimonial_edit'),
    path('dashboard/testimonials/<int:pk>/delete/',
         views.dash_testimonial_delete, name='dash_testimonial_delete'),

    # ==========================================================
    # DASHBOARD — CV MANAGER
    # ==========================================================
    path('dashboard/cv/', views.dash_cv, name='dash_cv'),

    # CV Education
    path('dashboard/cv/education/add/',
         views.dash_education_add, name='dash_education_add'),
    path('dashboard/cv/education/<int:pk>/edit/',
         views.dash_education_edit, name='dash_education_edit'),
    path('dashboard/cv/education/<int:pk>/delete/',
         views.dash_education_delete, name='dash_education_delete'),

    # CV Experience
    path('dashboard/cv/experience/add/',
         views.dash_experience_add, name='dash_experience_add'),
    path('dashboard/cv/experience/<int:pk>/edit/',
         views.dash_experience_edit, name='dash_experience_edit'),
    path('dashboard/cv/experience/<int:pk>/delete/',
         views.dash_experience_delete, name='dash_experience_delete'),

    # CV Skills
    path('dashboard/cv/skill/add/',
         views.dash_skill_add, name='dash_skill_add'),
    path('dashboard/cv/skill/<int:pk>/edit/',
         views.dash_skill_edit, name='dash_skill_edit'),
    path('dashboard/cv/skill/<int:pk>/delete/',
         views.dash_skill_delete, name='dash_skill_delete'),

    # CV Languages
    path('dashboard/cv/language/add/',
         views.dash_language_add, name='dash_language_add'),
    path('dashboard/cv/language/<int:pk>/edit/',
         views.dash_language_edit, name='dash_language_edit'),
    path('dashboard/cv/language/<int:pk>/delete/',
         views.dash_language_delete, name='dash_language_delete'),

    # CV Certifications
    path('dashboard/cv/certification/add/',
         views.dash_cert_add, name='dash_cert_add'),
    path('dashboard/cv/certification/<int:pk>/edit/',
         views.dash_cert_edit, name='dash_cert_edit'),
    path('dashboard/cv/certification/<int:pk>/delete/',
         views.dash_cert_delete, name='dash_cert_delete'),

    # ==========================================================
    # DASHBOARD — CONTACT INFO & BRANDING
    # ==========================================================
    path('dashboard/contact-info/',
         views.dash_contact_info, name='dash_contact_info'),
    path('dashboard/branding/',
         views.dash_branding, name='dash_branding'),

    # ==========================================================
    # DASHBOARD — MESSAGES (INBOX)
    # ==========================================================
    path('dashboard/messages/',
         views.dash_messages, name='dash_messages'),
    path('dashboard/messages/<int:pk>/',
         views.dash_message_detail, name='dash_message_detail'),
    path('dashboard/messages/<int:pk>/delete/',
         views.dash_message_delete, name='dash_message_delete'),

     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
]