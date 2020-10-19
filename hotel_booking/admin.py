from django.contrib import admin

# Register your models here.

from .models import Hotel, RoomType, Room, CardType, Card, Payment, PaymentStatus, BookingStatus, Booking

class HotelAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'address']
    list_display = ('name', 'description', 'address')

class RoomInLine(admin.StackedInline):
    model = Room
    extra = 3

class RoomTypeAdmin(admin.ModelAdmin):
    fields = ['type', 'description', 'rate']
    list_display = ('id', 'type', 'description', 'rate')
    inlines = [RoomInLine]

class RoomAdmin(admin.ModelAdmin):
    fields = ['room_type', 'number']
    list_display = ('number', 'room_type', 'rate')

class CardTypeAdmin(admin.ModelAdmin):
    fields = ['type']
    list_display = ('id', 'type')

class CardAdmin(admin.ModelAdmin):
    fields = ['payment', 'type', 'holder', 'number', 'expiry_date']

class CardInLine(admin.StackedInline):
    model = Card

class PaymentAdmin(admin.ModelAdmin):
    fields = ['transaction_number', 'booking', 'first_name', 'last_name', 'email', 'address', 'amount', 'status']
    list_display = ('transaction_number', 'booking', 'first_name', 'last_name', 'email', 'address', 'amount', 'status')
    inlines = [CardInLine]

class PaymentStatusAdmin(admin.ModelAdmin):
    fields = ['status']
    list_display = ('id', 'status')

class BookingStatusAdmin(admin.ModelAdmin):
    fields = ['status']
    list_display = ('id', 'status')

class BookingAdmin(admin.ModelAdmin):
    fields = ['reference_number', 'user', 'booking_status', 'check_in', 'check_out', 'persons', 'created_at', 'rooms']
    list_display = ('reference_number', 'user', 'check_in', 'check_out', 'persons', 'booking_status', 'created_at', 'rooms_included')

admin.site.register(Hotel, HotelAdmin)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(CardType, CardTypeAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentStatus, PaymentStatusAdmin)
admin.site.register(BookingStatus, BookingStatusAdmin)
admin.site.register(Booking, BookingAdmin)