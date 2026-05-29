from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    # Public
    path('', views.package_list, name='package_list'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('<slug:slug>/', views.package_detail, name='package_detail'),
    path('<slug:slug>/review/', views.submit_review, name='submit_review'),

    # Staff management
    path('manage/list/', views.package_manage, name='manage_list'),
    path('manage/create/', views.package_create, name='manage_create'),
    path('manage/<slug:slug>/edit/', views.package_edit, name='manage_edit'),
    path('manage/<slug:slug>/delete/', views.package_delete, name='manage_delete'),
]
