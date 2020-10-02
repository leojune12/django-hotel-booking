from django.db import models
from django.conf import settings

# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RoomType(models.Model):
    type = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    rate = models.FloatField()

class Room(models.Model):
    room_type = models.ForeignKey(
        RoomType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    number = models.CharField(max_length=100)

class BookingStatus(models.Model):
    status = models.CharField(max_length=100)

class Booking(models.Model):
    rooms = models.ManyToManyField(Room)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    booking_status = models.ForeignKey(
        BookingStatus,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    check_in = models.DateField()
    check_out = models.DateField()
    persons = models.IntegerField()
    created_at = models.DateTimeField()

class Payment(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    amount = models.FloatField()

class CardType(models.Model):
    type = models.CharField(max_length=100)

class Card(models.Model):
    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        CardType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    holder = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    expiry_date = models.DateField()
