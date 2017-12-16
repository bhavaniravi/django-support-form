from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^support/', include('supportform.urls')),
)
