from django.shortcuts import render
from django.views.generic.base import TemplateView


class PrivacyView(TemplateView):
    template_name = 'privacy.html'


class AgreementView(TemplateView):
    template_name = 'agreement.html'


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def error_view(request):
    return render(request, '500.html', status=500)

def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

def bad_request_view(request, exception):
    return render(request, '400.html', status=400)
