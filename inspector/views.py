from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from inspector.notification import process_notification
from inspector.plex import process_plex


@csrf_exempt
def handle_plex(request):
    return process_plex(request)


@csrf_exempt
def notification_posted(request):
    return process_notification(request)


@csrf_exempt
def notification_removed(request):
    return HttpResponse("Not yet Implemented")


@csrf_exempt
def call_started(request):
    return HttpResponse("Not yet Implemented")


@csrf_exempt
def call_ended(request):
    return HttpResponse("Not yet Implemented")
