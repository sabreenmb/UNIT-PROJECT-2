from django.urls import path
from . import views

app_name='wishList'

urlpatterns=[
    path('event-<event_id>/', views.wishList_view, name='wishList_view'),
    path('item/<event_id>', views.save_item_view, name='save_item_view'),
    path('gifts/', views.gift_finder_view, name='gift_finder_view'),


]

