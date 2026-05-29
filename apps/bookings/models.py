"""
Bookings app models:
- Booking: customer's reservation for a tour package
- Payment: payment record linked to a booking (mock payment only)
"""
import uuid
from django.db import models
from django.contrib.auth.models import User
from apps.tours.models import TourPackage


class Booking(models.Model):
    """A customer's booking for a tour package."""

    STATUS_CHOICES = [
        ('pending', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    # Unique booking reference shown to customers
    reference = models.CharField(max_length=12, unique=True, editable=False, blank=True)

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings',
    )
    package = models.ForeignKey(
        TourPackage, on_delete=models.PROTECT, related_name='bookings',
    )
    travel_date = models.DateField(help_text='Date the tour starts.')
    num_travellers = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, default='unpaid',
    )

    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Booking #{self.reference} — {self.customer.username}'

    def save(self, *args, **kwargs):
        if not self.reference:
            # Generate a short, readable booking reference: GT-ABC123
            self.reference = 'GT-' + uuid.uuid4().hex[:6].upper()
        super().save(*args, **kwargs)

    @property
    def can_cancel(self):
        """Customer may cancel only if not yet completed/cancelled."""
        return self.status in ('pending', 'confirmed')

    @property
    def can_review(self):
        return self.status == 'completed'


class Payment(models.Model):
    """A mock payment record — no real money flows."""

    METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
        ('paypal', 'PayPal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    # Mock transaction ID — generated on save
    transaction_id = models.CharField(max_length=40, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return f'Payment {self.transaction_id} — {self.booking.reference}'

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = 'TXN-' + uuid.uuid4().hex[:12].upper()
        super().save(*args, **kwargs)
