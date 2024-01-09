from django.shortcuts import render, redirect
from django.views import generic

# Create your views here.
class HomePageView(generic.TemplateView):
    template_name = 'home_page.html'