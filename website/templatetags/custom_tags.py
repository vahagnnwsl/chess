from django import template

register = template.Library()
from decouple import config


@register.simple_tag
def socket_host():

    return config('SOCKET_HOST')
