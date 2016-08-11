from django.test import TestCase
from corehq.apps.prelogin.views import *


class TestViews(TestCase):
    def test_status_codes(self):
        for view in [
            DemoPublicView,
            HomePublicView,
            ImpactPublicView,
            PricingPublicView,
            ServicesPublicView,
            SoftwareServicesPublicView,
            SolutionsPublicView,
        ]:
            response = self.client.get(reverse(view.urlname), follow=False)
            self.assertEqual(response.status_code, 200)
