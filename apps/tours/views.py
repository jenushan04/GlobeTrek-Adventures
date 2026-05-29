"""
Tour views:
- Public: package list (with search/filter), package detail, destination list/detail
- Staff: package CRUD
"""
from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings

from apps.accounts.decorators import role_required
from .models import TourPackage, Destination, TourCategory, Review
from .forms import TourPackageForm, DestinationForm, ReviewForm


# ============== Public Views ==============

def package_list(request):
    """Browse tour packages with search + filter."""
    packages = TourPackage.objects.filter(is_active=True).select_related('destination', 'category')

    # Search by keyword
    q = request.GET.get('q', '').strip()
    if q:
        packages = packages.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(destination__name__icontains=q)
            | Q(destination__country__icontains=q)
        )

    # Filter by destination
    dest_id = request.GET.get('destination', '').strip()
    if dest_id.isdigit():
        packages = packages.filter(destination_id=int(dest_id))

    # Filter by category
    cat_id = request.GET.get('category', '').strip()
    if cat_id.isdigit():
        packages = packages.filter(category_id=int(cat_id))

    # Max price filter
    max_price = request.GET.get('max_price', '').strip()
    if max_price:
        try:
            packages = packages.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            pass

    # Duration filter (short / medium / long)
    duration = request.GET.get('duration', '').strip()
    if duration == 'short':
        packages = packages.filter(duration_days__lte=3)
    elif duration == 'medium':
        packages = packages.filter(duration_days__gte=4, duration_days__lte=7)
    elif duration == 'long':
        packages = packages.filter(duration_days__gte=8)

    # Sort
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        packages = packages.order_by('price')
    elif sort == 'price_high':
        packages = packages.order_by('-price')
    elif sort == 'rating':
        packages = packages.order_by('-rating')
    else:
        packages = packages.order_by('-created_at')

    # Pagination — 9 per page (as required)
    paginator = Paginator(packages, settings.PAGINATE_BY)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'destinations': Destination.objects.all(),
        'categories': TourCategory.objects.all(),
        'q': q,
        'selected_destination': dest_id,
        'selected_category': cat_id,
        'max_price': max_price,
        'duration': duration,
        'sort': sort,
        'total_results': paginator.count,
    }
    return render(request, 'tours/package_list.html', context)


def package_detail(request, slug):
    """Tour package detail page — itinerary, price, reviews, book button."""
    package = get_object_or_404(
        TourPackage.objects.select_related('destination', 'category'),
        slug=slug,
        is_active=True,
    )
    reviews = package.reviews.select_related('customer')[:10]
    related = TourPackage.objects.filter(
        destination=package.destination, is_active=True,
    ).exclude(id=package.id)[:3]

    return render(request, 'tours/package_detail.html', {
        'package': package,
        'reviews': reviews,
        'related': related,
    })


def destination_list(request):
    """Browse all destinations."""
    destinations = Destination.objects.all().order_by('country', 'name')
    return render(request, 'tours/destination_list.html', {
        'destinations': destinations,
    })


def destination_detail(request, pk):
    """Show packages for a specific destination."""
    destination = get_object_or_404(Destination, pk=pk)
    packages = destination.packages.filter(is_active=True)
    return render(request, 'tours/destination_detail.html', {
        'destination': destination,
        'packages': packages,
    })


# ============== Customer Review Submission ==============

@login_required
def submit_review(request, slug):
    """Customer submits a review for a tour package (must have a completed booking)."""
    package = get_object_or_404(TourPackage, slug=slug)

    # Check user has a completed booking for this package
    from apps.bookings.models import Booking
    has_booking = Booking.objects.filter(
        customer=request.user, package=package, status='completed',
    ).exists()

    if not has_booking:
        messages.warning(
            request,
            'You can only review tours you have completed.',
        )
        return redirect('tours:package_detail', slug=slug)

    # Already reviewed?
    if Review.objects.filter(customer=request.user, package=package).exists():
        messages.info(request, 'You have already reviewed this tour.')
        return redirect('tours:package_detail', slug=slug)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
            review.package = package
            review.save()
            messages.success(request, 'Thanks for your review!')
            return redirect('tours:package_detail', slug=slug)
    else:
        form = ReviewForm()

    return render(request, 'tours/submit_review.html', {
        'form': form,
        'package': package,
    })


# ============== Staff Views — Package CRUD ==============

@role_required('staff', 'admin')
def package_manage(request):
    """Staff list view — manage all packages."""
    packages = TourPackage.objects.all().select_related('destination', 'category')
    return render(request, 'tours/manage_list.html', {'packages': packages})


@role_required('staff', 'admin')
def package_create(request):
    """Create a new tour package."""
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)
        if form.is_valid():
            pkg = form.save()
            messages.success(request, f'Tour package "{pkg.title}" created successfully.')
            return redirect('tours:manage_list')
    else:
        form = TourPackageForm()
    return render(request, 'tours/manage_form.html', {
        'form': form, 'mode': 'Create',
    })


@role_required('staff', 'admin')
def package_edit(request, slug):
    """Edit an existing tour package."""
    pkg = get_object_or_404(TourPackage, slug=slug)
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=pkg)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{pkg.title}" updated successfully.')
            return redirect('tours:manage_list')
    else:
        form = TourPackageForm(instance=pkg)
    return render(request, 'tours/manage_form.html', {
        'form': form, 'mode': 'Edit', 'package': pkg,
    })


@role_required('staff', 'admin')
def package_delete(request, slug):
    """Delete a tour package (requires POST confirmation)."""
    pkg = get_object_or_404(TourPackage, slug=slug)
    if request.method == 'POST':
        title = pkg.title
        pkg.delete()
        messages.success(request, f'Tour package "{title}" deleted.')
        return redirect('tours:manage_list')
    return render(request, 'tours/manage_delete.html', {'package': pkg})
