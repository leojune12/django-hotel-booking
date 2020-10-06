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

    def __str__(self):
        return self.type

    

class Room(models.Model):
    room_type = models.ForeignKey(
        RoomType,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    number = models.CharField(max_length=100)

    def __str__(self):
        return self.number

    def rate(self):
        return self.room_type.rate

class BookingStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Booking(models.Model):
    rooms = models.ManyToManyField(Room)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    reference_number = models.CharField(
        max_length=8,
        default="00000000"
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

    def __str__(self):
        return self.reference_number

    def rooms_included(self):
        return list(self.rooms.all())

class PaymentStatus(models.Model):
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Payment(models.Model):
    transaction_number = models.CharField(
        max_length=8,
        default="00000000"
    )
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE
    )
    status =  models.ForeignKey(
        PaymentStatus,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.transaction_number

class CardType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

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

    def __str__(self):
        return "Card for payment transaction number '" + self.payment.__str__() + "'"