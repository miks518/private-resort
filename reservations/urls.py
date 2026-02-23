from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('my/', views.my_reservations, name='my_reservations'),
    path('check/<slug:facility_slug>/', views.check_availability, name='check_availability'),
    path('book/<slug:facility_slug>/', views.create_reservation, name='create'),
    path('<int:pk>/', views.reservation_detail, name='detail'),
    path('<int:pk>/cancel/', views.cancel_reservation, name='cancel'),
]
