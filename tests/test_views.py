from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, SimpleTestCase
from django.utils import translation
from corehq.apps.prelogin.views import *


class TestViews(TestCase):
    def test_status_codes(self):
        for view in [
            HomePublicView,
            ImpactPublicView,
            PricingPublicView,
            ServicesPublicView,
            SoftwareServicesPublicView,
            SolutionsPublicView,
        ]:
            response = self.client.get(reverse(view.urlname), follow=False)
            self.assertEqual(response.status_code, 200)


class TestLanguagePrefixMixin(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.anon_user = AnonymousUser()

    def test_prefixed_pages_get_translated(self):
        import pdb; pdb.set_trace()
        for lang in ['en', 'fra']:
            prefixed_url = reverse(HomePublicView.urlname, args=[lang])
            prefix_mixin = LanguagePrefixMixin.from_url(prefixed_url)
            request = self.factory.get(prefixed_url)
            prefix_mixin.activate_language_from_request(request)
            self.assertEqual(translation.get_language(), lang)

    def test_unknown_lang_redirects(self):
        unknown_lang_url = reverse(HomePublicView.urlname, args=['random_lang'])
        response = self.client.get(unknown_lang_url, follow=False)
        # should redirect to same URL without prefix
        self.assertRedirects(
            response,
            reverse(HomePublicView.urlname),
            status_code=302,
            fetch_redirect_response=True,
            target_status_code=200
        )

    def test_root_url_is_in_default_language(self):
        import pdb; pdb.set_trace()
        root_url = reverse(HomePublicView.urlname)
        root_response = self.client.get(root_url, follow=False)
        self.assertEqual(root_response._headers['content-language'][1], settings.LANGUAGE_CODE)
