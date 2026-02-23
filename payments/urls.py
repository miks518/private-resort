from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<int:reservation_pk>/', views.initiate_payment, name='initiate'),
    path('<int:pk>/verify/', views.verify_payment, name='verify'),
    path('<int:pk>/success/', views.payment_success, name='success'),
    path('history/', views.payment_history, name='history'),
    path('webhook/', views.paymongo_webhook, name='webhook'),
]
