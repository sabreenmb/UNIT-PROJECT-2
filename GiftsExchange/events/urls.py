from django.urls import path
from . import views

app_name='events'

urlpatterns=[
    path('create/',views.create_event_view,name='create_event_view'),
    path('send_email/',views.event_update_email,name='event_update_email'),
    path('my_events/',views.user_events_view,name='user_events_view'),
    path('event_management/',views.event_management_view,name='event_management_view')


]
