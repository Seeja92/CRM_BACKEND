
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
# from rest_framework.response import Response
from .models import UserProfile
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def admin_exists(request):
    exists = UserProfile.objects.filter(role="Admin").exists()
    return Response({"admin_exists": exists})
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            tokens = get_tokens_for_user(user)
            return Response({
                "access": tokens["access"],
                "refresh": tokens["refresh"],

                "email": user.email,
                "id": user.id,

                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.profile.role,
})

            

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


                tokens = get_tokens_for_user(user)
                return Response({
                    "access": tokens["access"],
                    "refresh": tokens["refresh"],

                    'email': user.email,
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.profile.role,
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

   
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"message": "Logged out successfully"},
                status=200
            )

        except Exception:
            return Response(
                {"error": "Invalid token"},
                status=400
            )
    

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


