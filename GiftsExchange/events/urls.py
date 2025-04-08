from django.urls import path
from . import views

app_name='events'

urlpatterns=[
    path('create/',views.create_event_view,name='create_event_view'),
    path('send_email/',views.event_update_email,name='event_update_email'),
    path('my_events/',views.user_events_view,name='user_events_view'),
    path('participations/',views.current_user_participations_view,name='current_user_participations_view'),
    path('event_management/',views.event_management_view,name='event_management_view'),
    path('event_management/<event_id>/update_participant/',views.update_participant_view,name='update_participant_view'),   
    path('event_management/registration/<int:event_id>/',views.event_registration_view, name='event_registration_view'),
    path('event_management/validate/<event_id>/',views.validate_event_view,name='validate_event_view'),
    path('event_management/update/<event_id>/',views.update_event_view,name='update_event_view'),
    path('event_management/cancelation/<event_id>/',views.event_cancelation_view,name='event_cancelation_view'),
]
