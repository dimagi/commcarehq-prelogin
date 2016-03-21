from django import template
from django.template.loader import render_to_string

register = template.Library()


class PricingInfo(object):
    """
    Helper object for representing the availability of something on each plan.
    """
    COMMUNITY = 0
    STANDARD = 1
    PRO = 2
    ADVANCED = 3
    ENTERPRISE = 4

    def __init__(self, level):
        self.level = level

    @staticmethod
    def level_from_plan_name(plan_name):
        lookup = {
            'community': PricingInfo.COMMUNITY,
            'standard': PricingInfo.STANDARD,
            'pro': PricingInfo.PRO,
            'advanced': PricingInfo.ADVANCED,
            'enterprise': PricingInfo.ENTERPRISE,
        }
        if plan_name not in lookup:
            raise ValueError('Plan name {} must be one of {}'.format(plan_name, ', '.join(lookup.keys())))
        return lookup[plan_name]

    @staticmethod
    def from_plan_name(plan_name):
        return PricingInfo(PricingInfo.level_from_plan_name(plan_name))

    # these properties return whether the plan includes features at that level
    @property
    def community(self):
        return self._check_level(self.COMMUNITY)

    @property
    def standard(self):
        return self._check_level(self.STANDARD)

    @property
    def pro(self):
        return self._check_level(self.PRO)

    @property
    def advanced(self):
        return self._check_level(self.ADVANCED)

    @property
    def enterprise(self):
        return self._check_level(self.ENTERPRISE)

    def _check_level(self, level_to_check):
        return self.level <= level_to_check


@register.simple_tag
def pricing_row_contents(feature_name, plan_name):
    return render_to_string(
        'prelogin/_sections/pricing/partials/pricing_row_contents.html',
        {
            'feature_name': feature_name,
            'pricing_info': PricingInfo.from_plan_name(plan_name)
        }
    )


@register.simple_tag
def class_for_availability(is_available):
    # used by the check marks tags
    return 'fa-check' if is_available else 'fa-minus'
