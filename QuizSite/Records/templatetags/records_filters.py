from django import template
# from django.utils.html import format_html

from Records.models import *

register = template.Library()

# render all individuals with their
