from django.urls import path
from . import views

app_name = 'facilities'

urlpatterns = [
    path('', views.facility_list, name='list'),
    path('<slug:slug>/', views.facility_detail, name='detail'),
    path('<slug:slug>/virtual-tour/', views.virtual_tour_view, name='virtual_tour'),
]
