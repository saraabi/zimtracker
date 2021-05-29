from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView

from .functions import send_email
from .models import Vessel, UserProfile


class Home(View):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = {
            'vessel_list': Vessel.objects.all(),
        }
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_context_data()
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