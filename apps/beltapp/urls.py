from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.addtrip),
    url(r'^processnewtrip$', views.processnewtrip),
    url(r'^jointrip$', views.join),
    url(r'^destination/(?P<id>\d+)$', views.destination),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout)
]
