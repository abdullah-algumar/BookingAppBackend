from rest_framework import serializers
from api.models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['room', 'remaining_seats', 'start_time', 'end_time']


class AvailableRoomsSerializer(serializers.ModelSerializer):
    between = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['room', 'remaining_seats', 'between']

    def get_between(self, obj):
        return {
            "start_time": obj.start_time,
            "end_time": obj.end_time
        }