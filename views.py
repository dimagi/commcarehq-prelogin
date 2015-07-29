import codecs
import os
from django.utils.decorators import method_decorator
import markdown
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from djangular.views.mixins import allow_remote_invocation, JSONResponseMixin
from corehq.apps.prelogin.forms import ContactDimagiForm
from corehq.apps.style.decorators import use_bootstrap3


def public_default(request):
    return HttpResponseRedirect(reverse(HomePublicView.urlname))


class BasePreloginView(JSONResponseMixin, TemplateView):
    """Have the contact dimagi form logic present always, as pretty much
    every page needs access to it.
    """
    is_solutions_contact = False

    @method_decorator(use_bootstrap3())
    def dispatch(self, request, *args, **kwargs):
        return super(BasePreloginView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['contact_form'] = ContactDimagiForm()
        return super(BasePreloginView, self).get_context_data(**kwargs)

    @allow_remote_invocation
    def send_email(self, in_data):
        contact_form = ContactDimagiForm(in_data)
        if contact_form.is_valid():
            contact_form.send_email(is_solutions_contact=self.is_solutions_contact)
            return {'success': True}
        else:
            return {'success': False, 'errors': contact_form.errors}


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


class ServicesPublicView(BasePreloginView):
    urlname = 'public_services'
    template_name = 'prelogin/services.html'

    def get_context_data(self, **kwargs):
        kwargs['is_services'] = True
        return super(ServicesPublicView, self).get_context_data(**kwargs)


class PricingPublicView(BasePreloginView):
    urlname = 'public_pricing'
    template_name = 'prelogin/pricing.html'

    def get_context_data(self, **kwargs):
        kwargs['is_pricing'] = True
        return super(PricingPublicView, self).get_context_data(**kwargs)


class ServicesDetailsPublicView(BasePreloginView):
    urlname = 'public_services_details'
    template_name = 'prelogin/services_details.html'

    def get_context_data(self, **kwargs):
        kwargs['is_services'] = True
        return super(ServicesDetailsPublicView, self).get_context_data(**kwargs)


class SolutionsPublicView(BasePreloginView):
    urlname = 'public_solutions'
    template_name = 'prelogin/solutions.html'
    is_solutions_contact = True

    def get_context_data(self, **kwargs):
        kwargs['is_solutions'] = True
        return super(SolutionsPublicView, self).get_context_data(**kwargs)

