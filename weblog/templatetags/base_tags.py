from django import template
from ..models import Category

register = template.Library()


@register.simple_tag
def title():
    return "django weblog"


@register.inclusion_tag('weblog/partials/navbar.html')
def navbar_cat():
    return {
        'category': Category.objects.filter(status=True)
    }