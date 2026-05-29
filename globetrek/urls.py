"""
GlobeTrek Adventures URL Configuration
Top-level routing — delegates to each app's urls.py
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('tours/', include('apps.tours.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('inquiries/', include('apps.inquiries.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
]

# Serve media + static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
handler403 = 'apps.core.views.handler403'

# Django admin branding
admin.site.site_header = 'GlobeTrek Adventures Admin'
admin.site.site_title = 'GlobeTrek Admin'
admin.site.index_title = 'Travel Management System'
