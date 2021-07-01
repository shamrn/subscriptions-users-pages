from django.template import Library
from ..models import Pages,Contact

register = Library()

@register.simple_tag()
def get_pages():
    return Pages.objects.all()

@register.simple_tag()
def get_contact():
    return Contact.objects.get(pk=1)