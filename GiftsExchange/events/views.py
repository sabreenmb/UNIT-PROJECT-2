from django.shortcuts import render,redirect
from django.http import HttpRequest ,HttpResponse, JsonResponse
# Create your views here.
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Event, EventParticipant,PlaceholderParticipant
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt

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
from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventParticipant, PlaceholderParticipant, User

def update_event_view(request: HttpRequest, event_id):
    current_event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        user = request.user
        current_event.event_organizer = user
        current_event.event_title = request.POST['event_title']
        current_event.event_date = request.POST['event_date']
        current_event.event_description = request.POST['event_description']
        current_event.event_min_budget = request.POST['event_min_budget']
        current_event.event_max_budget = request.POST['event_max_budget']
        current_event.save()

        # Track participant changes
        existing_participant_emails = set()
        participant_count = 1
        
        # Loop through incoming participants
        while True:
            participant_name = request.POST.get(f'participant_name_{participant_count}')
            participant_email = request.POST.get(f'participant_email_{participant_count}')

            if not participant_name and not participant_email:
                break  # Stop if both fields are empty
            
            existing_participant_emails.add(participant_email)  # Add email to the set of existing participants
            
            # Check if the participant exists in the database
            try:
                existing_user = User.objects.get(email__iexact=participant_email)
                # If exists, update the participant or create it if not already associated
                EventParticipant.objects.get_or_create(event=current_event, user=existing_user)
            except User.DoesNotExist:
                # Create a PlaceholderParticipant if the user does not exist
                PlaceholderParticipant.objects.update_or_create(event=current_event, name=participant_name, email=participant_email)

            participant_count += 1

        # Remove participants that were not included in the POST data
        current_event.participants.exclude(user__email__in=existing_participant_emails).delete()
        current_event.placeholder_participants.exclude(email__in=existing_participant_emails).delete()
        return redirect(f"{reverse('events:event_management_view')}?event_id={event_id}")

    # Retrieve all participants
    registered_participants = [(part, 'registered') for part in current_event.participants.all()]  # Event Participants
    placeholder_participants = [(part, 'unregistered') for part in current_event.placeholder_participants.all()]  # Placeholder Participants
    
    all_participants = list(registered_participants) + list(placeholder_participants)

    return render(request, 'events/update_event.html', {
        "event": current_event,
        "all_participants": all_participants,
    })

# def update_event_view(request:HttpRequest,event_id):
#     current_event= Event.objects.get(pk=event_id)

#     if request.method == 'POST':
#         user= request.user
#         current_event.event_organizer=user
#         current_event.event_title=request.POST['event_title']
#         current_event.event_date=request.POST['event_date']
#         current_event.event_description=request.POST['event_description'] 
#         current_event.event_min_budget =request.POST['event_min_budget']
#         current_event.event_max_budget=request.POST['event_max_budget']
#         current_event.save()

#         participant_count = 0
#         participants = []
#         # Loop through dynamically created participant fields
#         while True:
#             participant_name = request.POST.get(f'participant_name_{participant_count + 1}')
#             participant_email = request.POST.get(f'participant_email_{participant_count + 1}')

#         #     print(f'email {participant_email}')
#         #     if participant_name and participant_email:
#         #         # If both fields are present, it means this participant should be processed
#         #         try:
#         #             existing_user = User.objects.get(email__iexact=participant_email)
#         #             print(existing_user)
#         #             # Create a Participant entry if the user exists
#         #             EventParticipant.objects.create(event=current_event, user=existing_user)
#         #         except User.DoesNotExist:
#         #             # Create a PlaceholderParticipant if the user does not exist
#         #             PlaceholderParticipant.objects.create(event=current_event, name=participant_name, email=participant_email)
                
#         #         participants.append({'name': participant_name, 'email': participant_email})
#         #         participant_count += 1
#         #     else:
#         #         # If any field is not present, stop checking for more participants
#         #         break

#         # After processing all participants, redirect or render a response
#         # add_participant(new_event.id, user.id)
#         return redirect('events:user_events_view')

#         # Initialize a participant counter

#     # Retrieve all participants and tag their type
#     participants = [(part, 'registered') for part in current_event.participants.all()]  # Event Participants
#     placeholder_participants = [(part, 'unregistered') for part in current_event.placeholder_participants.all()]  # Placeholder Participants
    
#     # Combine the two lists
#     all_participants = participants + placeholder_participants
#     print(all_participants)

    
#     return render(request, 'events/update_event.html', {"event":current_event ,"all_participants":all_participants})


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
        # Generate the shareable link
        shareable_link = request.build_absolute_uri(reverse('events:event_registration_view', args=[current_event.id]))
    return render(request, 'events/event_management.html' ,{"event":current_event ,"participants":event_participants,'unconfirmed_participants':unconfirmed_participants, "shareable_link":shareable_link})

def event_registration_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        # Process registration logic here
        # e.g., creating a participant instance
        # ...

        return redirect('events:event_management_view')  # Redirect after registration

    return render(request, 'events/register_event.html', {'event': event})

@csrf_exempt  # Use this decorator if you are not handling CSRF tokens for AJAX calls
def update_participant_view(request:HttpRequest,event_id):

    if request.method == 'POST':
        # Get data from the request
        participant_id = request.POST.get('id')
        participant_email = request.POST.get('email')
        print("-"*16)
        print(participant_id ,participant_email , event_id)
        try:
            current_event=Event.objects.get(pk=event_id)
            # Fetch the participant from the database

            participant=current_event.placeholder_participants.get(id=participant_id)

         
            # Update participant details
            participant.email = participant_email
            participant.save()  # Save changes

            return JsonResponse({'message': 'Participant updated successfully!'}, status=200)

        except PlaceholderParticipant.DoesNotExist:
            return JsonResponse({'error': 'Participant not found!'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method!'}, status=400)


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


