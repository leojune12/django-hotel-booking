from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from hotel_booking.models import Hotel, Booking, BookingStatus, Room, RoomType, CardType, Payment, Card, PaymentStatus
from datetime import date
import random
import string


@override_settings(LOGIN_URL='/hotel-booking/login/')
class RoutesTest(TestCase):

    def setUp(self):
        # create hotel
        Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test Address",
        )

        # create users
        admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pw@12345')
        test_user1 = User.objects.create_user(username='testuser1', password='pw@12345')
        test_user2 = User.objects.create_user(username='testuser2', password='pw@12345')

    def test_home_page_for_anonymous(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_for_user(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_for_admin(self):
        username = 'admin'
        login = self.client.login(username=username, password='pw@12345')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.url, reverse('admin-bookings'))
        self.assertEqual(response.status_code, 302)

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_logout_redirect(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, '/hotel-booking/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')
        response = self.client.get(reverse('index'))

        # Check user is logged in
        user = response.context['user']
        self.assertEqual(str(user), username)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')
        response = self.client.get(reverse('index'))

        # Check user is logged in
        self.assertEqual(str(response.context['user']), username)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check user is logged out
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'AnonymousUser')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_login_from_booking_search_page_if_user_not_authenticated(self):
        response = self.client.get('/hotel-booking/booking/search/?check_in_date=2020-11-13&check_out_date=2020-11-14')
        # check the redirect url
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/booking/search/%3Fcheck_in_date%3D2020-11-13%26check_out_date%3D2020-11-14')

    def test_booking_search_page_if_user_is_not_admin_invalid_input(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')
        # check-in date == check-out date
        response1 = self.client.get('/hotel-booking/booking/search/?check_in_date=2020-11-13&check_out_date=2020-11-13')
        # check the redirect url
        self.assertRedirects(response1, reverse('invalid-data-input'))

    def test_booking_search_page_if_user_is_not_admin(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.get('/hotel-booking/booking/search/?check_in_date=2020-11-13&check_out_date=2020-11-14')
        # check the status code
        self.assertEqual(response.status_code, 200)

    def test_booking_search_page_if_user_is_admin(self):
        username = 'admin'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.get('/hotel-booking/booking/search/?check_in_date=2020-10-13&check_out_date=2020-10-14')
        # check the redirect url
        self.assertEqual(response.url, reverse('admin-bookings'))
        self.assertEqual(response.status_code, 302)

    def test_405_response_from_booking_details_if_accessed_through_get_method(self):
        response = self.client.get('/hotel-booking/booking/details/')
        # return method not allowed status code(405)
        self.assertEqual(response.status_code, 405)

    def test_redirect_to_login_from_booking_list_if_user_not_authenticated(self):
        response = self.client.get('/hotel-booking/booking/list/')
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/booking/list/')

    def test_continue_to_booking_list_if_user_is_not_admin(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, 200)

    def test_redirect_from_booking_list_to_admin_booking_if_user_is_admin(self):
        username = 'admin'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.get(reverse('booking-list'))
        # redirect if user is admin
        self.assertRedirects(response, reverse('admin-bookings'))
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_login_from_admin_bookings_if_user_is_not_authenticated(self):
        response = self.client.get('/hotel-booking/admin/bookings/')
        # check redirect url
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/admin/bookings/')
        self.assertEqual(response.status_code, 302)

    def test_403_response_from_admin_bookings_if_user_is_not_authorized(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.get('/hotel-booking/admin/bookings/')
        # return unauthorized status(403)
        self.assertEqual(response.status_code, 403)

    def test_continue_to_admin_bookings_if_user_is_authorized(self):
        username = 'admin'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.get('/hotel-booking/admin/bookings/')
        self.assertEqual(response.status_code, 200)


class ViewsTest(TestCase):

    def setUp(self):
        # create hotel
        Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test Address",
        )

        # create users
        admin = User.objects.create_superuser(username='admin', email='admin@test.com', password='pw@12345')
        test_user1 = User.objects.create_user(username='testuser1', password='pw@12345')
        test_user2 = User.objects.create_user(username='testuser2', password='pw@12345')

        # create room types
        RoomType.objects.bulk_create([
            RoomType(
                type='Single Room',
                description='With single bed',
                rate=2000
            ),
            RoomType(
                type='Twin Room',
                description='With two single beds',
                rate=4000
            ),
            RoomType(
                type='Queen Double Room',
                description='With queen size double bed',
                rate=4000
            ),
            RoomType(
                type='King Double Room',
                description='With king size double bed',
                rate=4500
            ),
        ])
        # create rooms
        Room.objects.bulk_create([
            Room(
                room_type=RoomType.objects.get(type='Single Room'),
                number=101
            ),
            Room(
                room_type=RoomType.objects.get(type='Single Room'),
                number=102
            ),
            Room(
                room_type=RoomType.objects.get(type='Single Room'),
                number=103
            ),
            Room(
                room_type=RoomType.objects.get(type='Twin Room'),
                number=104
            ),
            Room(
                room_type=RoomType.objects.get(type='Twin Room'),
                number=105
            ),
            Room(
                room_type=RoomType.objects.get(type='Twin Room'),
                number=106
            ),
            Room(
                room_type=RoomType.objects.get(type='Queen Double Room'),
                number=201
            ),
            Room(
                room_type=RoomType.objects.get(type='Queen Double Room'),
                number=202
            ),
            Room(
                room_type=RoomType.objects.get(type='Queen Double Room'),
                number=203
            ),
            Room(
                room_type=RoomType.objects.get(type='King Double Room'),
                number=204
            ),
            Room(
                room_type=RoomType.objects.get(type='King Double Room'),
                number=205
            ),
            Room(
                room_type=RoomType.objects.get(type='King Double Room'),
                number=206
            ),
        ])
        # create card_types
        CardType.objects.bulk_create([
            CardType(
                type='MasterCard'
            ),
            CardType(
                type='Visa'
            ),
            CardType(
                type='American Express'
            ),
        ]),
        # create payment status
        PaymentStatus.objects.bulk_create([
            PaymentStatus(
                status='Paid',
            ),
            PaymentStatus(
                status='Pending',
            ),
            PaymentStatus(
                status='Cancelled',
            ),
            PaymentStatus(
                status='No Show',
            ),
        ])
        # create booking status
        BookingStatus.objects.bulk_create([
            BookingStatus(
                status='Confirmed'
            ),
            BookingStatus(
                status='Cancelled'
            ),
            BookingStatus(
                status='Checked-in'
            ),
            BookingStatus(
                status='Checked-out'
            ),
            BookingStatus(
                status='No Show'
            ),
        ])

    def random_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def create_booking(self, username, booking_status, check_in, check_out, persons, room_number):
        check_in_date = date(int(check_in.split("-")[0]), int(check_in.split("-")[1]), int(check_in.split("-")[2]))
        check_out_date = date(int(check_out.split("-")[0]), int(check_out.split("-")[1]), int(check_out.split("-")[2]))

        number_of_nights = check_out_date - check_in_date

        # create booking
        booking = Booking.objects.create(
            user=User.objects.get(username=username),
            reference_number=self.random_number(),
            booking_status=BookingStatus.objects.get(status=booking_status),
            check_in=check_in_date,
            check_out=check_out_date,
            persons=persons,
        )
        # add room to booking
        booking.rooms.add(Room.objects.get(number=room_number))
        # create payment object
        payment = Payment.objects.create(
            transaction_number=self.random_number(),
            booking=booking,
            status_id=2,
            first_name=username,
            last_name=username,
            email='test@test.com',
            address='test address',
            amount=Room.objects.get(number=room_number).rate() * number_of_nights.days
        )
        # create card object
        card = Card.objects.create(
            payment=payment,
            type_id=1,
            holder=username,
            number='1234123412341234',
            expiry_date=date(2021, 1, 1)
        )

        return booking

    def test_booking_search(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        # create bookings
        # single room - NOT available
        self.create_booking(
            'testuser1',
            'Confirmed',
            '2020-11-10',
            '2020-11-11',
            1,
            101
        )
        # twin room - NOT available
        self.create_booking(
            'testuser1',
            'Checked-in',
            '2020-11-10',
            '2020-11-11',
            1,
            104
        )
        # queen double room - available
        self.create_booking(
            'testuser1',
            'Cancelled',
            '2020-11-10',
            '2020-11-11',
            1,
            201
        )
        # queen double room - available
        self.create_booking(
            'testuser1',
            'Checked-out',
            '2020-11-10',
            '2020-11-11',
            1,
            204
        )
        # king double room - available
        self.create_booking(
            'testuser1',
            'No Show',
            '2020-11-10',
            '2020-11-11',
            1,
            206
        )
        # make get request
        response = self.client.get('/hotel-booking/booking/search/?check_in_date=2020-11-10&check_out_date=2020-11-11')
        # number of nights
        self.assertEqual(response.context['number_of_nights'], 1)
        # available rooms for king double room
        self.assertEqual(response.context['available_room_types'][0]['available_rooms'], 3)
        # available rooms for twin double room
        self.assertEqual(response.context['available_room_types'][1]['available_rooms'], 2)
        # available rooms for queen double room
        self.assertEqual(response.context['available_room_types'][2]['available_rooms'], 3)
        # available rooms for single room
        self.assertEqual(response.context['available_room_types'][3]['available_rooms'], 2)

    def test_booking_details(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        response = self.client.post('/hotel-booking/booking/details/', {
            'check_in_date': '2020-11-10',
            'check_out_date': '2020-11-13',
            'room_type_ids': '1,3',
            'selected_room_type_counts': '1,1',
        })

        number_of_nights = response.context['number_of_nights']
        # check total number of nights
        self.assertEqual(number_of_nights, 3)

        room_types = response.context['selected_room_types']
        total_payment = 0
        for room_type in room_types:
            total_payment += room_type['rate'] * number_of_nights
        # check total payments
        self.assertEqual(total_payment, 18000)

    def test_booking_create(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        self.client.post('/hotel-booking/booking/create/', {
            'first_name': 'test',
            'last_name': 'test',
            'address': 'test address',
            'email': 'test@test.com',
            'card_holder_name': 'test test',
            'card_type': '1',
            'card_number': '1234123412341234',
            'expiry_month': '2',
            'expiry_year': '2021',
            'persons': 2,
            'check_in_date': '2020-11-10',
            'check_out_date': '2020-11-12',
            'room_type_ids': '1,2',
            'selected_room_type_counts': '1,1',
        })

        # check the returned array from booking_list page if it returns the booking
        response = self.client.get(reverse('booking-list'))

        # get first item
        booking = response.context['bookings_lists'][0]
        # check check-in date
        self.assertEqual(booking['check_in'], date(2020, 11, 10))
        # check check-out date
        self.assertEqual(booking['check_out'], date(2020, 11, 12))
        # check rooms included
        self.assertEqual(booking['rooms_included'], ['1 x Single Room', '1 x Twin Room'])
        # check booking status
        self.assertEqual(booking['booking_status'], 'Confirmed')
        # check total amount
        self.assertEqual(booking['total_amount'], 12000)

    def test_booking_list_for_user(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')

        # create bookings
        # single room - NOT available
        self.create_booking(
            'testuser1',
            'Confirmed',
            '2020-11-10',
            '2020-11-11',
            1,
            101
        )
        # twin room - NOT available
        self.create_booking(
            'testuser1',
            'Checked-in',
            '2020-11-10',
            '2020-11-11',
            1,
            104
        )
        # queen double room - available
        self.create_booking(
            'testuser1',
            'Cancelled',
            '2020-11-10',
            '2020-11-11',
            1,
            201
        )
        # queen double room - available
        self.create_booking(
            'testuser2',
            'Checked-out',
            '2020-11-10',
            '2020-11-11',
            1,
            204
        )
        # king double room - available
        self.create_booking(
            'testuser2',
            'No Show',
            '2020-11-10',
            '2020-11-11',
            1,
            206
        )
        response = self.client.get(reverse('booking-list'))
        # check if it returns logged-in user's bookings only
        self.assertEqual(len(response.context['bookings_lists']), 3)

    def test_booking_list_for_admin(self):
        username = 'admin'
        login = self.client.login(username=username, password='pw@12345')

        # create bookings
        # single room - NOT available
        self.create_booking(
            'testuser1',
            'Confirmed',
            '2020-11-10',
            '2020-11-11',
            1,
            101
        )
        # twin room - NOT available
        self.create_booking(
            'testuser1',
            'Checked-in',
            '2020-11-10',
            '2020-11-11',
            1,
            104
        )
        # queen double room - available
        self.create_booking(
            'testuser1',
            'Cancelled',
            '2020-11-10',
            '2020-11-11',
            1,
            201
        )
        # queen double room - available
        self.create_booking(
            'testuser2',
            'Checked-out',
            '2020-11-10',
            '2020-11-11',
            1,
            204
        )
        # king double room - available
        self.create_booking(
            'testuser2',
            'No Show',
            '2020-11-10',
            '2020-11-11',
            1,
            206
        )
        response = self.client.get(reverse('admin-bookings'))
        # check if it returns all bookings
        self.assertEqual(len(response.context['bookings_lists']), 5)

    def test_admin_booking_show(self):
        username = 'admin'
        login = self.client.login(username=username, password='pw@12345')

        # create bookings
        # single room - NOT available
        self.create_booking(
            'testuser1',
            'Confirmed',
            '2020-11-10',
            '2020-11-11',
            1,
            101
        )
        # twin room - NOT available
        test_booking = self.create_booking(
            'testuser1',
            'Checked-in',
            '2020-11-10',
            '2020-11-14',
            1,
            104
        )
        # queen double room - available
        self.create_booking(
            'testuser1',
            'Cancelled',
            '2020-11-10',
            '2020-11-11',
            1,
            201
        )
        # queen double room - available
        self.create_booking(
            'testuser2',
            'Checked-out',
            '2020-11-10',
            '2020-11-11',
            1,
            204
        )
        # king double room - available
        self.create_booking(
            'testuser2',
            'No Show',
            '2020-11-10',
            '2020-11-11',
            1,
            206
        )
        response = self.client.get(reverse('admin-bookings-show', args=[2]))
        # check length of stay
        self.assertEqual(response.context['nights_of_stay'], 4)
        # check rooms included
        self.assertEqual(response.context['room_type_counts'], ['1 x Twin Room'])
        # check reference number
        self.assertEqual(response.context['booking'].reference_number, test_booking.reference_number)
