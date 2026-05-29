"""
Accounts models — Profile extends the built-in User model with a role and
travel-specific fields (phone, address, profile picture).
"""
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    One-to-one extension of Django's User model.
    Adds the 'role' field that drives role-based access control across the site.
    """

    ROLE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='customer',
        help_text='Determines what dashboards and actions are available.',
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    # Convenience role-check helpers (used by templates and views)
    @property
    def is_customer(self):
        return self.role == 'customer'

    @property
    def is_staff_role(self):
        return self.role == 'staff'

    @property
    def is_admin(self):
        return self.role == 'admin'
