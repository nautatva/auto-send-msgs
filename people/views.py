# from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount, SocialToken
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
# import urllib
# import xml.etree.ElementTree as etree
from django.http import HttpResponse


def get_email_google(request):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user = request.user

    # Code dependent upon django-allauth. Will change if we shift to another module

    # if request.user.userprofile.get_provider() != "google":
    a = SocialAccount.objects.get(user=user)
    # print(a)
    b = SocialToken.objects.get(account=a)
    # print(b)
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

    results = service.people().connections().list(
        resourceName="people/me",
        personFields='names,phoneNumbers,birthdays').execute()
    person_dict = {}
    for per in results['connections']:
        try:
            name = per['names'][0]['displayName']
            # As the response is an array
            # we need to do some list comprehension
            phoneNumbers = [x['value'] for x in per['phoneNumbers']]
            person_dict[name] = phoneNumbers
        except Exception:
            name = per['names'][0]['displayName']
            person_dict[name] = "No phone Number"

    print(person_dict)
    # TODO: send a parsed json with only birthdays
    return HttpResponse(person_dict, content_type='application/json')

    # return render(request, 'search/random_text_print.html', locals())
