"""
Tours app models:
- Destination: a city/country (Maldives, Bali, Paris, etc.)
- TourCategory: type of tour (Adventure, Honeymoon, Cultural, Family)
- TourPackage: a complete tour with price, duration, dates
- Review: customer rating + comment on a completed tour
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Destination(models.Model):
    """A place travellers can visit. Tour packages belong to one destination."""
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=80)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    featured = models.BooleanField(
        default=False,
        help_text='Tick to show this destination on the homepage.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}, {self.country}'


class TourCategory(models.Model):
    """High-level grouping for tour types (Adventure, Cultural, Honeymoon, etc.)."""
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    icon = models.CharField(
        max_length=50,
        default='bi-suitcase',
        help_text='Bootstrap icon class (e.g. bi-heart, bi-mountain).',
    )

    class Meta:
        verbose_name_plural = 'Tour Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourPackage(models.Model):
    """A complete travel package — what customers book."""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='packages',
    )
    category = models.ForeignKey(
        TourCategory,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='packages',
    )
    description = models.TextField()
    duration_days = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Total number of days for this tour.',
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text='Price per person in LKR.',
    )
    max_travellers = models.PositiveIntegerField(default=10)
    includes = models.TextField(
        help_text='What is included (one item per line: flights, hotel, meals).',
    )
    excludes = models.TextField(
        blank=True,
        help_text='What is NOT included (visa fees, insurance, etc.)',
    )
    image = models.ImageField(upload_to='tours/', blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=1,
        default=4.5,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    available_from = models.DateField()
    available_to = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    @property
    def includes_list(self):
        """Return includes as a list of lines for easy template iteration."""
        return [line.strip() for line in self.includes.splitlines() if line.strip()]

    @property
    def excludes_list(self):
        return [line.strip() for line in self.excludes.splitlines() if line.strip()]

    @property
    def avg_review_rating(self):
        """Average rating from customer reviews — falls back to seeded rating."""
        avg = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else float(self.rating)


class Review(models.Model):
    """Customer review on a tour package."""
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    package = models.ForeignKey(
        TourPackage, on_delete=models.CASCADE, related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # One review per customer per package
        unique_together = ('customer', 'package')

    def __str__(self):
        return f'{self.customer.username} - {self.package.title} ({self.rating}/5)'
