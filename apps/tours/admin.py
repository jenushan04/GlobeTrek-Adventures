from django.contrib import admin
from .models import Destination, TourCategory, TourPackage, Review


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'featured', 'created_at')
    list_filter = ('featured', 'country')
    search_fields = ('name', 'country')


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'category', 'price',
                    'duration_days', 'rating', 'is_active')
    list_filter = ('is_active', 'category', 'destination')
    search_fields = ('title', 'description', 'destination__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'is_active')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('customer', 'package', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('customer__username', 'package__title')
