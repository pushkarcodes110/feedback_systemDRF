from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from django.contrib.auth import logout
from rest_framework import status
from accounts.api.serializers import RegistrationSerializer

@api_view(['POST',])
@extend_schema(
    description="Logout user and delete their authentication token.",
    responses={200: None}  # No response body expected for successful logout
)
def logout_view(request):
    if request.method == 'POST':
        user = request.user
        try:
            token = Token.objects.get(user=user)
            token.delete()

            # Access the underlying HttpRequest object
            django_request = request._request
            logout(django_request)  # Django logout function with HttpRequest
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            # If user does not have a token, just log them out
            django_request = request._request
            logout(django_request)  # Django logout function with HttpRequest
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

@api_view(['POST',])
@extend_schema(
    responses=RegistrationSerializer,
    description="User registration endpoint.",
)
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "Registration Successful!"
            data['username'] = account.username
            data['email'] = account.email

            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data, status=status.HTTP_201_CREATED)
