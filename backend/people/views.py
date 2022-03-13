# from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount, SocialToken, SocialApp
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.http import HttpResponse
from people.models import Contact
from datetime import datetime
from django.conf import settings
from phonenumber_field.phonenumber import PhoneNumber


def get_contacts(service):
    totalList = []
    kwargs = {"resourceName":"people/me", "personFields":"names,phoneNumbers,birthdays", "pageSize":1000}
    results = service.people().connections().list(**kwargs).execute()
    totalList = results['connections']
    while is_json_key_present(results, 'nextPageToken'):
        results = service.people().connections().list(
            **kwargs, pageToken=results['nextPageToken']).execute()
        totalList = totalList + results['connections']
    return totalList


def is_json_key_present(json, key):
    try:
        json[key]
    except KeyError:
        return False

    return True


def save_birthdays_from_google(request):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user = request.user

    # Code dependent upon django-allauth. Will change if we shift to another module

    # if request.user.userprofile.get_provider() != "google":
    a = SocialAccount.objects.get(user=user)
    b = SocialToken.objects.get(account=a)

    app = SocialApp.objects.get(provider="google")
    # TODO: Handle if refresh token is expired: redirect to login page to regenerate fresh token
    credentials = Credentials(
        token=b.token,
        refresh_token=b.token_secret,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=app.client_id,
        client_secret=app.secret)

    service = build('people', 'v1', credentials=credentials)

    results = get_contacts(service)
    contacts = []
    serial = []
    for per in results:
        contact = Contact()
        person_dict = {}
        contact.user = user
        if not is_json_key_present(per, 'names'):
            # Only email present for this contact
            # TODO: pick birthdays from this as well
            # print(per)
            continue
        contact.name = name = per['names'][0]['displayName']

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
            birthdate = datetime(year, birthday['month'], birthday['day'])
            contact.birthday = birthdate

            numbers = []
            if is_json_key_present(per, 'phoneNumbers'):
                numbers = [x['canonicalForm'] for x in per['phoneNumbers'] if is_json_key_present(x, 'canonicalForm')]
                number = numbers[0]  # TODO: Handle for multiple numbers
                contact.number = PhoneNumber.from_string(number)

            # TODO: Save email if no number present?
            contact.detail = per
            contacts.append(contact)

            person_dict["name"] = name
            person_dict["birthday"] = birthdate
            person_dict["number"] = numbers
            serial.append(person_dict)
        else:
            pass
        # contacts.append(contact)

    Contact.objects.bulk_update_or_create(contacts, update_fields=['birthday','number', 'detail'], match_field=['user','name'])
    return HttpResponse(serial, content_type='application/json')
