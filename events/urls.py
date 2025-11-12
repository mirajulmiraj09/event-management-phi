from django.urls import path
from events.views import create_event, delete_event, edit_event, organizer_dashboard,view_event,admin_dashboard,rsvp_event,rsvp_list,remove_rsvp,add_category,participant_dashboard,cancel_rsvp

urlpatterns = [
   path('admin-dashboard/',admin_dashboard,name='admin-dashboard'),
   path('organizer-dashboard/',organizer_dashboard,name='organizer-dashboard'),
   path('participant-dashboard/',participant_dashboard,name='participant-dashboard'),
   path('rsvp-event/<int:event_id>',rsvp_event,name='rsvp-event'),

   path("events/<int:event_id>/rsvps/", rsvp_list, name="rsvp-list"),
   path("events/<int:event_id>/rsvps/remove/<int:user_id>/",remove_rsvp, name="remove-rsvp"),
   path('cancel-rsvp/<int:event_id>/',cancel_rsvp, name='cancel-rsvp'),

   path('create-event/',create_event, name='create-event'),
   path('add-category/',add_category,name = 'add-category'),
   path('view-event/<int:id>', view_event, name='view-event'),
   path('edit-event/<int:id>/',edit_event, name='edit-event'),
   path('delete-event/<int:id>',delete_event, name='delete-event'),
]