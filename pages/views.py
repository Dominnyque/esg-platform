from django.shortcuts import render
from django.views import generic
from django.contrib.auth.views import LoginView

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

class ComingSoonView(generic.TemplateView):
    template_name = 'commingsoon.html'

class HomePageView(generic.TemplateView):
    template_name = 'home_page.html'

class CarbonFootprintMeasurements(generic.TemplateView):
    template_name = 'pages/carbonfootprintmeasurement.html'

class FanCarbonFootprintMeasurementView(generic.TemplateView):
    template_name = 'pages/fan_arbonfootprint_measurements.html'

class OurWorkView(generic.TemplateView):
    template_name = 'pages/our_work.html'

class AboutUsView(generic.TemplateView):
    template_name = 'pages/about_us.html'

class OffsetView(generic.TemplateView):
    template_name = 'pages/offset.html'

class ProjectView(generic.TemplateView):
    template_name = 'pages/project.html'

class CareerView(generic.TemplateView):
    template_name = 'pages/career.html'
class FAQView(generic.TemplateView):
    template_name = 'pages/faq.html'

