from django.contrib import admin

# Register your models here.

from .models import Hotel, RoomType, Room, CardType, Card, Payment, BookingStatus, Booking

class HotelAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'address']
    list_display = ('name', 'description', 'address')

class RoomInLine(admin.StackedInline):
    model = Room
    extra = 3

class RoomTypeAdmin(admin.ModelAdmin):
    fields = ['type', 'description', 'rate']
    list_display = ('type', 'description', 'rate')
    inlines = [RoomInLine]

class RoomAdmin(admin.ModelAdmin):
    fields = ['room_type', 'number']
    list_display = ('number', 'room_type', 'rate')

class CardTypeAdmin(admin.ModelAdmin):
    fields = ['type']

class CardAdmin(admin.ModelAdmin):
    fields = ['payment', 'type', 'holder', 'number', 'expiry_date']

class CardInLine(admin.StackedInline):
    model = Card

class PaymentAdmin(admin.ModelAdmin):
    fields = ['booking', 'first_name', 'last_name', 'email', 'address', 'amount']
    inlines = [CardInLine]

class BookingStatusAdmin(admin.ModelAdmin):
    fields = ['status']

class BookingAdmin(admin.ModelAdmin):
    fields = ['user', 'booking_status', 'check_in', 'check_out', 'persons', 'created_at', 'rooms']
    list_display = ('description', 'user', 'check_in', 'check_out', 'persons', 'booking_status', 'created_at', 'rooms_included')

admin.site.register(Hotel, HotelAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(CardType, CardTypeAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(BookingStatus, BookingStatusAdmin)
admin.site.register(Booking, BookingAdmin)