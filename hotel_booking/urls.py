from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('search/', views.search_available_rooms, name='search'),
    path('booking-details/', views.book_guest, name='booking-details'),
    path('confirm-booking/', views.confirm_booking, name='confirm-booking'),
    path('my-bookings/', views.show_bookings, name='my-bookings'),
]