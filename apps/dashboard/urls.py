from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_redirect, name='redirect'),
    path('customer/', views.customer_dashboard, name='customer'),
    path('staff/', views.staff_dashboard, name='staff'),
    path('admin/', views.admin_dashboard, name='admin'),

    # Admin staff management
    path('admin/staff/', views.manage_staff, name='manage_staff'),
    path('admin/staff/new/', views.create_staff, name='create_staff'),
    path('admin/staff/<int:user_id>/toggle/', views.toggle_staff, name='toggle_staff'),
]
