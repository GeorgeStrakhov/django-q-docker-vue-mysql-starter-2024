from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer
from .models import MyUser as User
from shared.mailer import mail_client, base_email_template
from app.logging import logger

# custom token obtain with extra user fields
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# custom token refresh with extra user fields
class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


# signup view
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({"error": "A user with that email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.save()

            # create token and send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"{settings.MAIN_HOST}/verify/{uid}/{token}/"

            title = "Signup Confirmation"
            content = f"""
            <h2>Welcome to {settings.PROJECT_NAME}!</h2>
            <p>Thank you for signing up. Please confirm your email address by clicking the link below.</p>
            <br />
            <p><a href="{verification_link}" class="button">Confirm Email</a></p>
            <br />
            """

            mail_client.emails.send(
                From=f'{settings.PROJECT_NAME} <{settings.ACCOUNTS_EMAIL}>',
                To=email,
                Subject='Confirm your email',
                HtmlBody=base_email_template.substitute(title=title, content=content)
            )

            return Response({
                "message": "User created successfully. Check your email for verification link.",
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# signup token verification view
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()

                # Generate token for instant login
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    # Add custom user data here
                    'email': str(user.email),
                    'payment_plan': str(user.payment_plan),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification link"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


# Password reset request view
class PasswordResetRequestView(APIView):

    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')

        logger.info(f"Password reset request for {email}")

        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{settings.MAIN_HOST}/resetpassword/{uid}/{token}/"

            title = "Reset Password Confirmation"
            content = f"""
            <h2>Would you like to reset your password for {settings.PROJECT_NAME}?</h2>
            <p>If yes - please click the button below. If not - please ignore this message.</p>
            <br />
            <p><a href="{reset_link}" class="button">Reset Password</a></p>
            <br />
            """

            mail_client.emails.send(
                From=f'{settings.PROJECT_NAME} <{settings.ACCOUNTS_EMAIL}>',
                To=email,
                Subject='Reset your password',
                HtmlBody=base_email_template.substitute(title=title, content=content)
            )

        return Response({'message': 'If an account with the email exists, a password reset link has been sent.'}, status=status.HTTP_200_OK)


# Password reset confirmation view
class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):

        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

        if user and default_token_generator.check_token(user, token):
            user.set_password(request.data.get('password'))
            user.is_verified = True
            user.save()

            # Generate token for instant login
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                # Add custom user data here
                'email': str(user.email),
                'payment_plan': str(user.payment_plan),
            }, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid token or user. Please try resetting your password again.'}, status=status.HTTP_400_BAD_REQUEST)
