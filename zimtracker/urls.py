from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('vessels', views.VesselList.as_view(), 
        name='vessel-list'),
]