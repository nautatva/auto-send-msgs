# from django.shortcuts import render
from django.http import HttpResponse
from people.models import Contact, Event
from itertools import islice
from people.data_providers import core


# TODO: Add authenticated flag across the application
def extract_birthdays_from_contacts(request):
    user = request.user
    contacts = Contact.objects.filter(user=user)

    events = []
    for contact in contacts:
        birthdate = core.extract_birthday(contact)
        if birthdate is None:
            continue

        event = Event()
        event.name = "Birthday"
        event.date = birthdate
        event.contact = contact

        events.append(event)

    Event.objects.bulk_update_or_create(events, update_fields=['name', 'date', 'contact'], match_field=['name', 'date', 'contact'])
    return HttpResponse(content_type='application/json')


def get_contacts_from_google(request):
    user = request.user

    # TODO: Add account relations from multiple providers
    # TODO: Handle without specifying provider (get data from user object, fetch all incase multiple linked)
    contacts = core.get_contacts(user, "google")

    split_list = []
    len_list = len(contacts)
    contacts_iter = iter(contacts)
    split_size = 500
    while len_list > 0:
        split_list.append(list(islice(contacts_iter, split_size)))
        len_list = len_list - split_size

    for split in split_list:
        # TODO: Check if (bulk_update_or_create) is better, or (query, make a map and update new contacts with respective IDs)
        Contact.objects.bulk_update_or_create(split, update_fields=['number', 'source', 'detail'], match_field=['created_by','name'])
    return HttpResponse(content_type='application/json')
