from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.conf import settings
from court.models import Court
from django.http import HttpResponse
import json

def __failed_auth(request):
    return not hasattr(settings, 'OAUTH_TOKEN') or (request.META.get('HTTP_AUTHORIZATION','') != 'Bearer ' + settings.OAUTH_TOKEN)

def __to_obj(court):
    return {'name':court.name, 'slug':court.slug, 'number':court.number, 'updated_at':court.updated_at, 'closed': court.closed, 'alert': court.alert, 'lat':court.lat, 'lon':court.lon, 'DX':court.dx}

def list(request):
    if __failed_auth(request):
        return HttpResponseForbidden()
    courts = Court.objects.all()
    court_objs = [__to_obj(court) for court in courts]
    return HttpResponse(json.dumps(court_objs))

def court(request, uuid):
    if __failed_auth(request):
        return HttpResponseForbidden()
    if request.method == "GET":
        court = get_object_or_404(Court,uuid=uuid)
        court_obj = __to_obj(court)
        return HttpResponse(json.dumps(court_obj))

    elif request.method == "PUT":
        print request.body
        try:
            c = json.loads(request.body);
        except ValueError:
            return HttpResponse("invalid JSON payload", status=400)
        court = Court.objects.filter(uuid=uuid)
        if len(court) != 0:
            # update existing court
            court.name=c['name']
            court.slug=c['slug']
            court.updated_at=c['updated_at']
            court.closed=c['closed']
            court.alert=c['alert']
            court.lat=c['lat']
            court.lon=c['lon']
            court.number=c['number']
            court.dx=c['DX']
            return HttpResponse(status=200)
        else:
            court = Court.objects.create(
              uuid=uuid,
              name=c['name'],
              slug=c['slug'],
              updated_at=c['updated_at'],
              closed=c['closed'],
              alert=c['alert'],
              lat=c['lat'],
              lon=c['lon'],
              number=c['number'],
              dx=c['DX']
            )
            return HttpResponse(status=201)
    elif request.method == "DELETE":
        if uuid == 'all-the-things':
            Court.objects.all().delete()
        else:
            court = Court.objects.filter(uuid=uuid)
            court.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
