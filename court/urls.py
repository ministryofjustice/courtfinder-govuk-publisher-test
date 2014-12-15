from django.conf.urls import patterns, url
from court import views

urlpatterns = patterns('',
    url(r'^$', views.list),
    url(r'^(?P<uuid>[-a-z\d]+)$', views.court),
    url(r'^public/(?P<slug>[-a-z\d]+)$', views.public),
)
