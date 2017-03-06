from __future__ import absolute_import
import re
from django.conf import settings
from django.http import Http404
from django.utils import translation
from django.utils.translation import ugettext as _
import codecs
import os
import markdown
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from corehq.apps.hqwebapp.utils import aliased_language_name
from corehq.apps.style.decorators import use_angular_js


MAIN_FORM = 'main'
SUPPLY_FORM = 'supply'

HUBSPOT_PORTAL_IDS = {
    MAIN_FORM: '503070',
    SUPPLY_FORM: '503070',
}

HUBSPOT_FORM_IDS = {
    MAIN_FORM: '4e28b3a0-1268-42f2-8d58-6a34b05ed08a',
    SUPPLY_FORM: '6ac30a6d-2ab9-4ad2-8c67-2da973535b4f',
}

DEFAULT_LANG = settings.LANGUAGE_CODE
PRELOGIN_LANGUAGES = (
    ('en', 'English'),
    ('fra', 'French'),
)


def public_default(request):
    return HttpResponseRedirect(reverse(HomePublicView.urlname))


class BasePreloginView(TemplateView):
    hubspot_portal_id = HUBSPOT_PORTAL_IDS[MAIN_FORM]
    hubspot_form_id = HUBSPOT_FORM_IDS[MAIN_FORM]

    def get_context_data(self, **kwargs):
        kwargs['hubspot'] = {
            'portal_id': self.hubspot_portal_id,
            'form_id': self.hubspot_form_id,
        }
        kwargs.update(self.i18n_context())
        return super(BasePreloginView, self).get_context_data(**kwargs)

    @use_angular_js
    def dispatch(self, request, *args, **kwargs):
        return super(BasePreloginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        def drop_regiondialect(lang_code):
            """
            Drop the "-us" in "en-us"
            """
            return re.sub(r'(\w+)[_-]\w+', r'\1', lang_code) if lang_code else lang_code

        lang_prefix = drop_regiondialect(kwargs.get('lang_code'))
        # handle prefix URLs
        if lang_prefix:
            if lang_prefix in prelogin_lang_codes():
                # activate translation if known lang
                translation.activate(lang_prefix)
            else:
                # 404 on unknown langs
                raise Http404()
        # handle non-prefix URLs
        else:
            # guess user_lang from browser or logged-in user language setting and
            # try to redirect prefixed URL for that lang
            user_lang = drop_regiondialect(translation.get_language_from_request(request))
            if user_lang in prelogin_lang_codes() and not is_default_lang_code(user_lang):
                return HttpResponseRedirect(reverse(self.urlname, args=[user_lang]))
            # fall back to english always
            translation.activate(DEFAULT_LANG)

        return super(BasePreloginView, self).get(request, *args, **kwargs)

    def i18n_context(self):
        localized_options = []
        for lang_code, display_label in PRELOGIN_LANGUAGES:
            with translation.override(lang_code):
                localized_options.append({
                    'display_label': _(display_label),
                    'prefix_url': reverse(self.urlname, args=[lang_code])
                })

        return {
            'language_options': localized_options,
            'current_lang_name': _(aliased_language_name(translation.get_language())),
            'url_uses_prefix': bool(self.kwargs.get('lang_code', False))
        }


class HomePublicView(BasePreloginView):
    urlname = 'public_home'
    template_name = 'prelogin/home.html'

    def get_context_data(self, **kwargs):
        kwargs['is_home'] = True
        return super(HomePublicView, self).get_context_data(**kwargs)


class DemoFormCTA(BasePreloginView):
    urlname = 'public_demo_cta'
    template_name = 'prelogin/demo_cta.html'

    def get_context_data(self, **kwargs):
        kwargs['is_demo_cta'] = True
        return super(DemoFormCTA, self).get_context_data(**kwargs)


class ImpactPublicView(BasePreloginView):
    urlname = 'public_impact'
    template_name = 'prelogin/impact.html'

    def get_context_data(self, **kwargs):
        pub_col1 = os.path.join(
            os.path.dirname(__file__), '_resources/publications_col1.md'
        )
        with codecs.open(pub_col1, mode="r", encoding="utf-8") as f:
            kwargs['pub_first_col'] = mark_safe(markdown.markdown(f.read()))

        pub_col2 = os.path.join(
            os.path.dirname(__file__), '_resources/publications_col2.md'
        )
        with codecs.open(pub_col2, mode="r", encoding="utf-8") as f:
            kwargs['pub_second_col'] = mark_safe(markdown.markdown(f.read()))

        kwargs['is_impact'] = True

        return super(ImpactPublicView, self).get_context_data(**kwargs)


class SoftwareServicesPublicView(BasePreloginView):
    urlname = 'public_software_services'
    template_name = 'prelogin/software_services.html'

    def get_context_data(self, **kwargs):
        kwargs['is_software_services'] = True
        return super(SoftwareServicesPublicView, self).get_context_data(**kwargs)


class PricingPublicView(BasePreloginView):
    urlname = 'public_pricing'
    template_name = 'prelogin/pricing.html'

    def get_context_data(self, **kwargs):
        kwargs['is_software_services'] = True
        return super(PricingPublicView, self).get_context_data(**kwargs)


class ServicesPublicView(BasePreloginView):
    urlname = 'public_services'
    template_name = 'prelogin/services.html'

    def get_context_data(self, **kwargs):
        kwargs['is_software_services'] = True
        return super(ServicesPublicView, self).get_context_data(**kwargs)


class SolutionsPublicView(BasePreloginView):
    urlname = 'public_solutions'
    template_name = 'prelogin/solutions.html'
    hubspot_portal_id = HUBSPOT_PORTAL_IDS[SUPPLY_FORM]
    hubspot_form_id = HUBSPOT_FORM_IDS[SUPPLY_FORM]

    def get_context_data(self, **kwargs):
        kwargs['is_solutions'] = True
        return super(SolutionsPublicView, self).get_context_data(**kwargs)


def prelogin_lang_codes():
    return [code for code, name in PRELOGIN_LANGUAGES]


def is_default_lang_code(lang_code):
    # DEFAULT_LANG (en-us) is alias of 'en'
    return lang_code in [DEFAULT_LANG, 'en']
