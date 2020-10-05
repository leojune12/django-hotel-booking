from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from hotel_booking.forms import SignUpForm

from hotel_booking.models import Hotel, Booking, Room, RoomType, CardType

import json
from django.contrib.auth.decorators import login_required
from datetime import date
import string
import random

# Create your views here.

def index(request):
    hotel = Hotel.objects.get(id=1)
    return render(request, 'hotel_booking/home.html', {'hotel': hotel})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def search_available_rooms(request):
    # get hotel instance
    hotel = Hotel.objects.get(id=1)

    check_in_date = request.GET['check_in_date']
    check_out_date = request.GET['check_out_date']

    # get total number of nights
    number_of_nights = date(int(check_out_date.split("-")[0]), int(check_out_date.split("-")[1]), int(check_out_date.split("-")[2])) - date(int(check_in_date.split("-")[0]), int(check_in_date.split("-")[1]), int(check_in_date.split("-")[2]))

    # storage for id's of occupied rooms
    occupied_room_ids = []

    # get bookings within the range of chek-in and check-out dates
    active_bookings = Booking.objects.filter(check_in__range=(check_in_date, check_out_date)) | Booking.objects.filter(check_out__range=(check_in_date, check_out_date)).values()

    # get all rooms included in active_bookings
    for active_booking in active_bookings:
        for room in active_booking.rooms.all().values():
            occupied_room_ids.append(room['id'])

    # get all rooms excluding the occupied rooms
    available_rooms = Room.objects.all().exclude(pk__in=occupied_room_ids)

    # storage for room types of available rooms
    available_room_types = []

    # get room types of available rooms
    for room_type in RoomType.objects.all().values().order_by('-rate'):
        # add extra keys
        room_type['available_rooms'] = available_rooms.filter(room_type=room_type['id']).count()
        room_type['selected_rooms'] = 0
        available_room_types.append(room_type)

    return render(request, 'hotel_booking/check_rooms.html', {
        'hotel': hotel,
        'check_in': check_in_date,
        'check_out': check_out_date,
        'available_room_types': available_room_types,
        'number_of_nights': number_of_nights.days
    })

@login_required
def book_guest(request):
    hotel = Hotel.objects.get(id=1)
    check_in_date = request.POST['check_in_date']
    check_out_date = request.POST['check_out_date']
    room_type_ids = request.POST['room_type_ids']
    selected_room_type_counts = request.POST['selected_room_type_counts']

    card_types = CardType.objects.all().values()

    room_types = []

    index = 0
    for count in selected_room_type_counts.split(","):
        if int(count) > 0:
            type = RoomType.objects.filter(pk=room_type_ids.split(",")[index]).values()[0]
            type['selected_rooms'] = int(count)
            room_types.append(type)
        index += 1

    # get total number of nights
    number_of_nights = date(int(check_out_date.split("-")[0]), int(check_out_date.split("-")[1]), int(check_out_date.split("-")[2])) - date(int(check_in_date.split("-")[0]), int(check_in_date.split("-")[1]), int(check_in_date.split("-")[2]))

    return render(request, 'hotel_booking/booking_details.html', {
        'hotel': hotel,
        'check_in': check_in_date,
        'check_out': check_out_date,
        'number_of_nights': number_of_nights.days,
        'room_type_ids': room_type_ids.split(","),
        'selected_room_type_counts': selected_room_type_counts.split(","),
        'room_types': room_types,
        'card_types': card_types,
    })

@login_required
def bookings_list(request):
    # first_name = request.POST['first_name']
    # last_name = request.POST['last_name']
    # address = request.POST['address']
    # email = request.POST['email']
    # card_holder_name = request.POST['card_holder_name']
    # card_type = request.POST['card_type']
    # card_number = request.POST['card_number']
    # expiry_month = request.POST['expiry_month']
    # expiry_year = request.POST['expiry_year']
    # check_in = request.POST['check_in_date']
    # check_out = request.POST['check_out_date']
    # selected_room_types = request.POST['selected_room_types']
    #
    # reference_number = ''.join(random.choices(string.ascii_uppercase+string.digits, k=8))

    # booking = Booking.objects.create(
    #     user=request.user,
    #     reference_number=reference_number,
    #     booking_status_id=1,
    #     check_in=date()
    # )

    return render(request, 'hotel_booking/my_bookings.html', {
        # 'user': request.user,
        # 'reference_number': reference_number,
        # 'selected_room_types': selected_room_types[0]
    })
