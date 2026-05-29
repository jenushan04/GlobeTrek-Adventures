"""Core views — home, about, contact, error handlers."""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from apps.tours.models import TourPackage, Destination
from apps.inquiries.forms import InquiryForm


def home(request):
    """Home page — hero banner + featured tours + testimonials."""
    featured_packages = TourPackage.objects.filter(
        is_active=True
    ).select_related('destination', 'category').order_by('-rating', '-created_at')[:6]

    featured_destinations = Destination.objects.filter(featured=True)[:4]

    context = {
        'featured_packages': featured_packages,
        'featured_destinations': featured_destinations,
    }
    return render(request, 'home.html', context)


def about(request):
    """About Us — company profile."""
    return render(request, 'about.html')


@require_http_methods(["GET", "POST"])
def contact(request):
    """Contact page — submits an Inquiry for staff to reply to."""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            # If logged in, associate inquiry with that user
            if request.user.is_authenticated:
                inquiry.customer = request.user
            inquiry.save()
            messages.success(
                request,
                'Thank you for contacting GlobeTrek Adventures! '
                'Our team will get back to you shortly.'
            )
            return redirect('core:contact')
    else:
        # Pre-fill subject if logged in (for nicer UX)
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = request.user.get_full_name() or request.user.username
            initial['email'] = request.user.email
        form = InquiryForm(initial=initial)

    return render(request, 'contact.html', {'form': form})


# ============== Error Handlers ==============
def handler404(request, exception=None):
    """Custom 404 page."""
    return render(request, '404.html', status=404)


def handler500(request):
    """Custom 500 page."""
    return render(request, '500.html', status=500)


def handler403(request, exception=None):
    """Custom 403 page."""
    return render(request, '403.html', status=403)
