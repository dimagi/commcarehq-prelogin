from django.utils import translation
import codecs
import os
import markdown
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from corehq.apps.style.decorators import use_bootstrap3

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
        kwargs['language_options'] = self.language_options()
        return super(BasePreloginView, self).get_context_data(**kwargs)

    @use_bootstrap3
    def dispatch(self, request, *args, **kwargs):
        return super(BasePreloginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        lang_prefix = kwargs.get('lang_code')
        if lang_prefix and lang_prefix not in prelogin_lang_codes():
            return HttpResponseRedirect(reverse(self.urlname))
        self.activate_language_from_request(request, lang_prefix)
        return super(BasePreloginView, self).get(request, *args, **kwargs)

    def activate_language_from_request(self, request, lang_prefix):
        if lang_prefix in prelogin_lang_codes():
            lang = lang_prefix
        else:
            lang = translation.get_language_from_request(request)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        request.session['django_language'] = lang
        translation.activate(lang)

    def language_options(self):
        options = []
        for lang_code, display_label in PRELOGIN_LANGUAGES:
            options.append({
                'display_label': display_label,
                'prefix_url': reverse(self.urlname, args=[lang_code])
            })
        return options


class HomePublicView(BasePreloginView):
    urlname = 'public_home'
    template_name = 'prelogin/home.html'

    def get_context_data(self, **kwargs):
        kwargs['is_home'] = True
        return super(HomePublicView, self).get_context_data(**kwargs)


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
