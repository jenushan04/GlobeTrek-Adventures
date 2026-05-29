from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Customer
    path('create/<slug:slug>/', views.create_booking, name='create'),
    path('<int:booking_id>/', views.booking_detail, name='detail'),
    path('<int:booking_id>/customize/', views.customize_booking, name='customize'),
    path('<int:booking_id>/cancel/', views.cancel_booking, name='cancel'),
    path('<int:booking_id>/pay/', views.pay, name='pay'),
    path('<int:booking_id>/receipt/', views.receipt, name='receipt'),

    # Staff
    path('manage/list/', views.manage_bookings, name='manage_list'),
    path('manage/<int:booking_id>/confirm/', views.confirm_booking, name='confirm'),
    path('manage/<int:booking_id>/cancel/', views.staff_cancel_booking, name='staff_cancel'),
    path('manage/<int:booking_id>/complete/', views.mark_completed, name='complete'),
]
