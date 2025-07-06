from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
  
    path('completed/', views.completed, name='completed')
  
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])