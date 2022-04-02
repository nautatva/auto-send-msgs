from people.data_providers import google
from people.models import Contact
import datetime


def get_contacts(user, provider:str):
    # social = request.user.social_auth.get(provider='google-oauth2')
    # TODO: if request.user.userprofile.get_provider() != "google"
    if provider == "google":
        return google.get_contacts(user)


def extract_birthday(contact: Contact) -> datetime:
    if contact.source == "google":
        return google.extract_birthday(contact)
