from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_dashboard, name='home'),
    path('browse-events/', views.browse_events, name='browse_events'),
    path('event/<int:event_id>/', views.event_details, name='event_details'),
    path('my-registrations/', views.my_registrations, name='my_registrations'),
    path('cancel-registration/<int:registration_id>/', views.cancel_registration, name='cancel_registration'),
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),
    path('feedback/<int:event_id>/', views.provide_feedback, name='provide_feedback'),
]



 