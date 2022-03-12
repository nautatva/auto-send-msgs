# from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount, SocialToken
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from django.http import HttpResponse
from people.models import Contact
from datetime import datetime


def get_contacts(service):
    # TODO: Get more than 2000 entries - recurse with next page token
    return service.people().connections().list(
        resourceName="people/me",
        personFields='names,phoneNumbers,birthdays').execute()


def is_json_key_present(json, key):
    try:
        json[key]
    except KeyError:
        return False

    return True


def get_email_google(request):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user = request.user

    # Code dependent upon django-allauth. Will change if we shift to another module

    # if request.user.userprofile.get_provider() != "google":
    a = SocialAccount.objects.get(user=user)
    b = SocialToken.objects.get(account=a)
    # access = b.token
    token = b.token

    # TODO: do something to renew the token if expired
    credentials = Credentials(
        token=token,
        refresh_token=token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='60537759944-4mjhgk6igidjl9s3h3gnvqseuk91a6ae.apps.googleusercontent.com',  # replace with yours
        client_secret='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')  # replace with yours

    service = build('people', 'v1', credentials=credentials)

    results = get_contacts(service)
    person_dict = {}

    contacts = []
    for per in results['connections']:
        contact = Contact()
        contact.user = user
        contact.name = name = per['names'][0]['displayName']
        # As the response is an array
        # we need to do some list comprehension
        # phoneNumbers = [x['value'] for x in per['phoneNumbers']]
        if is_json_key_present(per, 'birthdays'):
            birthdays = [x['date'] for x in per['birthdays']]
            birthday = birthdays[0]  # TODO: Handle for multiple dates. find a case
            if is_json_key_present(birthday, 'year'):
                year = birthday['year']
            else:
                year = 1500
            birthdate = datetime(year, birthday['month'], birthday['day'])
            person_dict[name] = birthdate
            contact.birthday = birthdate
            contacts.append(contact)
        else:
            pass
        # contacts.append(contact)

    Contact.objects.bulk_update_or_create(contacts, ['birthday'], match_field=['user','name'])
    # TODO: send a better response
    return HttpResponse(person_dict, content_type='application/json')

    # return render(request, 'search/random_text_print.html', locals())
