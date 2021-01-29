from django import template

register = template.Library()


@register.simple_tag
def is_auth(request):
    if request.user:
        if request.user.id and isinstance(request.user.id, int):
            return False
    return True
