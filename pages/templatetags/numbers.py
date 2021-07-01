from django.template import Library, Node, Template
import re

register = Library()

def numbers(value):
    value = re.sub('[()+ -]', '', value)
    return value

register.filter(numbers)