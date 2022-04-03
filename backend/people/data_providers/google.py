from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from people.models import Contact
import json
from phonenumber_field.phonenumber import PhoneNumber
from utils.common_utils import is_json_key_present
from datetime import datetime
from django.conf import settings
import traceback


def _get_contacts_from_service(service):
    totalList = []
    kwargs = {"resourceName":"people/me", "personFields":"names,phoneNumbers,birthdays", "pageSize":1000}
    results = service.people().connections().list(**kwargs).execute()
    totalList = results['connections']
    while is_json_key_present(results, 'nextPageToken'):
        results = service.people().connections().list(
            **kwargs, pageToken=results['nextPageToken']).execute()
        totalList = totalList + results['connections']
    return totalList


def get_contacts(user) -> list:
    # Code dependent upon django-allauth. Will change if we shift to another module
    app = SocialApp.objects.get(provider="google")
    socialAccount = SocialAccount.objects.get(user=user, provider="google")
    socialAccountSecrets = SocialToken.objects.get(account=socialAccount, app=app)

    # TODO: Handle if refresh token is expired: redirect to login page to regenerate fresh token
    credentials = Credentials(
        token=socialAccountSecrets.token,
        refresh_token=socialAccountSecrets.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=app.client_id,
        client_secret=app.secret)

    service = build('people', 'v1', credentials=credentials)

    results = _get_contacts_from_service(service)
    contacts = []

    for per in results:
        contact = Contact()
        contact.created_by = user
        if not is_json_key_present(per, 'names'):
            # Only email present for this contact
            # TODO: pick birthdays from this as well
            # print(per)
            continue
        contact.name = name = per['names'][0]['displayName']

        numbers = []
        if is_json_key_present(per, 'phoneNumbers'):
            numbers = [x['canonicalForm'] for x in per['phoneNumbers'] if is_json_key_present(x, 'canonicalForm')]
            if len(numbers) > 0:
                number = numbers[0]  # TODO: Handle for multiple numbers
                try:
                    phoneNumber = PhoneNumber.from_string(number)
                except Exception:
                    print(f"Some error in {name} - phoneNumber: {number}")
                    phoneNumber = None
                contact.number = phoneNumber
            else:
                print(f"No numbers found for {name}")

        # TODO: Save email if no number present?
        contact.source = app.provider
        contact.detail = json.dumps(per)
        contacts.append(contact)

    return contacts


def extract_birthday(contact: Contact) -> datetime:
    detail = contact.detail

    # No details needed to be parsed if made manually
    if detail == settings.DEFAULT_CONTACT_DETAIL:
        return None

    try:
        per = json.loads(detail)
    except json.JSONDecodeError:
        print(f"Error in contact {contact} for user {contact.user}")
        traceback.print_exc()
        return None

    if is_json_key_present(per, 'birthdays'):
        birthdays = [x['date'] for x in per['birthdays']]
        if len(birthdays) > 1:
            # When can birthday be more than 1
            # - When contact has google profile and date present in that
            print("More than 1 birthdays found!!!!!!")
            print(per)
        birthday = birthdays[0]
        if is_json_key_present(birthday, 'year'):
            year = birthday['year']
        else:
            year = settings.DEFAULT_BIRTH_YEAR

        return datetime(year, birthday['month'], birthday['day'])

    return None
