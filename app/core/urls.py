from django.conf.urls import patterns, url
from core.views import *

urlpatterns = patterns('',
                       url(r'^$', HomePageView.as_view(), name='core__homepage'),
                       url(r'^(?P<pk>[-\w]+)/$', AdsDetailView.as_view(), name='core__ads_detail'),
                       )
