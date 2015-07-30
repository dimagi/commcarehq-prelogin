import logging
from django import forms
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy, ugettext as _
from django.conf import settings

# Bootstrap 3 Crispy Forms
from crispy_forms import layout as cb3_layout
from crispy_forms import helper as cb3_helper
from crispy_forms import bootstrap as twbscrispy
from corehq.apps.style import crispy as hqcrispy
from corehq.apps.hqwebapp.tasks import send_html_email_async

logger = logging.getLogger(__name__)

SOLUTIONS_CONTACT_EMAIL = "commcare.supply@dimagi.com"


class ContactDimagiForm(forms.Form):
    first_name = forms.CharField(
        label=ugettext_lazy("First Name"),
        required=False,
    )
    last_name = forms.CharField(
        label=ugettext_lazy("Last Name"),
        required=False,
    )
    company = forms.CharField(
        label=ugettext_lazy("Company / Organization"),
        required=False,
    )
    email = forms.EmailField(
        label=ugettext_lazy("Email Address"),
        required=True,
    )
    phone_number = forms.CharField(
        label=ugettext_lazy("Phone Number"),
        required=False,
    )
    country = forms.CharField(
        label=ugettext_lazy("Country"),
        required=False,
    )
    details = forms.CharField(
        label=ugettext_lazy(
            "What is your interest in CommCare and "
            "any specific questions you have?"
        ),
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(ContactDimagiForm, self).__init__(*args, **kwargs)
        self.helper = cb3_helper.FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.layout = cb3_layout.Layout(
            hqcrispy.Field(
                'first_name',
                ng_model="contact.first_name",
            ),
            hqcrispy.Field(
                'last_name',
                ng_model="contact.last_name",
            ),
            hqcrispy.Field(
                'company',
                ng_model="contact.company",
            ),
            hqcrispy.Field(
                'email',
                type="email",
                required="",
                ng_model="contact.email",
            ),
            hqcrispy.Field(
                'phone_number',
                ng_model="contact.phone_number",
            ),
            hqcrispy.Field(
                'country',
                ng_model="contact.country",
            ),
            hqcrispy.Field(
                'details',
                ng_model="contact.details",
            ),
            twbscrispy.Div(
                cb3_layout.HTML("need yo email"),
                ng_if="showEmailError",
            ),
            hqcrispy.FormActions(
                twbscrispy.StrictButton(
                    _("Contact Dimagi"),
                    type='submit',
                    css_class='btn-primary',
                    ng_click="send_email(contact)",
                )
            )
        )

    def send_email(self, is_solutions_contact=False):
        try:
            params = {
                'contact_form': self,
            }
            html_content = render_to_string("prelogin/_email/contact_form_email.html", params)
            text_content = render_to_string("prelogin/_email/contact_form_email.txt", params)
            recipient = SOLUTIONS_CONTACT_EMAIL if is_solutions_contact else settings.CONTACT_EMAIL
            subject = "Contact Dimagi Request from prelogin"
            send_html_email_async.delay(
                subject, recipient, html_content, text_content=text_content,
                email_from=settings.DEFAULT_FROM_EMAIL)
        except Exception:
            logging.error("Couldn't send pre-login contact email. "
                          "Contact: %s" % self.cleaned_data['contact_email']
            )
