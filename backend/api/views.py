from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from bson import ObjectId
from rest_framework.permissions import IsAdminUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': ProfileSerializer(user).data,
                'access_token': str(refresh.access_token)
            }, status=201)
        else:
            print(serializer.errors)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            print(user)
            tokens = get_tokens_for_user(user)
            profile = ProfileSerializer(user)
            print(profile.data)
            return Response({
                'user': profile.data,
                'access_token': tokens['access'],
            }, status=200)
        print(serializer)
        return Response(serializer.errors, status=400)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


class ServiceListView(APIView):
    def get(self, request):
        try:
            services = Service.objects.all()
            services = [s for s in services if s.availability is True]
            serializer = ServiceSerializer(services, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            print(e)


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        print(booking_id)
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            print("error")
            return Response({'error': 'Booking not found'}, status=404)

        booking.status = 'Cancelled'
        booking.save()
        return Response({'message': 'Booking cancelled'})


class RescheduleBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)

        serializer = BookingRescheduleSerializer(data=request.data)
        if serializer.is_valid():
            booking.date = serializer.validated_data['date']
            booking.time_slot = serializer.validated_data['time_slot']
            booking.save()
            return Response({'message': 'Booking rescheduled'})
        return Response(serializer.errors, status=400)


class RateBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=404)

        serializer = BookingRateSerializer(data=request.data)
        if serializer.is_valid():
            booking.rating = serializer.validated_data['rating']
            booking.comment = serializer.validated_data.get('comment', '')
            booking.save()
            return Response({'message': 'Rating submitted'})
        return Response(serializer.errors, status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    total_services = Service.objects.count()
    total_bookings = Booking.objects.count()
    user_bookings = Booking.objects.filter(user=request.user).count()

    res= Response({
        'total_services': total_services,
        'total_bookings': total_bookings,
        'your_bookings': user_bookings
    })
    print(res.data)
    return res

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unavailable_slots(request):
    service_id = request.GET.get('service_id')
    date = request.GET.get('date')
    
    bookings = Booking.objects.filter(service_id=service_id, date=date)
    unavailable = bookings.values_list('time_slot', flat=True)
    return Response({'unavailable_slots': list(unavailable)})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.delete()
        return Response({'message': 'Booking deleted successfully.'}, status=status.HTTP_200_OK)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_bookings(request):
    bookings = Booking.objects.select_related('user', 'service').all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    users = get_user_model().objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_service_providers(request):
    providers = ServiceProvider.objects.prefetch_related('services').all()
    serializer = ServiceProviderSerializer(providers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_service_provider(request):
    predefined_services = {
        1: 'Laundry',
        2: 'Room Cleaning',
        3: 'Study Spaces',
        4: 'Room Repairs',
        5: 'Tech Support',
        6: 'AI Booking Assistant'
    }

    name = request.data.get('name')
    email = request.data.get('email')
    phone = request.data.get('phone')
    specialization = request.data.get('specialization')
    service_ids = request.data.get('services', [])

    if not name or not email:
        return Response({'error': 'Name and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

    default_password = "serviceprovider"
    user = User.objects.create_user(
        username=name,
        email=email,
        password=default_password
    )
    user.is_serviceprovider = True
    user.save()

    service_provider = ServiceProvider.objects.create(
        name=user.username,
        email=user.email,
        phone=phone,
        specialization=specialization
    )

    new_services = []
    created_services = []

    for sid in service_ids:
        service_name = predefined_services.get(sid)
        if service_name:
            service, created = Service.objects.get_or_create(
                name=service_name,
                defaults={
                    'description': get_default_description(service_name),
                    'price': 100.00,
                    'duration': '2 hours',
                    'rating': 0.0,
                    'availability': True,
                    'provider_name': name
                }
            )
            created_services.append(service.id)
            if created:
                new_services.append(ServiceSerializer(service).data)
            else:
                # optionally update provider_name if needed
                service.provider_name = name
                service.save()

    service_provider.services.set(created_services)

    response_data = {
        'service_provider': {
            'id': service_provider.id,
            'user_id': user.id,
            'name': name,
            'email': email
        },
        'newly_created_services': new_services
    }

    return Response(response_data, status=status.HTTP_201_CREATED)


def get_default_description(service_name):
    descriptions = {
        'Laundry': "Professional laundry services including washing, drying, and ironing.",
        'Room Cleaning': "Complete room cleaning with dusting, mopping, and sanitization.",
        'Study Spaces': "Well-maintained study spaces for focused and quiet study sessions.",
        'Room Repairs': "On-demand maintenance and repair services for hostel rooms.",
        'Tech Support': "Technical assistance for your devices, connectivity, and software.",
        'AI Booking Assistant': "Smart AI-powered assistant to help you schedule services easily."
    }
    return descriptions.get(service_name, "General service provided by the hostel.")


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_service_provider(request, provider_id):
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
    except ServiceProvider.DoesNotExist:
        return Response({"detail": "Provider not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ServiceProviderSerializer(provider, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_service_provider(request, provider_id):
    try:
        provider = ServiceProvider.objects.get(id=provider_id)
    except ServiceProvider.DoesNotExist:
        return Response({"detail": "Provider not found."}, status=status.HTTP_404_NOT_FOUND)

    provider.delete()
    return Response({"detail": "Provider deleted."}, status=status.HTTP_204_NO_CONTENT)


