import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView

from .functions import send_email
from .models import Vessel, UserProfile

class RecaptchaMixin:
    subject = 'ZimTracker Request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['captcha_key'] = settings.RECAPTCHA_API_KEY
        return context

    def get_captcha_token(self, form=None):
        if form:
            if form.cleaned_data.get('recaptcha'):
                return form.cleaned_data.get('recaptcha')
        return self.request.POST.get('recaptcha')

    def is_captcha_valid(self, form=None):
        result = self.validate_captcha(
            self.get_captcha_token(form)
        )
        if result['success']:
            return True
        else:
            return False

    def validate_captcha(self, recaptcha_response):
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode())

class Home(RecaptchaMixin, View):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = {
            'vessel_list': Vessel.objects.all(),
            'captcha_key': settings.RECAPTCHA_API_KEY
        }
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
        if self.is_captcha_valid():
            email = send_email(
                to='sarrabi@gmail.com',
                subject='ZimTracker Request',
                content='{0} ({1} {2}): {3}'.format(
                    request.POST.get('name'),
                    request.POST.get('email'),
                    request.POST.get('phone'),
                    request.POST.get('location')
                )
            )
            messages.success(request, 
                'Request Received, Thank You!')
        else:
            messages.error(request, 
                'An error occurred. Please try again later')
        return render(request, self.template_name, context)

class VesselList(ListView):
    model = Vessel

class VesselDetail(DetailView):
    model = Vessel

    def get_context_data(self, **kwargs):
        vessel = self.get_object()
        context = super().get_context_data(**kwargs)
        context['GOOGLEMAPS_API_KEY'] = settings.GOOGLEMAPS_API_KEY
        return context