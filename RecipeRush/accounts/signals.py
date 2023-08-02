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
    # Replace these with your Mailgun credentials and email details
    API_KEY = "aecda29d3d08d27bef0a866042c52361-4e034d9e-92a49a34"
    DOMAIN = "sandbox272503a250a246e194093ce86ca6afe4.mailgun.org"
    SENDER = "reciperush@abv.bg"
    RECIPIENT = user_instance.email  # Send the email to the user's email address
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
