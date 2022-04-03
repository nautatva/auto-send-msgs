# from django.shortcuts import render
from people.models import Event
from message.models import ScheduledMessage
from datetime import date
from django.http import HttpResponse
# from datetime import timedelta
from utils import date_utils


def is_event_valid(ref_date:date, event:Event) -> bool:
    return date_utils.is_event_valid_at_reference_date(ref_date, event.date, event.frequency)


def schedule_event_messages(request):
    # TODO: run a scheduler to schedule messages
    # TODO: schedule_event_messages?

    user = request.user

    # TODO: Make query from user timezone
    # TODO: Make query without year
    events = Event.objects.filter(contact__created_by=user)
    # print(contacts)
    messages_to_schedule = []
    for event in events:
        if not is_event_valid(date.today(), event):
            continue

        m = ScheduledMessage()
        m.user = user
        m.content = "Happy birthday!!!!"  # TODO: Make this configurable, regex
        m.reference_event = event  # Automatically sets number and contact when saving

        m.time_to_send = date.today()  # TODO: Set time as well
        messages_to_schedule.append(m)

    ScheduledMessage.objects.bulk_create(messages_to_schedule)
    return HttpResponse(status=200)


# def get_scheduled_messages(request):
#     # TODO: Run a scheduler or continuous poll and send?
#     user = request.user
#     s = ScheduledMessage.objects.filter(user=user,time_to_send=date.today())
#     print(s)
#     pass
