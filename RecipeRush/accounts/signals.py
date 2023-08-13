from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import RecipeRushProfile
import requests

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        RecipeRushProfile.objects.create(user=instance)
        send_email(instance)


def send_email(user_instance):
    API_KEY = "5820eb17414a6850568c171415917e20-28e9457d-aba4bd18"
    DOMAIN = "sandboxefe7db9a61b04888990e1e03bdd31a2b.mailgun.org"
    SENDER = "reciperush@abv.bg"
    RECIPIENT = user_instance.email
    SUBJECT = "Account Registration"
    TEXT = f"Hello {user_instance.username},\n\nThank you for registering an account with us! " \
           f"We are excited to have you on board.\n\nBest regards,\nThe RecipeRush Team"

    # Mailgun API endpoint
    mailgun_url = f"https://api.mailgun.net/v3/{DOMAIN}/messages"

    # Prepare the request parameters
    data = {
        "from": SENDER,
        "to": RECIPIENT,
        "subject": SUBJECT,
        "text": TEXT
    }

    # Send the POST request to Mailgun API
    response = requests.post(mailgun_url, auth=("api", API_KEY), data=data)

    # Check if the email was sent successfully
    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Status code: {response.status_code}")
        print(response.text)
