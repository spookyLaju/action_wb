from . import views
from django.urls import path

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
  
    path('completed/', views.completed, name='completed')
  
]