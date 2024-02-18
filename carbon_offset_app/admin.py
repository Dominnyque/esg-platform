from django.contrib import admin
from .models import Event

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'country', 'city']
    search_fields = ['name', 'country', 'city']
    list_filter = ['start_date', 'end_date', 'country', 'city']