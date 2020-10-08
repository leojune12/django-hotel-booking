from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from hotel_booking.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from hotel_booking.models import Hotel, Booking, BookingStatus, Room, RoomType, CardType, Payment, Card

import json
from datetime import date
from django.utils import timezone
from django.db.models import Q
import datetime
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
def booking_search(request):
    # get hotel instance
    hotel = Hotel.objects.get(id=1)

    check_in_date = request.GET['check_in_date']
    check_out_date = request.GET['check_out_date']

    # get total number of nights
    number_of_nights = date(int(check_out_date.split("-")[0]), int(check_out_date.split("-")[1]), int(check_out_date.split("-")[2])) - date(int(check_in_date.split("-")[0]), int(check_in_date.split("-")[1]), int(check_in_date.split("-")[2]))

    # storage for id's of occupied rooms
    occupied_room_ids = []

    # get bookings that are within the range of check-in and check-out dates AND booking status id is 1 or 3
    active_bookings = Booking.objects.filter((Q(check_in__range=(check_in_date, check_out_date)) | Q(check_out__range=(check_in_date, check_out_date))) & Q(booking_status_id__in=[1, 3]))

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

    return render(request, 'hotel_booking/booking_search.html', {
        'hotel': hotel,
        'check_in': check_in_date,
        'check_out': check_out_date,
        'available_room_types': available_room_types,
        'number_of_nights': number_of_nights.days
    })

@login_required
def booking_details(request):
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
            room_type = RoomType.objects.filter(pk=room_type_ids.split(",")[index]).values()[0]
            room_type['selected_rooms'] = int(count)
            room_types.append(room_type)
        index += 1

    # get total number of nights
    number_of_nights = date(int(check_out_date.split("-")[0]), int(check_out_date.split("-")[1]), int(check_out_date.split("-")[2])) - date(int(check_in_date.split("-")[0]), int(check_in_date.split("-")[1]), int(check_in_date.split("-")[2]))

    return render(request, 'hotel_booking/booking_details.html', {
        'hotel': hotel,
        'check_in': check_in_date,
        'check_out': check_out_date,
        'number_of_nights': number_of_nights.days,
        'room_types': room_types,
        'card_types': card_types,
    })

@login_required
def booking_confirm(request):
    # get all post data
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    address = request.POST['address']
    email = request.POST['email']
    card_holder_name = request.POST['card_holder_name']
    card_type = request.POST['card_type']
    card_number = request.POST['card_number']
    expiry_month = request.POST['expiry_month']
    expiry_year = request.POST['expiry_year']
    persons = request.POST['persons']
    check_in = request.POST['check_in_date']
    check_out = request.POST['check_out_date']
    number_of_nights = request.POST['number_of_nights']
    room_type_ids = request.POST['room_type_ids']
    selected_room_type_counts = request.POST['selected_room_type_counts']

    selected_room_types = []

    # get selected room types and add to list
    i = 0
    for id in room_type_ids.split(","):
        # get first item
        room_type = RoomType.objects.filter(pk=int(id)).values()[0]
        # add key and value
        room_type['selected_rooms_count'] = int(selected_room_type_counts.split(",")[i])
        selected_room_types.append(room_type)
        i += 1

    # calculate total payment
    total_payment = 0
    for room_type in selected_room_types:
        total_payment += room_type['rate'] * room_type['selected_rooms_count'] * int(number_of_nights)

    # generate 8 random characters
    reference_number = ''.join(random.choices(string.ascii_uppercase+string.digits, k=8))
    transaction_number = ''.join(random.choices(string.ascii_uppercase+string.digits, k=8))
    # convert string data to date instance
    check_in_date = date(int(check_in.split("-")[0]), int(check_in.split("-")[1]), int(check_in.split("-")[2]))
    check_out_date = date(int(check_out.split("-")[0]), int(check_out.split("-")[1]), int(check_out.split("-")[2]))

    # storage for id's of occupied rooms
    occupied_room_ids = []
    # storage for room id's to book
    rooms_to_book_ids = []
    # get bookings within the range of chek-in and check-out dates
    active_bookings = Booking.objects.filter(check_in__range=(check_in_date, check_out_date)) | Booking.objects.filter(
        check_out__range=(check_in_date, check_out_date)).values()

    # get all rooms included in active_bookings
    for active_booking in active_bookings:
        for room in active_booking.rooms.all().values():
            occupied_room_ids.append(room['id'])
    # set rooms to book
    for room_type in selected_room_types:
        selected_rooms_count = room_type['selected_rooms_count']
        # get rooms of this type
        all_rooms_for_type = Room.objects.filter(room_type_id=room_type['id'])
        # get rooms with id NOT found in occupied_rooms_id
        available_rooms_id_for_this_type = all_rooms_for_type.exclude(pk__in=occupied_room_ids).values('id')
        # book rooms only found in available_rooms_id_for_this_type
        for n in range(selected_rooms_count):
            rooms_to_book_ids.append(available_rooms_id_for_this_type[n])

    # create booking object
    booking = Booking.objects.create(
        user=request.user,
        reference_number=reference_number,
        booking_status_id=1,
        check_in=check_in_date,
        check_out=check_out_date,
        persons=persons,
        created_at=datetime.datetime.now()
    )

    # add rooms to booking
    for id in rooms_to_book_ids:
        booking.rooms.add(Room.objects.get(pk=id['id']))

    # create payment object
    payment = Payment.objects.create(
        transaction_number=transaction_number,
        booking=booking,
        status_id=2,
        first_name=first_name,
        last_name=last_name,
        email=email,
        address=address,
        amount=total_payment
    )
    # create card object
    card = Card.objects.create(
        payment=payment,
        type_id=int(card_type),
        holder=card_holder_name,
        number=card_number,
        expiry_date=date(int(expiry_year), int(expiry_month), 1)
    )

    # create session
    request.session['booking_message'] = "Booking created successfully"

    return redirect('booking-list')

def booking_list_user(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')

    # storage for list of bookings
    bookings_lists = []

    # convert each queryset to dictionary
    for booking in bookings:
        room_types = []
        room_counts = []
        room_type_counts = []

        for room in booking.rooms.all():
            if not room.room_type in room_types:
                room_types.append(room.room_type)
                room_counts.append(booking.rooms.all().filter(room_type=room.room_type).count())

        i = 0
        for type in room_types:
            room_type_counts.append(room_counts[i].__str__() + " x " + type.__str__())
            i += 1

        # create dictionary of booking
        booking_dictionary = {
            'id': booking.id,
            'reference_number': booking.reference_number,
            'check_in': booking.check_in.__str__(),
            'check_out': booking.check_out.__str__(),
            'persons': booking.persons,
            'created_at': booking.created_at,
            'rooms_included': room_type_counts,
            'booking_status': booking.booking_status,
            'booking_status_id': booking.booking_status_id,
            'total_amount': booking.payment.amount
        }
        # add dictionary to list of bookings
        bookings_lists.append(booking_dictionary)

    # if session exist
    if 'booking_message' in request.session:
        # store before deleting
        message = request.session['booking_message']
        del request.session['booking_message']

        return render(request, 'hotel_booking/booking_list_user.html', {
            'booking_message': message,
            'bookings': bookings,
            'bookings_lists': bookings_lists
        })
    else:
        return render(request, 'hotel_booking/booking_list_user.html', {
            'bookings': bookings,
            'bookings_lists': bookings_lists
        })

def booking_cancel(request):
    booking_id = request.POST['booking_id']

    # update object
    Booking.objects.filter(pk=booking_id).update(booking_status_id=2)

    # create session
    request.session['booking_message'] = "Booking cancelled successfully"

    return redirect('booking-list')
