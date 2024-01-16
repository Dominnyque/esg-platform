from django.urls import path
from .views import CommingSoonView


urlpatterns = [
    path('', CommingSoonView.as_view(), name = 'coming_soon'),
    # path ('create/', lead_create, name = 'create-lead'),
    # path('<pk>/', lead_details, name = 'lead-details'),
    # path('<pk>/update', lead_update, name = 'update-lead'),
    # path('<pk>/delete', lead_delete, name = 'delete-lead'),
]