from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.UserSerializer import UserRegisterSerializer
from api.models import Room, Reservation, User
from api.serializers.ReservationSerializer import AvailableRoomsSerializer, ReservationSerializer
from api.serializers.BookingSerializer import BookingSerializer
from api.serializers.RoomSerializer import RoomSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                return Response({"detail" : "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AvailableRooms(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            number_of_people = int(request.GET.get('numberOfPeople'))
            start_time = timezone.datetime.strptime(request.GET.get('start_time'), '%Y-%m-%d %H:%M')
            end_time = timezone.datetime.strptime(request.GET.get('end_time'), '%Y-%m-%d %H:%M')

            available_rooms = Reservation.objects.filter(start_time__lt=end_time,
                                                        end_time__gt=start_time,
                                                        remaining_seats__gte=number_of_people
                                                        )

            serializer = AvailableRoomsSerializer(available_rooms, many=True)

            return Response({'availableRooms': serializer.data})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   

class BookRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            room_id = request.data.get('room').get('id').get('room')
            start_time = timezone.datetime.strptime(request.data.get('start_time'), '%Y-%m-%d %H:%M')
            end_time = timezone.datetime.strptime(request.data.get('end_time'), '%Y-%m-%d %H:%M')
            number_of_people = request.data.get('number_of_people')

            try:
                room = Room.objects.get(pk=room_id)
            except Room.DoesNotExist:
                return Response({'error': 'No there room with this name - {room_id}'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                available_reservation = Reservation.objects.filter(room=room, start_time__lt=end_time,
                                                                end_time__gt=start_time,
                                                                remaining_seats__gte=number_of_people
                                                                ).first()
                if available_reservation.remaining_seats == 0 or number_of_people > available_reservation.remaining_seats:
                    return Response({'error': 'No available seats in the room'}, status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({'error': 'Selected room is not available for the specified time'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not available_reservation:
                return Response({'error': 'Selected room is not available for the specified time'}, status=status.HTTP_400_BAD_REQUEST)

            reservation_data = {
                'user': user.id,
                'room': room.id,
                'start_time': start_time,
                'end_time': end_time,
                'number_of_people': number_of_people
            }
            serializer = BookingSerializer(data=reservation_data)
            if serializer.is_valid():
                serializer.save()
                room.capacity -= number_of_people
                room.save()
                return Response({'message': 'Room booked successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class CreateReservations(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        try:
            room_serializer = RoomSerializer(data=request.data.get('room'))
            if room_serializer.is_valid():
                room = room_serializer.save()

                reservation_data = request.data.copy()
                reservation_data['room'] = room.id
                reservation_serializer = ReservationSerializer(data=reservation_data)
                if reservation_serializer.is_valid():
                    reservation_serializer.save()
                    return Response({'message': 'Reservation created successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'error': reservation_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': room_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddRoom(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListRooms(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

class GetRoom(APIView):
    def get(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)
    
class UpdateRoom(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteRoom(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        room = self.get_object(pk)
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)