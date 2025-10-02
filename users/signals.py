from django.contrib.auth.models import Group
from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings

@receiver(post_save, sender = User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        print("DEBUG: send_activation_email called for user:", instance.username, "email:", instance.email)
        print("DEBUG: EMAIL_HOST:", getattr(settings, "EMAIL_HOST", None))
        # for a single user, we need to send a token for it's unique identification:
        token = default_token_generator.make_token(instance)
        # for every single user need a unique activation url:
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}/"
        subject = "Activate Your Account-EventZone"
        message = f"""
        Dear {instance.username},
        Thank you for registering with EventZone!
        To activate your account, please verify your email by clicking the link below:{activation_url}
        Thank You!
        EventZone by @anis191"""
        recipient_list = [instance.email]
        print("DEBUG: sending mail to:", recipient_list)
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                recipient_list
            )
            print("DEBUG: send_mail completed")
        except Exception as error:
            print(f"Failed to send email to {instance.email}: {str(error)}")

pass