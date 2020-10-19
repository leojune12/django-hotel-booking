from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('invalid-data-input/', views.invalid_data_input, name='invalid-data-input'),

    path('', views.index, name='index'),
    path('booking/search/', views.booking_search, name='booking-search'),
    path('booking/details/', views.booking_details, name='booking-details'),
    path('booking/create/', views.booking_create, name='booking-confirm'),
    path('booking/list/', views.booking_list, name='booking-list'),
    path('booking/cancel/', views.booking_cancel, name="booking-cancel"),

    path('admin/bookings/', views.booking_list_admin, name='admin-bookings'),
    path('admin/bookings/show/<int:booking_id>', views.booking_show, name='admin-bookings-show'),
    path('admin/bookings/show/<int:booking_id>/check-in', views.booking_show_check_in, name='admin-bookings-show-check-in'),
    path('admin/bookings/show/<int:booking_id>/check-out', views.booking_show_check_out, name='admin-bookings-show-check-out'),
    path('admin/bookings/show/<int:booking_id>/no-show', views.booking_show_no_show, name='admin-bookings-show-no-show'),

]