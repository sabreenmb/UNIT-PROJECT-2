from django.shortcuts import render,redirect
from django.http import HttpRequest ,HttpResponse
# Create your views here.
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .models import Event

def create_event_view(request:HttpRequest):
    if request.method == 'post':
        user= request.user
        new_event= Event(event_organizer=user,event_title='',event_date='',event_description='' ,event_min_budget ='',event_max_budget='')
    return render(request, 'events/create_event.html')

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


