from django.conf.urls import patterns, url
from court import views

urlpatterns = patterns('',
    url(r'^exts$', views.check_extensions),
    url(r'^exts/delete-all$', views.ext_delete_all),

    url(r'^$', views.list),
    url(r'^(?P<uuid>[-a-z\d]+)$', views.court),
    url(r'^public/(?P<slug>[-a-z\d]+)$', views.public),
)
