from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('<int:pk>/', views.payment_detail, name='payment_detail'),
    path('create/', views.payment_create, name='payment_create'),
    path('<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('export/', views.export_payments_csv, name='export_payments_csv'),
]
