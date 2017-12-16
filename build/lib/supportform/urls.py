from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^$', views.form, name='supportform-form'),
    url(r'^success/$', views.success, name='supportform-success'),
]
