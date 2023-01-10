from django import template
from ..models import Category

register = template.Library()


@register.simple_tag
def title():
    return "django blog"


@register.inclusion_tag('blog/partials/navbar.html')
def navbar_cat():
    return {
        'category': Category.objects.filter(status=True)
    }