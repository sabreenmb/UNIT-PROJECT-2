from django.urls import path
from . import views

app_name='wishList'

urlpatterns=[
    path('event-<event_id>/', views.wishList_view, name='wishList_view'),
    path('item/<event_id>', views.save_item_view, name='save_item_view'),
    path('item/<event_id>/<item_id>', views.remove_item_view, name='remove_item_view'),
    path('drawn_name/<event_id>/<drawn_user_id>', views.drawn_name_view, name='drawn_name_view'),
    path('gifts/<event_id>', views.gift_finder_view, name='gift_finder_view'),


]

