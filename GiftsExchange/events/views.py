from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.http import Http404, HttpRequest ,HttpResponse, JsonResponse
# Create your views here.
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Event, EventParticipant,PlaceholderParticipant
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect


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
            participant_email:str = request.POST.get(f'participant_email_{participant_count + 1}')
            if participant_name and participant_email:
                participant_email:str=participant_email.lower()

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
            if participant_name and participant_email:
                participant_email:str=participant_email.lower()

                existing_participant_emails.add(participant_email)  # Add email to the set of existing participants

                # Check if the participant exists in the database
                try:
                    existing_user = User.objects.get(email__iexact=participant_email)
                    print(existing_user)
                    # If exists, update the participant or create it if not already associated
                    EventParticipant.objects.get_or_create(event=current_event, user=existing_user)
                except User.DoesNotExist:
                    # Create a PlaceholderParticipant if the user does not exist
                    PlaceholderParticipant.objects.update_or_create(event=current_event, name=participant_name, email=participant_email)

                participant_count += 1
            else:
                break
        print("******************************")
        print(existing_participant_emails)

        # Remove participants that were not included in the POST data
        v=current_event.participants.exclude(user__email__in=existing_participant_emails)
        print(v)
        v.delete()
        x=current_event.placeholder_participants.exclude(email__in=existing_participant_emails)
        print(x)
        x.delete()
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
def current_user_participations_view(request:HttpRequest):
    
    if not request.user.is_authenticated:
        return render(request, 'events/events_participations.html')
    user= request.user
    events = Event.objects.filter(participants__user=user)
    event_exists = events.exists()  # This returns True or False

    return render(request, 'events/events_participations.html' ,{"events":reversed(events),'event_exists': event_exists})


def user_events_view(request:HttpRequest):
    user= request.user
    user_events=Event.objects.filter(event_organizer=user.id)
    event_exists = user_events.exists()  # This returns True or False

    return render(request, 'events/user_events.html' ,{"events":reversed(user_events) , 'event_exists': event_exists})


def event_management_view(request:HttpRequest):
    if request.GET['event_id']:
        try:
            current_event= get_object_or_404(Event, pk=request.GET['event_id'])
            unconfirmed_participants=current_event.placeholder_participants.all()
            event_participants=current_event.participants.all()
            # Generate the shareable link
            # Build the shareable link with next parameter
            shareable_link = (
                request.build_absolute_uri(
                    reverse('events:event_registration_view', args=[current_event.id])
                ) + '?next=' + request.build_absolute_uri(
                    reverse('events:event_registration_view', args=[current_event.id])
                )
            )
        except Exception:
            redirect()
    return render(request, 'events/event_management.html' ,{"event":current_event ,"participants":event_participants,'unconfirmed_participants':unconfirmed_participants, "shareable_link":shareable_link})

def validate_event_view(request:HttpRequest, event_id):
    if request.user.is_authenticated:
        try:
            event = get_object_or_404(Event, pk=event_id)
            shareable_link = (
                request.build_absolute_uri(
                    reverse('events:event_registration_view', args=[event_id])
                ) + '?next=' + request.build_absolute_uri(
                    reverse('events:event_registration_view', args=[event_id])
                )
            )
  
            participants_Placeholder=PlaceholderParticipant.objects.filter(event=event)
            participants=EventParticipant.objects.filter(event=event)
            emails:list=[]
            if participants.exists():
                print(participants)
                for participant in participants:
                    emails.append(participant.user.email)

            
            if participants.exists():
                print(participants)
                for participant in participants_Placeholder:
                    emails.append(participant.email)
            
            number=len(participants)+len(participants_Placeholder)
            if number <1:
                messages.error(request, 'cannot start an event with less than three participants, mak sure to invite or add participants then try to validate them again', 'alert-danger')
            else:
                invitation_email(emails,event,shareable_link)
                messages.success(request, 'the invitations were sent to the participants through the email', 'alert-success')


        except Exception as error:
            print('new wrror',error)
            messages.error(request, 'somthing went wrong please try again later', 'alert-danger')

        return redirect(f"{reverse('events:event_management_view')}?event_id={event_id}")



@login_required(login_url='accounts:sign_in_view')
def event_registration_view(request, event_id):
    try:
        event = get_object_or_404(Event, pk=event_id)
        user = request.user

        # Check if user is already registered as a participant
        is_participant = event.participants.filter(user=user).exists()
        # Check if user is already registered as a placeholder
        is_placeholder = event.placeholder_participants.filter(email=user.email).exists()

        if is_participant:
            messages.warning(request, f"You are already registered as a participant for {event.event_title}.", "alert-warning")
        elif is_placeholder:
            # Register the user as a participant
            event.placeholder_participants.filter(email=user.email).delete()
            EventParticipant.objects.create(user=user, event=event)
            messages.success(request, f"You have successfully registered for {event.event_title}!", "alert-success")
        else :
            EventParticipant.objects.create(user=user, event=event)
            messages.success(request, f"You have successfully registered for {event.event_title}!","alert-success")
    except IntegrityError:
        messages.error(request, "Failed to register you for the event. Please try again." ,"alert-danger")
    return redirect("main:home_view")

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

def draw_participants_view(request:HttpRequest, event_id):

    try:
        event = get_object_or_404(Event, id=event_id)
        # Check if drawing was done
        if  event.is_draw:
            messages.error(request,"This Event already draw", "alert-danger")
        
        else:
            if len(event.participants.all())<3:
                messages.error(request,"Not enough participants to draw!. at least invite 3 participants to start the draw", "alert-danger")
            else:
                event.draw_participants()  # Perform draw ensuring no self-selection
                messages.success(request,"the names has been drawn sucssefuly. and the participants notified throw the email", "alert-sucsses")

        # Get the drawn names
        # drawn_names = event.get_drawn_names()

    except Http404 as e:
        return redirect('main:error_view')
    except Exception as error:
        messages.error(request,"Could not draw names please try again later", "alert-danger")
    return redirect(f"{reverse('events:event_management_view')}?event_id={event_id}")

def event_cancelation_view(request:HttpRequest, event_id):
    try:
        event = get_object_or_404(Event, pk=event_id)
        event.delete()
        messages.success(request, f"Your event has been canceled successfully.","alert-success")
        return redirect('events:user_events_view')
    except Http404:
        return redirect('main:error_view')

def add_participant(event_id,user_id):
    event= Event.objects.get(pk=event_id)
    user=User.objects.get(pk=user_id)
    Participant =EventParticipant(event =event,user=user)
    Participant.save()

def invitation_email(emails:list, event:Event,shareable_link):
    context = {
        "event_name": event.event_title,
        "event_organizer": event.event_organizer,
        "event_date": event.event_date,
        "event_min_budget": event.event_min_budget,
        "event_max_budget": event.event_max_budget,
        "event_link":shareable_link
    }
    content_html=render_to_string('main/mail/Invitation_email.html' , context=context)
    # content_html="this is an email to confirm your registeration"
    # send_to='sabreenbinsalman@hotmail.com'
    email_msg=EmailMessage('Invitation',content_html, settings.EMAIL_HOST_USER,emails)
    email_msg.content_subtype='html'
    email_msg.send()
    return redirect("main:home_view")


