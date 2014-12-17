from django.core import serializers
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.conf import settings
from court.models import Court
from django.http import HttpResponse
import jsonschema
import json
import re

def __failed_auth(request):
    if settings.OAUTH_TOKEN:
        return not hasattr(settings, 'OAUTH_TOKEN') or (request.META.get('HTTP_AUTHORIZATION','') != 'Bearer ' + settings.OAUTH_TOKEN)
    else:
        return False

def __to_obj(court):
    return {'uuid':court.uuid, 'name':court.name, 'slug':court.slug, 'number':court.number, 'updated_at':court.updated_at, 'closed': court.closed, 'alert': court.alert, 'lat':court.lat, 'lon':court.lon, 'DX':court.dx}

def __valid_uuid(uuid):
    return re.match('\A[a-f\d]{8}-[a-f\d]{4}-[1-5][a-f\d]{3}-[89ab][a-f\d]{3}-[a-f\d]{12}\Z',uuid)

def __json_to_court(court_json):
    with open(settings.BASE_DIR+'/../data/court-schema.json', 'r') as schema_file:
        try:
            court_obj = json.loads(court_json)
            schema = json.loads(schema_file.read())
            if jsonschema.validate(court_obj, schema) is None:
                return court_obj
        except Exception as e:
            raise ValueError("malformed or invalid json")

def list(request):
    if __failed_auth(request):
        return HttpResponseForbidden()
    courts = Court.objects.all()
    court_objs = [__to_obj(court) for court in courts]
    return HttpResponse(json.dumps(court_objs))

def public(request, slug):
    court = get_object_or_404(Court, slug=slug)
    return HttpResponse("<html><body><h1>Name: %s<h1><p>uuid: %s</p></body></html>" % (court.name, court.uuid))

def court(request, uuid):
    if __failed_auth(request):
        return HttpResponseForbidden()
    if not __valid_uuid(uuid):
        return HttpResponse("invalid uuid", status=400)
    if request.method == "GET":
        court = get_object_or_404(Court,uuid=uuid)
        court_obj = __to_obj(court)
        return HttpResponse(json.dumps(court_obj))

    elif request.method == "PUT":
        try:
            c = __json_to_court(request.body);
        except ValueError as e:
            return HttpResponse(e, status=400)
        court = Court.objects.filter(uuid=uuid)
        if len(court) != 0:
            # update existing court
            court.name=c['name']
            court.slug=c['slug']
            court.updated_at=c['updated_at']
            if hasattr(c, 'closed'):
                court.closed=c['closed']
            if hasattr(c, 'lat'):
                court.lat=c['lat']
            if hasattr(c, 'lon'):
                court.lon=c['lon']
            if hasattr(c, 'number'):
                court.number=c['number']
            if hasattr(c, 'alert'):
                court.alert=c['alert']
            if hasattr(c, 'DX'):
                court.DX=c['DX']

            return HttpResponse('{"public_url":"%s%s"}' % (settings.PUBLIC_COURT_PAGES_BASE_URL, court.slug), status=200)
        else:
            # create new court
            if len(Court.objects.filter(slug=c['slug'])) != 0:
                return HttpResponse('Error: a court with the same slug already exists', status=400)
            court = Court(
              uuid=uuid,
              name=c['name'],
              slug=c['slug'],
              updated_at=c['updated_at'],
            )
            if hasattr(c, 'closed'):
                court.closed=c['closed']
            if hasattr(c, 'lat'):
                court.lat=c['lat']
            if hasattr(c, 'lon'):
                court.lon=c['lon']
            if hasattr(c, 'number'):
                court.number=c['number']
            if hasattr(c, 'alert'):
                court.alert=c['alert']
            if hasattr(c, 'DX'):
                court.DX=c['DX']
            court.save()
            return HttpResponse('{"public_url":"%s%s"}' % (settings.PUBLIC_COURT_PAGES_BASE_URL, court.slug), status=201)
    elif request.method == "DELETE":
        court = Court.objects.filter(uuid=uuid)
        court.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)
