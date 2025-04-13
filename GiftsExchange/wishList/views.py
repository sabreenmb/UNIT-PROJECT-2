from django.shortcuts import get_object_or_404, render,redirect
from django.http import Http404, HttpRequest ,HttpResponse, JsonResponse
from wishList.models import Gift, Item
from events.models import Event
# Create your views here.
def wishList_view(request:HttpRequest ,event_id):
    try:
        if request.user.is_authenticated:
            user= request.user
            print(user)
        current_event = get_object_or_404(Event, pk=event_id)
        print(current_event)

        event_participant= current_event.participants.filter(user=user).first()
        wishItems=event_participant.wishlist.all()
        
        print ("my wish list" , wishItems)
        gifts=Gift.objects.all()

        return render(request, "wishList/wishlist.html",{'wishItems':wishItems, "event":current_event , "gifts":gifts})

    except Exception as error:     
        print('error',error)
        return redirect('main:error_view')


def save_item_view(request:HttpRequest,event_id):
    if request.method=="POST":
        item = Item.objects.create(name=request.POST['gift_name'])
        item.save()
        if request.user.is_authenticated:
            user= request.user
            print(user)
            current_event = get_object_or_404(Event, pk=event_id)
            print(current_event)

            event_participant= current_event.participants.filter(user=user).first()
            event_participant.wishlist.add(item)
   

    return redirect("wishList:wishList_view", event_id=event_id)

def remove_item_view(request:HttpRequest , event_id , item_id):
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return redirect("wishList:wishList_view", event_id=event_id)


def gift_finder_view(request:HttpRequest, event_id):
    current_event = get_object_or_404(Event, pk=event_id)

    gifts=Gift.objects.all()
    return render(request, 'wishList/gift_finder.html',{ "event":current_event,"gifts":gifts})

def drawn_name_view(request:HttpResponse, event_id , drawn_user_id):
    try:
        if request.user.is_authenticated:
            current_event = get_object_or_404(Event, pk=event_id)

        drawn_participant= current_event.participants.filter(user=drawn_user_id).first()
        wishItems=drawn_participant.wishlist.all()
        
        return render(request, "wishList/drawn_name_list.html",{'drawn_participant':drawn_participant, "event":current_event})

    except Exception as error:     
        print('error',error)
        return redirect('main:error_view')
