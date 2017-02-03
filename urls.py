from __future__ import absolute_import
from django.conf.urls import url, include
from django.views.generic import RedirectView
from corehq.apps.prelogin.views import *

root_patterns = [
    url(r'^home/$', HomePublicView.as_view(), name=HomePublicView.urlname),
    url(r'^demo/$', DemoPublicView.as_view(), name=DemoPublicView.urlname),
    url(r'^impact/$', ImpactPublicView.as_view(), name=ImpactPublicView.urlname),
    url(r'^pricing/$', SoftwareServicesPublicView.as_view(),
        name=SoftwareServicesPublicView.urlname),
    url(r'^software_services/$', RedirectView.as_view(
        pattern_name=SoftwareServicesPublicView.urlname,
        permanent=True)),
    url(r'^services/$', ServicesPublicView.as_view(),
        name=ServicesPublicView.urlname),
    url(r'^software/$', PricingPublicView.as_view(),
        name=PricingPublicView.urlname),
    url(r'^solutions/$', SolutionsPublicView.as_view(),
        name=SolutionsPublicView.urlname),
    url(r'^supply/$', RedirectView.as_view(url='/solutions/#supply', permanent=True)),
]


urlpatterns = root_patterns + [
    url(r'^lang/(?P<lang_code>[\w-]+)/', include(root_patterns)),
]
