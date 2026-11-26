from django.contrib import admin
from django.utils.html import format_html

from .models import (
    # Existing
    ContactMessage,
    Project,
    Testimonial,
    Service,
    SiteSettings,
    # New (dashboard models)
    Hero,
    HeroStat,
    AboutSection,
    CoreValue,
    CVProfile,
    CVEducation,
    CVExperience,
    CVSkill,
    CVLanguage,
    CVCertification,
)


# ==========================================================
# CONTACT MESSAGES
# ==========================================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject_short', 'is_read_badge', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 25
    actions = ['mark_as_read', 'mark_as_unread']

    fieldsets = (
        ('Sender', {'fields': ('name', 'email')}),
        ('Message', {'fields': ('subject', 'message')}),
        ('Status', {'fields': ('is_read', 'created_at')}),
    )

    @admin.display(description='Subject')
    def subject_short(self, obj):
        return (obj.subject[:55] + '…') if len(obj.subject) > 55 else obj.subject

    @admin.display(description='Read?')
    def is_read_badge(self, obj):
        if obj.is_read:
            return format_html(
                '<span style="color:#16a34a;font-weight:600;">✓ Read</span>'
            )
        return format_html(
            '<span style="color:#dc2626;font-weight:600;">● Unread</span>'
        )

    @admin.action(description='Mark selected as read')
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.')

    @admin.action(description='Mark selected as unread')
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.')


# ==========================================================
# PROJECTS
# ==========================================================
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'client',
        'is_featured', 'is_active', 'display_order',
        'created_at',
    )
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'client', 'technologies')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_active', 'display_order')
    ordering = ('display_order', '-created_at')
    list_per_page = 25

    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'category', 'client', 'description')
        }),
        ('Media', {
            'fields': ('image', 'icon'),
            'description': 'Upload an image OR leave blank and provide a Bootstrap Icons class (e.g. "bi bi-code-slash").'
        }),
        ('Details', {
            'fields': ('technologies', 'link')
        }),
        ('Display', {
            'fields': ('is_featured', 'is_active', 'display_order')
        }),
    )


# ==========================================================
# TESTIMONIALS
# ==========================================================
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating_display', 'is_active', 'display_order', 'created_at')
    list_filter = ('is_active', 'rating', 'created_at')
    search_fields = ('name', 'role', 'message')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order', '-created_at')
    list_per_page = 25

    @admin.display(description='Rating')
    def rating_display(self, obj):
        return '★' * obj.rating + '☆' * (5 - obj.rating)


# ==========================================================
# SERVICES
# ==========================================================
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order', 'title')


# ==========================================================
# SITE SETTINGS
# ==========================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Identity', {
            'fields': ('site_name', 'tagline', 'about_summary')
        }),
        ('Contact Details', {
            'fields': (
                'email', 'phone_primary', 'phone_secondary',
                'location', 'working_hours',
            )
        }),
        ('Social Media', {
            'fields': (
                'instagram_url', 'linkedin_url', 'facebook_url',
                'twitter_url', 'whatsapp_url', 'github_url',
                'youtube_url', 'tiktok_url',
            )
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('updated_at',)


# ==========================================================
# HERO SECTION (singleton)
# ==========================================================
@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not Hero.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Badge', {
            'fields': ('badge_text',)
        }),
        ('Headline (4 pieces — highlight = gradient text)', {
            'fields': (
                'headline_1', 'headline_highlight_1',
                'headline_2', 'headline_highlight_2',
            ),
            'description': 'Example: "Where | Art | Meets | Code" → headline_1=Where, highlight_1=Art, headline_2=Meets, highlight_2=Code'
        }),
        ('Description', {
            'fields': ('paragraph',)
        }),
        ('Primary CTA', {
            'fields': ('cta_primary_text', 'cta_primary_link')
        }),
        ('Secondary CTA', {
            'fields': ('cta_secondary_text', 'cta_secondary_link')
        }),
        ('Tertiary CTA (View CV)', {
            'fields': ('cta_tertiary_text', 'cta_tertiary_link')
        }),
        ('Media', {
            'fields': ('hero_image',),
            'description': 'Profile photo shown in the hero right column.'
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('updated_at',)


# ==========================================================
# HERO STATS (counters) — FIXED
# ==========================================================
@admin.register(HeroStat)
class HeroStatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'display_order', 'value_preview')
    list_editable = ('value', 'suffix', 'display_order')
    ordering = ('display_order',)
    list_per_page = 20

    fieldsets = (
        ('Stat', {
            'fields': ('label', 'value', 'suffix'),
            'description': 'Example: label="Projects", value=50, suffix="+" → "50+ Projects"'
        }),
        ('Display', {
            'fields': ('display_order',)
        }),
    )

    @admin.display(description='Preview')
    def value_preview(self, obj):
        return f"{obj.value}{obj.suffix} {obj.label}"


# ==========================================================
# ABOUT SECTION (singleton)
# ==========================================================
@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Background Block', {
            'fields': ('background_title', 'background_text')
        }),
        ('Mission Block', {
            'fields': ('mission_title', 'mission_text')
        }),
        ('Vision Block', {
            'fields': ('vision_title', 'vision_text')
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('updated_at',)


# ==========================================================
# CORE VALUES (About section value cards)
# ==========================================================
@admin.register(CoreValue)
class CoreValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_preview', 'icon', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'display_order')
    ordering = ('display_order', 'title')
    list_per_page = 20

    @admin.display(description='Preview')
    def icon_preview(self, obj):
        if not obj.icon:
            return '—'
        return format_html(
            '<i class="{}" style="font-size:1.4rem;color:#a33a13;"></i>',
            obj.icon,
        )


# ==========================================================
# CV PROFILE (singleton)
# ==========================================================
@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not CVProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'job_title', 'photo')
        }),
        ('Contact', {
            'fields': (
                'email', 'phone_primary', 'phone_secondary',
                'location', 'website',
            )
        }),
        ('Summary', {
            'fields': ('summary',)
        }),
        ('Downloads', {
            'fields': ('cv_file',),
            'description': 'Optional PDF — will be linked from the "Download PDF" button on the CV page.'
        }),
        ('Metadata', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('updated_at',)


# ==========================================================
# CV EDUCATION
# ==========================================================
@admin.register(CVEducation)
class CVEducationAdmin(admin.ModelAdmin):
    list_display = (
        'degree', 'institution', 'start_year', 'end_year_or_present',
        'display_order',
    )
    search_fields = ('degree', 'institution', 'description')
    list_editable = ('display_order',)
    ordering = ('display_order', '-start_year')
    list_per_page = 25

    fieldsets = (
        ('Education', {
            'fields': ('institution', 'degree', 'start_year', 'end_year')
        }),
        ('Details', {
            'fields': ('description',),
            'description': 'Optional — e.g. "Graduated with First Class Honors"'
        }),
        ('Display', {
            'fields': ('display_order',)
        }),
    )

    @admin.display(description='End Year')
    def end_year_or_present(self, obj):
        return obj.end_year or 'Present'


# ==========================================================
# CV EXPERIENCE
# ==========================================================
@admin.register(CVExperience)
class CVExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'role', 'company', 'start_date', 'end_date_or_present',
        'bullet_count', 'display_order',
    )
    search_fields = ('role', 'company', 'description')
    list_editable = ('display_order',)
    ordering = ('display_order',)
    list_per_page = 25

    fieldsets = (
        ('Position', {
            'fields': ('role', 'company', 'start_date', 'end_date')
        }),
        ('Achievements', {
            'fields': ('description',),
            'description': 'One bullet point per line. Bullets (• or -) are optional — they will be stripped automatically.'
        }),
        ('Display', {
            'fields': ('display_order',)
        }),
    )

    @admin.display(description='End Date')
    def end_date_or_present(self, obj):
        return obj.end_date or 'Present'

    @admin.display(description='Bullets')
    def bullet_count(self, obj):
        return len(obj.bullet_list)


# ==========================================================
# CV SKILLS
# ==========================================================
@admin.register(CVSkill)
class CVSkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level_bar', 'level', 'category', 'display_order')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    list_editable = ('level', 'display_order')
    ordering = ('display_order', 'name')
    list_per_page = 30

    fieldsets = (
        ('Skill', {
            'fields': ('name', 'level', 'category')
        }),
        ('Display', {
            'fields': ('display_order',)
        }),
    )

    @admin.display(description='Progress')
    def level_bar(self, obj):
        return format_html(
            '<div style="background:#e5e7eb;border-radius:4px;width:120px;height:8px;display:inline-block;vertical-align:middle;">'
            '<div style="background:linear-gradient(90deg,#a33a13,#ff9a6b);'
            'width:{}%;height:100%;border-radius:4px;"></div></div>',
            obj.level,
        )


# ==========================================================
# CV LANGUAGES
# ==========================================================
@admin.register(CVLanguage)
class CVLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'display_order')
    list_filter = ('level',)
    search_fields = ('name',)
    list_editable = ('level', 'display_order')
    ordering = ('display_order', 'name')
    list_per_page = 25


# ==========================================================
# CV CERTIFICATIONS
# ==========================================================
@admin.register(CVCertification)
class CVCertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'year', 'display_order')
    search_fields = ('name', 'issuer')
    list_editable = ('display_order',)
    ordering = ('display_order', '-year')
    list_per_page = 25


# ==========================================================
# ADMIN SITE BRANDING
# ==========================================================
admin.site.site_header = 'MOLA TECH Admin'
admin.site.site_title = 'MOLA TECH'
admin.site.index_title = 'Manage your website'