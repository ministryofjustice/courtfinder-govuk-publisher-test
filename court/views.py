from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.conf import settings
from court.models import Court
from django.http import HttpResponse
import json

def __failed_auth(request):
    return not hasattr(settings, 'OAUTH_TOKEN') or (request.META.get('HTTP_AUTHORIZATION','') != 'Bearer ' + settings.OAUTH_TOKEN)

def list(request):
    if __failed_auth(request):
        return HttpResponseForbidden()
    courts = Court.objects.all()
    return HttpResponse(serializers.serialize("json", courts))

def court(request, uuid):
    if __failed_auth(request):
        return HttpResponseForbidden()
    if request.method == "GET":
        return HttpResponse(get_object_or_404(court, uuid=uuid))

    elif request.method == "PUT":
        c = json.loads(request.body);
        court = Court.objects.filter(uuid=uuid)
        print len(court)
        if len(court) != 0:
            print "update"
            # update existing court
            court.name=c['name']
            court.slug=c['slug']
            court.updated_at=c['updated_at']
            court.closed=c['closed']
            court.alert=c['alert']
            court.lat=c['lat']
            court.lon=c['lon']
            court.number=c['court_number']
            court.dx=c['DX']
            return HttpResponse(status=200)
        else:
            print "create"
            court = Court.objects.create(
              uuid=uuid,
              name=c['name'],
              slug=c['slug'],
              updated_at=c['updated_at'],
              closed=c['closed'],
              alert=c['alert'],
              lat=c['lat'],
              lon=c['lon'],
              number=c['court_number'],
              dx=c['DX']
            )
            return HttpResponse(status=201)
    elif request.method == "DELETE":
        court = Court.objects.filter(uuid=uuid)
        court.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
