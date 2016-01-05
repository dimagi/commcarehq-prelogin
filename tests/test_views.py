from django.test import SimpleTestCase
from corehq.apps.prelogin.views import *


class TestViews(SimpleTestCase):
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


class TestLanguagePrefixes(SimpleTestCase):
    def test_prefixed_pages_get_translated(self):
        for lang in ['en', 'fra']:
            prefixed_url = reverse(HomePublicView.urlname, args=[lang])
            response = self.client.get(prefixed_url, follow=False)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response._headers['content-language'][1], lang)

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

    def test_root_url_is_always_english(self):
        french_url = reverse(HomePublicView.urlname, args=['fra'])
        root_url = reverse(HomePublicView.urlname)

        french_response = self.client.get(french_url, follow=False)
        self.assertEqual(french_response._headers['content-language'][1], 'fra')

        # root url should be back to english
        root_response = self.client.get(root_url, follow=False)
        self.assertEqual(root_response._headers['content-language'][1], 'en')
