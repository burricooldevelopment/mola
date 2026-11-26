from django import forms
from .models import (
    # Public content models
    ContactMessage, Project, Testimonial, Service, SiteSettings,
    # Dashboard models
    Hero, HeroStat, AboutSection, CoreValue,
    CVProfile, CVEducation, CVExperience, CVSkill, CVLanguage, CVCertification,
)


# ==========================================================
# PUBLIC FORMS
# ==========================================================

class ContactForm(forms.ModelForm):
    """
    Contact form used by views.contact() on all three pages.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'John Doe',
                'class': 'form-control',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'john@example.com',
                'class': 'form-control',
                'autocomplete': 'email',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Project Inquiry',
                'class': 'form-control',
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Tell us about your project...',
                'rows': 5,
                'class': 'form-control',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters.')
        return name

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if len(subject) < 3:
            raise forms.ValidationError('Subject must be at least 3 characters.')
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters.')
        return message


# ==========================================================
# DASHBOARD FORMS
# All dashboard forms use the `dash-input` class so the
# dashboard CSS can style them consistently.
# ==========================================================

class HeroForm(forms.ModelForm):
    """Edit the homepage hero section."""
    class Meta:
        model = Hero
        fields = '__all__'
        widgets = {
            'badge_text': forms.TextInput(attrs={'class': 'dash-input'}),
            'headline_1': forms.TextInput(attrs={'class': 'dash-input'}),
            'headline_highlight_1': forms.TextInput(attrs={'class': 'dash-input'}),
            'headline_2': forms.TextInput(attrs={'class': 'dash-input'}),
            'headline_highlight_2': forms.TextInput(attrs={'class': 'dash-input'}),
            'paragraph': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
            'cta_primary_text': forms.TextInput(attrs={'class': 'dash-input'}),
            'cta_primary_link': forms.TextInput(attrs={'class': 'dash-input'}),
            'cta_secondary_text': forms.TextInput(attrs={'class': 'dash-input'}),
            'cta_secondary_link': forms.TextInput(attrs={'class': 'dash-input'}),
            'cta_tertiary_text': forms.TextInput(attrs={'class': 'dash-input'}),
            'cta_tertiary_link': forms.TextInput(attrs={'class': 'dash-input'}),
            'hero_image': forms.ClearableFileInput(attrs={'class': 'dash-input'}),
        }


class HeroStatForm(forms.ModelForm):
    """Add or edit a hero stat counter."""
    class Meta:
        model = HeroStat
        fields = '__all__'
        widgets = {
            'label': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Projects',
            }),
            'value': forms.NumberInput(attrs={
                'class': 'dash-input',
                'placeholder': '50',
            }),
            'suffix': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': '+',
            }),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class AboutSectionForm(forms.ModelForm):
    """Edit background / mission / vision blocks."""
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {
            'background_title': forms.TextInput(attrs={'class': 'dash-input'}),
            'background_text': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
            'mission_title': forms.TextInput(attrs={'class': 'dash-input'}),
            'mission_text': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
            'vision_title': forms.TextInput(attrs={'class': 'dash-input'}),
            'vision_text': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
        }


class CoreValueForm(forms.ModelForm):
    """Add or edit a core value card."""
    class Meta:
        model = CoreValue
        fields = '__all__'
        widgets = {
            'icon': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'fas fa-lightbulb',
            }),
            'title': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Innovation',
            }),
            'description': forms.Textarea(attrs={'class': 'dash-input', 'rows': 2}),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class ServiceForm(forms.ModelForm):
    """Add or edit a service card."""
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'dash-input'}),
            'description': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
            'icon': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'fas fa-code',
            }),
            'bullet_points': forms.Textarea(attrs={
                'class': 'dash-input',
                'rows': 5,
                'placeholder': 'Logo Design\nBranding & Identity\nMarketing Materials',
            }),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class ProjectForm(forms.ModelForm):
    """Add or edit a portfolio project."""
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'dash-input'}),
            'slug': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'auto-generated if blank',
            }),
            'category': forms.Select(attrs={'class': 'dash-input'}),
            'description': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
            'client': forms.TextInput(attrs={'class': 'dash-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'dash-input'}),
            'icon': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'fas fa-palette',
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'React, Django, PostgreSQL',
            }),
            'link': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://example.com',
            }),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class TestimonialForm(forms.ModelForm):
    """Add or edit a testimonial."""
    class Meta:
        model = Testimonial
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'dash-input'}),
            'role': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'CEO, XYZ Corp',
            }),
            'message': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'dash-input'}),
            'rating': forms.Select(attrs={'class': 'dash-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class SiteSettingsForm(forms.ModelForm):
    """Edit contact info + social links + site identity."""
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'dash-input'}),
            'tagline': forms.TextInput(attrs={'class': 'dash-input'}),
            'email': forms.EmailInput(attrs={'class': 'dash-input'}),
            'phone_primary': forms.TextInput(attrs={'class': 'dash-input'}),
            'phone_secondary': forms.TextInput(attrs={'class': 'dash-input'}),
            'location': forms.TextInput(attrs={'class': 'dash-input'}),
            'working_hours': forms.TextInput(attrs={'class': 'dash-input'}),
            'instagram_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://instagram.com/...',
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://linkedin.com/in/...',
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://facebook.com/...',
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://twitter.com/...',
            }),
            'whatsapp_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://wa.me/234...',
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://github.com/...',
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://youtube.com/...',
            }),
            'tiktok_url': forms.URLInput(attrs={
                'class': 'dash-input',
                'placeholder': 'https://tiktok.com/@...',
            }),
            'about_summary': forms.Textarea(attrs={'class': 'dash-input', 'rows': 3}),
        }


class CVProfileForm(forms.ModelForm):
    """Edit CV page header info."""
    class Meta:
        model = CVProfile
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'dash-input'}),
            'job_title': forms.TextInput(attrs={'class': 'dash-input'}),
            'email': forms.EmailInput(attrs={'class': 'dash-input'}),
            'phone_primary': forms.TextInput(attrs={'class': 'dash-input'}),
            'phone_secondary': forms.TextInput(attrs={'class': 'dash-input'}),
            'location': forms.TextInput(attrs={'class': 'dash-input'}),
            'website': forms.TextInput(attrs={'class': 'dash-input'}),
            'summary': forms.Textarea(attrs={'class': 'dash-input', 'rows': 4}),
            'photo': forms.ClearableFileInput(attrs={'class': 'dash-input'}),
            'cv_file': forms.ClearableFileInput(attrs={'class': 'dash-input'}),
        }


class CVEducationForm(forms.ModelForm):
    """Add or edit a CV education entry."""
    class Meta:
        model = CVEducation
        fields = '__all__'
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'University of Lagos',
            }),
            'degree': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'B.Sc. Computer Science',
            }),
            'start_year': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': '2014',
            }),
            'end_year': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': '2018 (or leave blank for Present)',
            }),
            'description': forms.Textarea(attrs={'class': 'dash-input', 'rows': 2}),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class CVExperienceForm(forms.ModelForm):
    """Add or edit a CV experience entry."""
    class Meta:
        model = CVExperience
        fields = '__all__'
        widgets = {
            'company': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'MOLA TECH',
            }),
            'role': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Founder & Lead Developer',
            }),
            'start_date': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Jan 2020',
            }),
            'end_date': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Present (or leave blank)',
            }),
            'description': forms.Textarea(attrs={
                'class': 'dash-input',
                'rows': 5,
                'placeholder': (
                    'Developed responsive websites for 50+ clients.\n'
                    'Managed cloud migration projects.\n'
                    'Mentored junior developers.'
                ),
            }),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class CVSkillForm(forms.ModelForm):
    """Add or edit a CV skill."""
    class Meta:
        model = CVSkill
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Web Development',
            }),
            'level': forms.Select(attrs={'class': 'dash-input'}),
            'category': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Programming, Design...',
            }),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class CVLanguageForm(forms.ModelForm):
    """Add or edit a CV language."""
    class Meta:
        model = CVLanguage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'English',
            }),
            'level': forms.Select(attrs={'class': 'dash-input'}),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }


class CVCertificationForm(forms.ModelForm):
    """Add or edit a CV certification."""
    class Meta:
        model = CVCertification
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Google Cloud Certified',
            }),
            'issuer': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': 'Google',
            }),
            'year': forms.TextInput(attrs={
                'class': 'dash-input',
                'placeholder': '2023',
            }),
            'display_order': forms.NumberInput(attrs={'class': 'dash-input'}),
        }