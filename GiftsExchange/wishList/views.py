from django.shortcuts import get_object_or_404, render,redirect
from django.http import Http404, HttpRequest ,HttpResponse, JsonResponse
from wishList.models import Item
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
        return render(request, "wishList/wishlist.html",{'wishItems':wishItems, "event":current_event})

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


def gift_finder_view(request:HttpRequest):
    return render(request, 'wishList/gift_finder.html')

