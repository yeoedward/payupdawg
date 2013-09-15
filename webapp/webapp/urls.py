from django.conf.urls import patterns, include, url
from receipts.views import *
from django.conf import settings
import os

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
  url(r'^admin/', include(admin.site.urls)),
 
  url(r'^/?$', goHome),

  # serve static
  (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': settings.STATIC_ROOT,
     'show_indexes': True}),

  (r'^login/?$', login),
  (r'^logout/?$', logout),
  (r'^register/?$', register),
  (r'^dashboard/?$', dashboard),
  (r'^receipts/?$', receipts),
)
