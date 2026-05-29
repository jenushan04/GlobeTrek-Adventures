"""
Dashboard views — one per role + a redirect that sends users to the right one.
Admin dashboard includes sales/customer reports backed by Chart.js.
"""
import json
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.utils import timezone

from apps.accounts.decorators import role_required
from apps.accounts.forms import StaffCreateForm
from apps.bookings.models import Booking, Payment
from apps.tours.models import TourPackage
from apps.inquiries.models import Inquiry


# ============== Role-aware redirect ==============

@login_required
def dashboard_redirect(request):
    """Send each user to the right dashboard based on their role."""
    if not hasattr(request.user, 'profile'):
        return redirect('core:home')

    role = request.user.profile.role
    if role == 'admin':
        return redirect('dashboard:admin')
    if role == 'staff':
        return redirect('dashboard:staff')
    return redirect('dashboard:customer')


# ============== Customer Dashboard ==============

@login_required
def customer_dashboard(request):
    """Customer's home screen — bookings overview + quick actions."""
    bookings = Booking.objects.filter(customer=request.user).select_related('package')
    inquiries = Inquiry.objects.filter(customer=request.user)

    stats = {
        'total_bookings': bookings.count(),
        'pending': bookings.filter(status='pending').count(),
        'confirmed': bookings.filter(status='confirmed').count(),
        'completed': bookings.filter(status='completed').count(),
        'inquiries_open': inquiries.exclude(status='resolved').count(),
    }

    return render(request, 'dashboard/customer.html', {
        'bookings': bookings[:10],
        'recent_inquiries': inquiries[:5],
        'stats': stats,
    })


# ============== Staff Dashboard ==============

@role_required('staff', 'admin')
def staff_dashboard(request):
    """Staff overview — pending bookings, open inquiries, packages count."""
    stats = {
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'open_inquiries': Inquiry.objects.exclude(status='resolved').count(),
        'active_packages': TourPackage.objects.filter(is_active=True).count(),
        'total_bookings': Booking.objects.count(),
    }

    recent_bookings = Booking.objects.select_related(
        'customer', 'package',
    ).order_by('-created_at')[:8]

    recent_inquiries = Inquiry.objects.filter(
        status__in=['open', 'in_progress'],
    ).order_by('-created_at')[:5]

    return render(request, 'dashboard/staff.html', {
        'stats': stats,
        'recent_bookings': recent_bookings,
        'recent_inquiries': recent_inquiries,
    })


# ============== Admin Dashboard ==============

@role_required('admin')
def admin_dashboard(request):
    """Admin overview — KPI cards + sales chart + top packages."""
    # Top-line KPI numbers
    total_revenue = Payment.objects.filter(
        status='completed',
    ).aggregate(total=Sum('amount'))['total'] or 0

    stats = {
        'total_customers': User.objects.filter(profile__role='customer').count(),
        'total_staff': User.objects.filter(profile__role='staff').count(),
        'total_bookings': Booking.objects.count(),
        'total_revenue': total_revenue,
        'active_packages': TourPackage.objects.filter(is_active=True).count(),
        'avg_rating': TourPackage.objects.aggregate(avg=Avg('rating'))['avg'] or 0,
    }

    # ============ Chart 1: Bookings per month (last 6 months) ============
    today = timezone.now().date()
    months = []
    bookings_per_month = []
    revenue_per_month = []
    for i in range(5, -1, -1):
        # Compute first day of month i-months-back
        month_start = (today.replace(day=1) - timedelta(days=i * 30)).replace(day=1)
        # Compute end of that month
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        label = month_start.strftime('%b %Y')

        booking_count = Booking.objects.filter(
            created_at__date__gte=month_start,
            created_at__date__lt=next_month,
        ).count()

        revenue = Payment.objects.filter(
            paid_at__date__gte=month_start,
            paid_at__date__lt=next_month,
            status='completed',
        ).aggregate(total=Sum('amount'))['total'] or 0

        months.append(label)
        bookings_per_month.append(booking_count)
        revenue_per_month.append(float(revenue))

    # ============ Chart 2: Top tour packages by bookings ============
    top_packages = TourPackage.objects.annotate(
        booking_count=Count('bookings'),
    ).order_by('-booking_count')[:5]

    top_pkg_labels = [p.title[:25] for p in top_packages]
    top_pkg_counts = [p.booking_count for p in top_packages]

    # ============ Recent customer registrations ============
    recent_customers = User.objects.filter(
        profile__role='customer',
    ).order_by('-date_joined')[:6]

    chart_data = {
        'months': months,
        'bookings_per_month': bookings_per_month,
        'revenue_per_month': revenue_per_month,
        'top_pkg_labels': top_pkg_labels,
        'top_pkg_counts': top_pkg_counts,
    }

    return render(request, 'dashboard/admin.html', {
        'stats': stats,
        'top_packages': top_packages,
        'recent_customers': recent_customers,
        'chart_data_json': json.dumps(chart_data),
    })


# ============== Admin: Staff Management ==============

@role_required('admin')
def manage_staff(request):
    """Admin view of all staff accounts."""
    staff_users = User.objects.filter(profile__role='staff').order_by('username')
    return render(request, 'dashboard/manage_staff.html', {
        'staff_users': staff_users,
    })


@role_required('admin')
def create_staff(request):
    """Admin creates a new staff account."""
    if request.method == 'POST':
        form = StaffCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                f'Staff account for {user.username} created successfully.',
            )
            return redirect('dashboard:manage_staff')
    else:
        form = StaffCreateForm()
    return render(request, 'dashboard/create_staff.html', {'form': form})


@role_required('admin')
def toggle_staff(request, user_id):
    """Activate or deactivate a staff user."""
    staff = get_object_or_404(User, pk=user_id, profile__role='staff')
    if request.method == 'POST':
        staff.is_active = not staff.is_active
        staff.save()
        state = 'activated' if staff.is_active else 'deactivated'
        messages.info(request, f'Staff member {staff.username} {state}.')
    return redirect('dashboard:manage_staff')
