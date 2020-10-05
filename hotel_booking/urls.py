from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('search/', views.search_available_rooms, name='search'),
    path('book/', views.book_guest, name='book'),
    path('my-bookings/', views.bookings_list, name='my-bookings'),
]