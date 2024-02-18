from django.urls import path
from .views import(ComingSoonView,
                   CarbonFootprintMeasurements,
                   OurWorkView,
                   FanCarbonFootprintMeasurementView,
                   AboutUsView,
                   OffsetView,
                   ProjectView,
                   CareerView,
                   FAQView
)


urlpatterns = [
    path('', ComingSoonView.as_view(), name = 'coming_soon'),
    path('carbon-footprint-measurements/', CarbonFootprintMeasurements.as_view(), name='carbon-footprint-measurements'),
    path('our-work/', OurWorkView.as_view(), name='our-work'),
    path('carbon-footprint-measurements-fans/', FanCarbonFootprintMeasurementView.as_view(), name='carbon-footprint-fans'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
    path('offset/', OffsetView.as_view(), name='offset'),
    path('projects/', ProjectView.as_view(), name='projects'),
    path('career/', CareerView.as_view(), name='career'),
    path('faq/', FAQView.as_view(), name='faq'),
    # path('<pk>/', lead_details, name = 'lead-details'),
    # path('<pk>/update', lead_update, name = 'update-lead'),
    # path('<pk>/delete', lead_delete, name = 'delete-lead'),
]