import random
from rest_framework import status, exceptions, generics
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from config import settings
from .models import User
from .serializers import ProfileRegistrationSerializer, LoginSerializer, RegistrationSerializer, \
    LogoutSerializer, CodeCheckSerializer, CodeSendSerializer
from twilio.rest import Client
from twilio.base.exceptions import TwilioException


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status.HTTP_200_OK)


class ProfileUpdateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileRegistrationSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser, FormParser)

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeSendView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSendSerializer

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        verification_code = ''.join(random.choice('0123456789') for _ in range(4))

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your verification code is: {verification_code}',
                from_=settings.TWILIO_PHONE_NUMBER,
                to=phone_number
            )

            user = request.user
            user.phone_number = phone_number
            user.verification_code = verification_code
            user.save()

            return Response({'message': 'Verification code sent successfully.'}, status=status.HTTP_201_CREATED)
        except TwilioException as e:
            error_message = str(e)
            return Response({'message': f'Failed to send verification code. Error: {error_message}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CodeCheckView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeCheckSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verification_code = serializer.validated_data['verification_code']
        user = request.user

        if not user:
            raise exceptions.APIException('User not found!')

        if user.verification_code != verification_code:
            raise exceptions.APIException('Code is incorrect!')

        user.is_verified = True
        user.save()
        return Response({'message': 'You successfully verified your phone number'})


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
