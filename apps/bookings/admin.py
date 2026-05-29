from django.contrib import admin
from .models import Booking, Payment


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('reference', 'customer', 'package', 'travel_date',
                    'num_travellers', 'total_price', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'travel_date')
    search_fields = ('reference', 'customer__username', 'package__title')
    readonly_fields = ('reference', 'created_at', 'updated_at')
    date_hierarchy = 'travel_date'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'booking', 'amount',
                    'payment_method', 'status', 'paid_at')
    list_filter = ('status', 'payment_method')
    search_fields = ('transaction_id', 'booking__reference')
    readonly_fields = ('transaction_id',)
