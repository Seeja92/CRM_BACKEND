

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset
from django.core.mail import send_mail
from django.conf import settings


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    reset_link = (
        f"{settings.FRONTEND_URL}/reset-password"
        f"?token={reset_password_token.key}"
    )

    print("DEBUG: Resetting password for email:", reset_password_token.user.email)
    print("TOKEN:", reset_password_token.key)
    print("RESET LINK:", reset_link)

    message = (
        f"Hi {reset_password_token.user.first_name},\n\n"
        f"You requested a password reset for your CRM account.\n\n"
        f"Click the link below to reset your password:\n\n"
        f"{reset_link}\n\n"
        f"This link will expire in 24 hours.\n\n"
        f"If you did not request this, please ignore this email.\n\n"
        f"Regards,\n"
        f"CRM Team"
    )

    # send_mail(
    #     subject="Password Reset Request - CRM",
    #     message=message,
    #     from_email=settings.EMAIL_HOST_USER,
    #     recipient_list=[settings.EMAIL_HOST_USER],
    #     fail_silently=False,
    # )


@receiver(post_password_reset)
def password_reset_done(sender, user, *args, **kwargs):
    print(f"✅ PASSWORD SUCCESSFULLY RESET FOR: {user.email}")