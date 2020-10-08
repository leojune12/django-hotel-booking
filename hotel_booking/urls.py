from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('booking/search/', views.booking_search, name='booking-search'),
    path('booking/details/', views.booking_details, name='booking-details'),
    path('booking/confirm/', views.booking_confirm, name='booking-confirm'),
    path('booking/list/', views.booking_list_user, name='booking-list'),
    path('booking/cancel/', views.booking_cancel, name="booking-cancel")
]