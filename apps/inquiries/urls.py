from django.urls import path
from . import views

app_name = 'inquiries'

urlpatterns = [
    # Customer
    path('new/', views.create_inquiry, name='create'),
    path('mine/', views.my_inquiries, name='my_list'),
    path('mine/<int:pk>/', views.my_inquiry_detail, name='my_detail'),

    # Staff
    path('manage/list/', views.manage_inquiries, name='manage_list'),
    path('manage/<int:pk>/reply/', views.reply_inquiry, name='reply'),
    path('manage/<int:pk>/resolve/', views.resolve_inquiry, name='resolve'),
]
