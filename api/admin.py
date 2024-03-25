from django.contrib import admin
from api.models import *


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Booking)