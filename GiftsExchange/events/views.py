from django.shortcuts import render,redirect
from django.http import HttpRequest ,HttpResponse
# Create your views here.
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Event, EventParticipant,PlaceholderParticipant
from django.contrib.auth.models import User 

def create_event_view(request:HttpRequest):
    if request.method == 'POST':
        user= request.user
        new_event= Event(event_organizer=user,event_title=request.POST['event_title'],event_date=request.POST['event_date'],event_description=request.POST['event_description'] ,event_min_budget =request.POST['event_min_budget'],event_max_budget=request.POST['event_max_budget'])
        new_event.save()

        # Initialize a participant counter
        participant_count = 0
        participants = []

        # Loop through dynamically created participant fields
        while True:
            participant_name = request.POST.get(f'participant_name_{participant_count + 1}')
            participant_email = request.POST.get(f'participant_email_{participant_count + 1}')
            print(f'email {participant_email}')
            if participant_name and participant_email:
                # If both fields are present, it means this participant should be processed
                try:
                    existing_user = User.objects.get(email__iexact=participant_email)
                    print(existing_user)
                    # Create a Participant entry if the user exists
                    EventParticipant.objects.create(event=new_event, user=existing_user)
                except User.DoesNotExist:
                    # Create a PlaceholderParticipant if the user does not exist
                    PlaceholderParticipant.objects.create(event=new_event, name=participant_name, email=participant_email)
                
                participants.append({'name': participant_name, 'email': participant_email})
                participant_count += 1
            else:
                # If any field is not present, stop checking for more participants
                break

        # After processing all participants, redirect or render a response
        # add_participant(new_event.id, user.id)
        return redirect('events:user_events_view')
    
    return render(request, 'events/create_event.html')

def user_events_view(request:HttpRequest):
    user= request.user
    user_events=Event.objects.filter(event_organizer=user.id)
    print(user)
    print(user_events)
     
    return render(request, 'events/user_events.html' ,{"events":reversed(user_events)})


def event_management_view(request:HttpRequest):
    if request.GET['event_id']:
        current_event=Event.objects.get(pk=request.GET['event_id'])
        unconfirmed_participants=current_event.placeholder_participants.all()
        event_participants=current_event.participants.all()
    return render(request, 'events/event_management.html' ,{"event":current_event ,"participants":event_participants,'unconfirmed_participants':unconfirmed_participants})




def add_participant(event_id,user_id):
    event= Event.objects.get(pk=event_id)
    user=User.objects.get(pk=user_id)
    Participant =EventParticipant(event =event,user=user)
    Participant.save()

def event_update_email(request:HttpRequest):
    
    context = {
    "receiver_name": "Saium Khan",
    "age": 27,
    "profession": "Software Developer",
    "marital_status": "Divorced",
    "address": "Planet Earth",
    "year": 2023
    }


    content_html=render_to_string('main/mail/email.html' , context=context)
    # content_html="this is an email to confirm your registeration"
    send_to='sabreenbinsalman@hotmail.com'
    email_msg=EmailMessage('confirmation',content_html, settings.EMAIL_HOST_USER,[send_to])
    email_msg.content_subtype='html'
    email_msg.send()
    return redirect("main:home_view")


