from django.db import models
from django.utils.text import slugify
from django.urls import reverse


# ==========================================================
# CONTACT MESSAGES
# ==========================================================
class ContactMessage(models.Model):
    """
    Stores messages submitted via any contact form on the site
    (homepage, portfolio page, CV page).
    """
    name = models.CharField(max_length=120, help_text="Sender's full name")
    email = models.EmailField(help_text="Sender's email address")
    subject = models.CharField(max_length=200, help_text="Message subject")
    message = models.TextField(help_text="Message body")
    is_read = models.BooleanField(default=False, help_text="Mark as read once handled")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.name} — {self.subject}"


# ==========================================================
# PROJECTS (Portfolio items)
# ==========================================================
class Project(models.Model):
    """
    Portfolio project cards. Used on homepage, portfolio page, and CV page.
    """
    CATEGORY_CHOICES = [
        ('graphics', 'Graphics Design'),
        ('software', 'Software Development'),
        ('robotics', 'Robotics & AI'),
        ('web', 'Web Development'),
        ('hardware', 'Hardware'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='software')
    description = models.TextField(help_text="Short description shown on the card")
    client = models.CharField(max_length=150, blank=True, help_text="Optional client name")

    image = models.ImageField(
        upload_to='projects/',
        blank=True,
        null=True,
        help_text="Thumbnail or screenshot for the card",
    )
    icon = models.CharField(
        max_length=60,
        default='fas fa-palette',
        help_text="Font Awesome icon class (e.g. fas fa-code) — shown if no image",
    )
    technologies = models.CharField(
        max_length=250,
        blank=True,
        help_text="Comma-separated tech stack (e.g. React, Django, PostgreSQL)",
    )

    link = models.URLField(
        blank=True,
        help_text="External URL to live project / case study (optional)",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show on homepage featured projects grid",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from site without deleting",
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

    def save(self, *args, **kwargs):
        # Auto-generate unique slug from title
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('portfolio:portfolio') + f'#{self.slug}'

    @property
    def tech_list(self):
        """Return technologies as a clean list."""
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',') if t.strip()]


# ==========================================================
# TESTIMONIALS
# ==========================================================
class Testimonial(models.Model):
    """
    Client testimonials shown on homepage + portfolio page.
    """
    name = models.CharField(max_length=120, help_text="Client name")
    role = models.CharField(
        max_length=180,
        blank=True,
        help_text="Client role / company (e.g. CEO, XYZ Corp)",
    )
    message = models.TextField(help_text="Testimonial text")
    avatar = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True,
        help_text="Optional client photo",
    )
    rating = models.PositiveSmallIntegerField(
        default=5,
        choices=[(i, f"{i} ★") for i in range(1, 6)],
        help_text="Star rating (1-5)",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from site",
    )
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} — {self.role or 'Client'}"


# ==========================================================
# SERVICES (optional — makes the Services section DB-driven)
# ==========================================================
class Service(models.Model):
    """
    Services shown on homepage + CV services panel.
    """
    title = models.CharField(max_length=120)
    description = models.TextField(help_text="Short description")
    icon = models.CharField(
        max_length=60,
        default='fas fa-cog',
        help_text="Font Awesome icon class (e.g. fas fa-code)",
    )
    bullet_points = models.TextField(
        blank=True,
        help_text="Optional: one bullet per line (e.g. 'Logo Design\\nBranding')",
    )
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title

    @property
    def bullet_list(self):
        if not self.bullet_points:
            return []
        return [line.strip() for line in self.bullet_points.splitlines() if line.strip()]


# ==========================================================
# SITE SETTINGS (singleton — optional but useful)
# ==========================================================
class SiteSettings(models.Model):
    """
    Global site settings editable from admin.
    Only ONE row should exist — the admin enforces this.
    """
    site_name = models.CharField(max_length=120, default='MOLA TECH')
    tagline = models.CharField(max_length=200, default='Where Art Meets Code')

    email = models.EmailField(default='molatech6784@gmail.com')
    phone_primary = models.CharField(max_length=40, default='+234 902 255 6784')
    phone_secondary = models.CharField(max_length=40, blank=True, default='+234 913 138 8402')
    location = models.CharField(max_length=120, default='Nigeria')
    working_hours = models.CharField(max_length=120, default='Monday - Friday: 9:00 AM - 4:00 PM')

    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)

    about_summary = models.TextField(
        blank=True,
        help_text="Short company description shown in the footer/about"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Enforce singleton pattern — only one row
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ==========================================================
# HERO SECTION (homepage header — dashboard editable)
# ==========================================================
class Hero(models.Model):
    """
    Homepage hero section — badge, headline (4 parts with gradient
    highlights), paragraph, 3 CTA buttons, hero image.
    Singleton — only ONE row.
    """
    badge_text = models.CharField(
        max_length=100,
        default="Building Future Minds",
        help_text="Small chip text above the headline",
    )

    # Headline: 4 pieces — e.g. "Where Art Meets Code"
    # The two *_highlight fields get the gradient colour.
    headline_1 = models.CharField(max_length=80, default="Where")
    headline_highlight_1 = models.CharField(max_length=80, default="Art")
    headline_2 = models.CharField(max_length=80, default="Meets")
    headline_highlight_2 = models.CharField(max_length=80, default="Code")

    paragraph = models.TextField(
        default=(
            "MOLA TECH is a fusion of creativity and technology — where innovative "
            "thinkers craft stunning designs and write efficient code to simplify "
            "complex problems."
        )
    )

    # Primary CTA (main button)
    cta_primary_text = models.CharField(max_length=60, default="Explore Services")
    cta_primary_link = models.CharField(
        max_length=200, default="#services",
        help_text="Can be #anchor, /path/ or full URL",
    )

    # Secondary CTA
    cta_secondary_text = models.CharField(max_length=60, default="Get in Touch")
    cta_secondary_link = models.CharField(max_length=200, default="#contact")

    # Tertiary CTA (e.g. View CV)
    cta_tertiary_text = models.CharField(max_length=60, default="View CV")
    cta_tertiary_link = models.CharField(max_length=200, default="/cv/")

    hero_image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True,
        help_text="Profile photo or hero illustration (right column)",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ==========================================================
# HERO STAT COUNTERS (e.g. "50+ Projects, 30+ Clients")
# ==========================================================
class HeroStat(models.Model):
    """
    Animated number counters shown in the hero section.
    Example: label='Projects', value=50, suffix='+'
    """
    label = models.CharField(max_length=60, help_text="e.g. Projects, Clients, Years")
    value = models.PositiveIntegerField(default=0, help_text="Numeric target, e.g. 50")
    suffix = models.CharField(
        max_length=10, default="+", blank=True,
        help_text="Appended after the number (e.g. '+', 'K', '%')",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = "Hero Stat"
        verbose_name_plural = "Hero Stats"

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


# ==========================================================
# ABOUT SECTION (background / mission / vision)
# ==========================================================
class AboutSection(models.Model):
    """
    About section — three text blocks.  Singleton.
    """
    background_title = models.CharField(max_length=100, default="Our Background")
    background_text = models.TextField(
        default=(
            "MOLA TECH Company was founded on the belief that technology and design "
            "can come together to create something truly extraordinary. Our journey "
            "began with a passion for innovation and a desire to make a meaningful impact."
        )
    )

    mission_title = models.CharField(max_length=100, default="Our Mission")
    mission_text = models.TextField(
        default=(
            "Our mission is to harness the power of technology and design to deliver "
            "exceptional solutions that empower businesses and individuals. We strive "
            "to build long-lasting relationships, foster growth, and inspire positive change."
        )
    )

    vision_title = models.CharField(max_length=100, default="Our Vision")
    vision_text = models.TextField(
        default=(
            "A world transformed by technology and design where businesses and "
            "individuals are empowered by exceptional solutions — driven by the "
            "seamless integration of cutting-edge tech and innovative design."
        )
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section"

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ==========================================================
# CORE VALUES (About section value cards)
# ==========================================================
class CoreValue(models.Model):
    """
    The 5 value cards next to the About section
    (Innovation, Excellence, Integrity, Collaboration, Passion).
    """
    icon = models.CharField(
        max_length=60,
        default="fas fa-lightbulb",
        help_text="Font Awesome class e.g. fas fa-lightbulb",
    )
    title = models.CharField(max_length=60)
    description = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'title']
        verbose_name = "Core Value"
        verbose_name_plural = "Core Values"

    def __str__(self):
        return self.title


# ==========================================================
# CV PROFILE (CV page header — name, title, contact, summary)
# ==========================================================
class CVProfile(models.Model):
    """
    Header block on the CV page.  Singleton.
    """
    full_name = models.CharField(max_length=150, default="Lucky Matthew Obasanjo")
    job_title = models.CharField(
        max_length=150,
        default="Software Engineer & Founder of MOLA TECH",
    )
    email = models.EmailField(default="molatech6784@gmail.com")
    phone_primary = models.CharField(max_length=40, default="+234 902 255 6784")
    phone_secondary = models.CharField(
        max_length=40, blank=True, default="+234 913 138 8402",
    )
    location = models.CharField(max_length=100, default="Nigeria")
    website = models.CharField(
        max_length=200, blank=True, default="www.molatech.com",
        help_text="Displayed text — can be a URL or short label",
    )
    summary = models.TextField(
        default=(
            "MOLA TECH is a technology-driven brand providing modern software, "
            "web development, and digital solutions for businesses and individuals."
        )
    )
    photo = models.ImageField(
        upload_to='cv/', blank=True, null=True,
        help_text="Optional portrait photo",
    )
    cv_file = models.FileField(
        upload_to='cv/files/', blank=True, null=True,
        help_text="Optional PDF download of the CV",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "CV Profile"
        verbose_name_plural = "CV Profile"

    def __str__(self):
        return self.full_name

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


# ==========================================================
# CV EDUCATION
# ==========================================================
class CVEducation(models.Model):
    """
    Education entries on the CV page.
    """
    institution = models.CharField(max_length=150)
    degree = models.CharField(max_length=150)
    start_year = models.CharField(max_length=20, help_text="e.g. 2014")
    end_year = models.CharField(
        max_length=20, blank=True,
        help_text="Leave blank to show 'Present'",
    )
    description = models.TextField(
        blank=True,
        help_text="Optional extra line e.g. 'Graduated with First Class Honors'",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-start_year']
        verbose_name = "CV Education"
        verbose_name_plural = "CV Education"

    def __str__(self):
        return f"{self.degree} — {self.institution}"


# ==========================================================
# CV EXPERIENCE
# ==========================================================
class CVExperience(models.Model):
    """
    Work experience entries on the CV page.
    """
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    start_date = models.CharField(max_length=40, help_text="e.g. Jan 2020")
    end_date = models.CharField(
        max_length=40, blank=True,
        help_text="Leave blank to show 'Present'",
    )
    description = models.TextField(
        blank=True,
        help_text="One bullet point per line. Bullets (• or -) are optional.",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name = "CV Experience"
        verbose_name_plural = "CV Experience"

    def __str__(self):
        return f"{self.role} — {self.company}"

    @property
    def bullet_list(self):
        """Return description as a clean list of bullet strings."""
        if not self.description:
            return []
        return [
            line.strip().lstrip('•-').strip()
            for line in self.description.splitlines()
            if line.strip()
        ]


# ==========================================================
# CV SKILL
# ==========================================================
class CVSkill(models.Model):
    """
    Skills with percentage bars on the CV page.
    """
    LEVEL_CHOICES = [(i, f"{i}%") for i in range(0, 101, 5)]

    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField(
        default=80, choices=LEVEL_CHOICES,
        help_text="Skill proficiency percentage",
    )
    category = models.CharField(
        max_length=80, blank=True,
        help_text="Optional category e.g. 'Programming' or 'Design'",
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "CV Skill"
        verbose_name_plural = "CV Skills"

    def __str__(self):
        return f"{self.name} ({self.level}%)"


# ==========================================================
# CV LANGUAGE
# ==========================================================
class CVLanguage(models.Model):
    """
    Languages listed on the CV page.
    """
    LEVEL_CHOICES = [
        ('native', 'Native'),
        ('fluent', 'Fluent'),
        ('intermediate', 'Intermediate'),
        ('basic', 'Basic'),
    ]

    name = models.CharField(max_length=80)
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default='fluent',
    )
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = "CV Language"
        verbose_name_plural = "CV Languages"

    def __str__(self):
        return f"{self.name} — {self.get_level_display()}"


# ==========================================================
# CV CERTIFICATION
# ==========================================================
class CVCertification(models.Model):
    """
    Certifications listed on the CV page.
    """
    name = models.CharField(max_length=200)
    issuer = models.CharField(
        max_length=150, blank=True,
        help_text="e.g. Google, AWS, Microsoft",
    )
    year = models.CharField(max_length=10, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', '-year']
        verbose_name = "CV Certification"
        verbose_name_plural = "CV Certifications"

    def __str__(self):
        return self.name