"""Forms for inquiries."""
from django import forms
from .models import Inquiry, InquiryReply


class InquiryForm(forms.ModelForm):
    """Public/customer-facing contact form."""

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Tell us how we can help...',
            }),
            'name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'phone': forms.TextInput(attrs={'placeholder': '+94 77 xxx xxxx'}),
            'subject': forms.TextInput(attrs={'placeholder': 'What is your question about?'}),
        }


class ReplyForm(forms.ModelForm):
    """Staff form for replying to an inquiry."""

    class Meta:
        model = InquiryReply
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Type your reply to the customer...',
            }),
        }
