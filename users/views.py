from rest_framework import status, exceptions, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import User
from .serializers import ProfileRegistrationSerializer, LoginSerializer, RegistrationSerializer, ProfileSerializer, \
    LogoutSerializer


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

    def put(self, request):
        user = request.user

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)