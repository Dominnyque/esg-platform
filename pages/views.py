from django.shortcuts import render
from django.views import generic

# Create your views here.
class CommingSoonView(generic.TemplateView):
    template_name = 'commingsoon.html'