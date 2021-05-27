from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.generic import View, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView

from .models import Vessel, UserProfile

class Home(View):
    template_name = 'home.html'

    def get(self, request, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = {
            'vessel_list': Vessel.objects.all(),
        }
        return context

class VesselList(ListView):
    model = Vessel

class VesselDetail(DetailView):
    model = Vessel

    def get_context_data(self, **kwargs):
        vessel = self.get_object()
        context = super().get_context_data(**kwargs)
        context['GOOGLEMAPS_API_KEY'] = settings.GOOGLEMAPS_API_KEY
        return context