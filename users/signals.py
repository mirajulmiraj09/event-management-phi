from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings 
from django.core.mail import send_mail 
from django.contrib.auth.tokens import default_token_generator



@receiver(post_save,sender=User)
def send_activation_email(sender,instance,created,**kwargs):
    if created and not instance.is_active:
        token = default_token_generator.make_token(instance)
        activation_link = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"

        subject = "Activate Your Account"
        message = f"Hi {instance.email},\n\nPlease click the link below to activate your account:\n{activation_link}\n\nThank you!"
        recipient_list = [instance.email]


        try:
            send_mail(subject, message,
                      settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"Failed to send email to {instance.email}: {str(e)}")