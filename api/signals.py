from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import *


@receiver(post_save, sender=Booking)
def handle_room_capacity(sender, instance, created, **kwargs):
    try:
        booking = instance
        number_of_people = booking.number_of_people
        room = booking.room
        start_time = instance.start_time
        end_time = instance.end_time
        
        reservation = Reservation.objects.filter(room=room, start_time__lt=end_time, end_time__gt=start_time).first()
        
        if reservation:
            remaining_seats = reservation.remaining_seats - number_of_people
            reservation.remaining_seats = remaining_seats
            reservation.save()
            
            room.booked += number_of_people
            room.save()
        else:
            pass
            
            room.booked += number_of_people
            room.save()
            
    except Exception as e:
        print(f"An error occurred while handling room capacity: {str(e)}")
        
