from django.conf.urls import patterns, url
from django.views.generic import RedirectView
from corehq.apps.prelogin.views import *

root_patterns = patterns(
    'corehq.apps.prelogin.views',
    url(r'^home/$', HomePublicView.as_view(), name=HomePublicView.urlname),
    url(r'^impact/$', ImpactPublicView.as_view(), name=ImpactPublicView.urlname),
    url(r'^software_services/$', SoftwareServicesPublicView.as_view(),
        name=SoftwareServicesPublicView.urlname),
    url(r'^services/$', ServicesPublicView.as_view(),
        name=ServicesPublicView.urlname),
    url(r'^pricing/$', PricingPublicView.as_view(),
        name=PricingPublicView.urlname),
    url(r'^solutions/$', SolutionsPublicView.as_view(),
        name=SolutionsPublicView.urlname),
    url(r'^supply/$', RedirectView.as_view(url='/solutions/#supply', permanent=True)),
)

urlpatterns = root_patterns + patterns(
    'corehq.apps.prelogin.views',
    url(r'^lang/(?P<lang_code>[\w-]+)/home/$', HomePublicView.as_view(), name=HomePublicView.urlname),
    url(r'^lang/(?P<lang_code>[\w-]+)/impact/$', ImpactPublicView.as_view(), name=ImpactPublicView.urlname),
    url(r'^lang/(?P<lang_code>[\w-]+)/software_services/$', SoftwareServicesPublicView.as_view(),
        name=SoftwareServicesPublicView.urlname),
    url(r'^lang/(?P<lang_code>[\w-]+)/services/$', ServicesPublicView.as_view(),
        name=ServicesPublicView.urlname),
    url(r'^lang/(?P<lang_code>[\w-]+)/pricing/$', PricingPublicView.as_view(),
        name=PricingPublicView.urlname),
    url(r'^lang/(?P<lang_code>[\w-]+)/solutions/$', SolutionsPublicView.as_view(),
        name=SolutionsPublicView.urlname),
    url(r'^lang/(?P<lang_code>[\w-]+)/supply/$', RedirectView.as_view(url='/solutions/#supply', permanent=True)),
)
