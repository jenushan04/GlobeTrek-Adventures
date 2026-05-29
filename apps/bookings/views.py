"""
Booking views — create, list, customize, cancel, pay.
Staff views: list all bookings, confirm/cancel.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden

from apps.accounts.decorators import role_required
from apps.tours.models import TourPackage
from .models import Booking, Payment
from .forms import BookingForm, BookingCustomizeForm, PaymentForm


# ============== Customer Views ==============

@login_required
def create_booking(request, slug):
    """Customer initiates a booking for a tour package."""
    package = get_object_or_404(TourPackage, slug=slug, is_active=True)

    if request.method == 'POST':
        form = BookingForm(request.POST, package=package)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.package = package
            # Calculate total price = package price × num travellers
            booking.total_price = package.price * booking.num_travellers
            booking.save()
            messages.success(
                request,
                f'Booking #{booking.reference} created! '
                f'Please complete payment to confirm.',
            )
            return redirect('bookings:pay', booking_id=booking.id)
    else:
        form = BookingForm(package=package)

    return render(request, 'bookings/create.html', {
        'form': form,
        'package': package,
    })


@login_required
def booking_detail(request, booking_id):
    """Customer views one of their bookings."""
    booking = get_object_or_404(Booking, id=booking_id)

    # Owner check — staff/admin can view any
    if booking.customer != request.user and not (
        request.user.profile.is_staff_role or request.user.profile.is_admin
    ):
        return HttpResponseForbidden('You can only view your own bookings.')

    return render(request, 'bookings/detail.html', {'booking': booking})


@login_required
def customize_booking(request, booking_id):
    """Customer modifies date/travellers on a pending booking."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if booking.status not in ('pending', 'confirmed'):
        messages.warning(request, 'This booking cannot be modified anymore.')
        return redirect('bookings:detail', booking_id=booking.id)

    if request.method == 'POST':
        form = BookingCustomizeForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.total_price = booking.package.price * booking.num_travellers
            booking.save()
            messages.success(request, 'Booking updated successfully.')
            return redirect('bookings:detail', booking_id=booking.id)
    else:
        form = BookingCustomizeForm(instance=booking)

    return render(request, 'bookings/customize.html', {
        'form': form, 'booking': booking,
    })


@login_required
def cancel_booking(request, booking_id):
    """Customer cancels their own booking."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if not booking.can_cancel:
        messages.warning(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', booking_id=booking.id)

    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.info(
            request, f'Booking #{booking.reference} has been cancelled.',
        )
        return redirect('dashboard:customer')

    return render(request, 'bookings/cancel.html', {'booking': booking})


@login_required
def pay(request, booking_id):
    """Mock payment page."""
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)

    if booking.payment_status == 'paid':
        messages.info(request, 'This booking is already paid.')
        return redirect('bookings:detail', booking_id=booking.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Create the mock payment record
            Payment.objects.update_or_create(
                booking=booking,
                defaults={
                    'amount': booking.total_price,
                    'payment_method': form.cleaned_data['payment_method'],
                    'status': 'completed',
                    'paid_at': timezone.now(),
                },
            )
            booking.payment_status = 'paid'
            # Auto-confirm when payment received
            if booking.status == 'pending':
                booking.status = 'confirmed'
            booking.save()
            messages.success(
                request,
                f'Payment received! Booking #{booking.reference} is now confirmed.',
            )
            return redirect('bookings:receipt', booking_id=booking.id)
    else:
        form = PaymentForm()

    return render(request, 'bookings/pay.html', {
        'form': form, 'booking': booking,
    })


@login_required
def receipt(request, booking_id):
    """Post-payment receipt page."""
    booking = get_object_or_404(
        Booking, id=booking_id, customer=request.user,
    )
    return render(request, 'bookings/receipt.html', {'booking': booking})


# ============== Staff Views ==============

@role_required('staff', 'admin')
def manage_bookings(request):
    """Staff/admin list of all bookings."""
    status_filter = request.GET.get('status', '')
    bookings = Booking.objects.select_related('customer', 'package').all()
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'bookings/manage_list.html', {
        'bookings': bookings,
        'status_filter': status_filter,
    })


@role_required('staff', 'admin')
def confirm_booking(request, booking_id):
    """Staff confirms a pending booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()
        messages.success(
            request, f'Booking #{booking.reference} confirmed.',
        )
    return redirect('bookings:manage_list')


@role_required('staff', 'admin')
def staff_cancel_booking(request, booking_id):
    """Staff cancels a booking."""
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.info(
            request, f'Booking #{booking.reference} cancelled by staff.',
        )
    return redirect('bookings:manage_list')


@role_required('staff', 'admin')
def mark_completed(request, booking_id):
    """Staff marks a confirmed booking as completed (after the tour)."""
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.status = 'completed'
        booking.save()
        messages.success(
            request, f'Booking #{booking.reference} marked as completed.',
        )
    return redirect('bookings:manage_list')
