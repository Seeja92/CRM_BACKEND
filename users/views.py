
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'email': user.email,
                'id': user.id,

                'first_name': user.first_name,
                'last_name': user.last_name,
            }, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)

            except User.DoesNotExist:
                return Response(
                    {'error': 'Invalid email or password.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            user = authenticate(
                username=user.username,
                password=password
            )

            if user:

                token, _ = Token.objects.get_or_create(user=user)

                return Response({
                    'token': token.key,
                    'email': user.email,
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                })

            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):

    def post(self, request):

        request.user.auth_token.delete()

        return Response({
            'message': 'Logged out successfully'
        })
    

# ── Get All Users ─────────────────────────────────────────────────────────────
class UsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all().values(
            'id', 'first_name', 'last_name', 'email'
        )
        data = [
            {
                'id'   : u['id'],
                'name' : f"{u['first_name']} {u['last_name']}".strip(),
                'email': u['email'],
            }
            for u in users
        ]
        return Response(data)


