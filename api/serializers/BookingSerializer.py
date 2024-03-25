from rest_framework import serializers
from api.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['user', 'room', 'start_time', 'end_time', 'number_of_people']