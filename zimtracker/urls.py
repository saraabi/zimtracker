from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('vessels/', include([
        path('', views.VesselList.as_view(), 
            name='vessel-list'),
        path('<pk>/', views.VesselDetail.as_view(),
            name='vessel-detail')
    ])),
    path('ports/', include([
        path('', views.PortList.as_view(), 
            name='port-list'),
    ])),
]