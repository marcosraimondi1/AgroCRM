from django import template
from django.utils.html import format_html, mark_safe

register = template.Library()

# documentation on custom tags -> https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/


@register.simple_tag
def style(bill):
    if bill.daysleft() > 100 or bill.owed == 0:
        return "list-group-item-success"
    elif bill.daysleft() > 30:
        return "list-group-item-warning"
    else:
        return "list-group-item-danger"


@register.simple_tag()
def statusPill(bill):
    if bill.daysleft() > 100 or bill.owed == 0:
        span = '<span class="badge badge-pill" style="background-color: green;">No hurry</span>'
        return format_html("{}", mark_safe(span))

    elif bill.daysleft() > 30:
        span = '<span class="badge badge-pill" style="background-color: yellow; color: black;">Near deadline</span>'
        return format_html("{}", mark_safe(span))
    else:
        span = '<span class="badge badge-pill" style="background-color: red;">Pay Time!</span>'
        return format_html("{}", mark_safe(span))
