from django.views.decorators.http import require_http_methods
from django.shortcuts import render


@require_http_methods(["GET"])
def home(request):
    return render(request, 'website/pages/home.html', {'request': request})
