from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^homepage/$', views.homepage),
    url(r'^log_out/$', views.log_out),
    url(r'^add_quote/$', views.add_quote),
    url(r'^remove_favorite/(?P<id>\d*)/$', views.remove_favorite),
    url(r'^add_favorite/(?P<id>\d*)/$', views.add_favorite),
    url(r'^user/(?P<id>\d*)/$', views.user),
]
