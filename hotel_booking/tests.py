from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase, override_settings, Client
import unittest

from django.urls import reverse

from hotel_booking.models import Hotel
from django.contrib.auth.models import User

@override_settings(LOGIN_URL='/hotel-booking/login/')
class AuthenticationTestCaseClass(TestCase):

    def setUp(self):
        # create hotel
        Hotel.objects.create(
            name="Test Hotel",
            description="Test description",
            address="Test Address",
        )

        # create two users
        test_user1 = User.objects.create_user(username='testuser1', password='pw@12345')
        test_user2 = User.objects.create_user(username='testuser2', password='pw@12345')

    def test_home_page(self):
        response = self.client.get('/hotel-booking/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')
        response = self.client.get(reverse('index'))

        # Check user is logged in
        user = response.context['user']
        self.assertEqual(str(user), username)
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_redirect_to_login_from_booking_search_page_if_user_not_authenticated(self):
        response = self.client.get('/hotel-booking/booking/search/?check_in_date=2020-10-13&check_out_date=2020-10-14')
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/booking/search/%3Fcheck_in_date%3D2020-10-13%26check_out_date%3D2020-10-14')

    def test_redirect_to_login_from_booking_details_page_if_user_not_authenticated(self):
        response = self.client.get('/hotel-booking/booking/details/')
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/booking/details/')

    def test_redirect_to_home_page_from_booking_details_if_accessed_through_get_method(self):
        username = 'testuser1'
        login = self.client.login(username=username, password='pw@12345')
        response = self.client.get('/hotel-booking/booking/details/')
        self.assertRedirects(response, '/hotel-booking/')

    def test_redirect_to_login_from_booking_list_if_user_not_authenticated(self):
        response = self.client.get('/hotel-booking/booking/list/')
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/booking/list/')

    def test_redirect_to_login_from_booking_list_if_user_is_authenticated(self):
        response = self.client.get('/hotel-booking/booking/list/')
        self.assertRedirects(response, '/hotel-booking/login/?next=/hotel-booking/booking/list/')
