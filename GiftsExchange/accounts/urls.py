from django.urls import path
from . import views

app_name='accounts'

urlpatterns=[
    path('sign_in/', views.sign_in_view, name='sign_in_view'),
    path('sign_up/', views.sign_up_view, name='sign_up_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/<username>', views.user_profile_view, name='user_profile_view'),

]

