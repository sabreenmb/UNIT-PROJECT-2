from django.urls import path
from . import views

app_name='events'

urlpatterns=[
    path('create/',views.create_event_view,name='create_event_view'),
    path('my_events/',views.user_events_view,name='user_events_view'),
    path('participations/',views.current_user_participations_view,name='current_user_participations_view'),
    path('participations/event-<event_id>',views.participant_area_view,name='participant_area_view'),
    path('participant_area/event-<event_id>',views.temp_participant_area_view,name='temp_participant_area_view'),
    path('event_management/',views.event_management_view,name='event_management_view'),
    path('event_management/registration/<int:event_id>/',views.event_registration_view, name='event_registration_view'),
    path('event_management/share/<int:event_id>/',views.share_link_view, name='share_link_view'),
    path('event_management/validate/<event_id>/',views.validate_event_view,name='validate_event_view'),
    path('event_management/update/<event_id>/',views.update_event_view,name='update_event_view'),
    path('event_management/draw_names/<event_id>/',views.draw_participants_view,name='draw_participants_view'),
    path('event_management/cancelation/<event_id>/',views.event_cancelation_view,name='event_cancelation_view'),
]
