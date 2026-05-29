"""
Inquiry views:
- Public: create (anyone), my-inquiries (logged-in customer)
- Staff: list all, reply
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from apps.accounts.decorators import role_required
from .models import Inquiry
from .forms import InquiryForm, ReplyForm


# ============== Public/Customer Views ==============

def create_inquiry(request):
    """Standalone inquiry form (also reachable from contact page)."""
    # Pre-fill subject if passed via querystring (from tour detail "Ask a question")
    initial = {}
    if request.GET.get('subject'):
        initial['subject'] = request.GET['subject']

    if request.user.is_authenticated and not initial.get('name'):
        initial['name'] = request.user.get_full_name() or request.user.username
        initial['email'] = request.user.email

    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inq = form.save(commit=False)
            if request.user.is_authenticated:
                inq.customer = request.user
            inq.save()
            messages.success(
                request,
                'Your inquiry has been submitted! Our team will respond within 24 hours.',
            )
            if request.user.is_authenticated:
                return redirect('inquiries:my_list')
            return redirect('core:home')
    else:
        form = InquiryForm(initial=initial)

    return render(request, 'inquiries/create.html', {'form': form})


@login_required
def my_inquiries(request):
    """Customer's list of own inquiries with reply count."""
    inquiries = Inquiry.objects.filter(customer=request.user).prefetch_related('replies')
    return render(request, 'inquiries/my_list.html', {'inquiries': inquiries})


@login_required
def my_inquiry_detail(request, pk):
    """Customer views own inquiry with all replies."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    # Owner OR staff/admin only
    if inquiry.customer != request.user and not (
        hasattr(request.user, 'profile')
        and (request.user.profile.is_staff_role or request.user.profile.is_admin)
    ):
        return HttpResponseForbidden('You can only view your own inquiries.')

    return render(request, 'inquiries/my_detail.html', {'inquiry': inquiry})


# ============== Staff Views ==============

@role_required('staff', 'admin')
def manage_inquiries(request):
    """Staff list of all inquiries."""
    status_filter = request.GET.get('status', '')
    inquiries = Inquiry.objects.all().prefetch_related('replies')
    if status_filter:
        inquiries = inquiries.filter(status=status_filter)
    return render(request, 'inquiries/manage_list.html', {
        'inquiries': inquiries,
        'status_filter': status_filter,
    })


@role_required('staff', 'admin')
def reply_inquiry(request, pk):
    """Staff replies to an inquiry."""
    inquiry = get_object_or_404(Inquiry, pk=pk)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.inquiry = inquiry
            reply.staff = request.user
            reply.save()
            # Auto-flip status to in_progress
            if inquiry.status == 'open':
                inquiry.status = 'in_progress'
                inquiry.save()
            messages.success(request, 'Reply sent to the customer.')
            return redirect('inquiries:reply', pk=inquiry.pk)
    else:
        form = ReplyForm()

    return render(request, 'inquiries/reply.html', {
        'inquiry': inquiry, 'form': form,
    })


@role_required('staff', 'admin')
def resolve_inquiry(request, pk):
    """Mark an inquiry as resolved."""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if request.method == 'POST':
        inquiry.status = 'resolved'
        inquiry.save()
        messages.success(request, 'Inquiry marked as resolved.')
    return redirect('inquiries:manage_list')
