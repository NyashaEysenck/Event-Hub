from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('', views.superuser_dashboard, name='super_home'),
    path('manage-events/', views.manage_events, name='manage_events'),
    path('add-event/', views.add_event, name='add_event'),
    path('edit-event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('view_registrations/', views.view_registrations, name='view_registrations'),
    path('api/generate_suggestions/', views.generate_suggestions, name='generate_suggestions'),
]



 