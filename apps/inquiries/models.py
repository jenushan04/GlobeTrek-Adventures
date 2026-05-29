"""
Inquiries app models:
- Inquiry: customer's question/query
- InquiryReply: staff's response to an inquiry
"""
from django.db import models
from django.contrib.auth.models import User


class Inquiry(models.Model):
    """A customer query/question. Can be from a logged-in user or a guest (contact form)."""

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    # If logged in — link to the User. Otherwise just keep name/email.
    customer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='inquiries',
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='open')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Inquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} — {self.name}'


class InquiryReply(models.Model):
    """A staff reply to an inquiry."""
    inquiry = models.ForeignKey(
        Inquiry, on_delete=models.CASCADE, related_name='replies',
    )
    staff = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='inquiry_replies',
    )
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Inquiry Replies'
        ordering = ['created_at']

    def __str__(self):
        return f'Reply to {self.inquiry.subject}'
