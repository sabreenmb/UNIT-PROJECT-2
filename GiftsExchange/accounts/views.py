from django.shortcuts import render, redirect
from django.http import HttpRequest , HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login ,logout
from django.contrib import messages
from django.db import IntegrityError,transaction
from .models import Profile
# Create your views here.

def sign_up_view(request:HttpRequest):
    if request.method =='POST':
        try:
            with transaction.atomic():
                new_user=User.objects.create_user(username=request.POST['username'],password=request.POST['password'], email=request.POST['email'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                new_user.save()
                profile:Profile=Profile(user=new_user)
                profile.save()

            messages.success(request, "Registered User Successfuly","alert-success")
            return redirect('accounts:sign_in_view')
        
        except IntegrityError as e :
            messages.error(request, "Please try another username. This username already in use","alert-danger")
            print("error :",e)
        except Exception as e:
            messages.error(request, "Could not register the user. Please again later","alert-danger")
            print("error :",e)
    return render(request, 'accounts/signup.html')

def sign_in_view(request:HttpRequest):
    if request.method =='POST':
        try:
            #check user cradentials
            user=authenticate(request,username=request.POST['username'],password= request.POST['password'])
            if user :
                #login the user
                login(request,user)
                messages.success(request, "Logged in Successfuly","alert-success")
                return redirect('main:home_view')
            else:
                messages.error(request, "Please try again. Your credentials are wrong.","alert-danger")
        except Exception as e:
            print("error :",e)
            messages.error(request, "Could not login. Try again","alert-danger")

    return render(request, 'accounts/signin.html')



def logout_view(request:HttpRequest):
    logout(request)
    messages.success(request, "Logged Out Successfuly","alert-success")

    return redirect('main:home_view')


def user_profile_view(request:HttpRequest, username):
    try:
        user= User.objects.get(username=username)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()


    except Exception as e:
        print(e)
    return render(request,"accounts/profile.html")