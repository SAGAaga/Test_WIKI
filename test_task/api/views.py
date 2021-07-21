from django.db.models import query
from django.http.response import HttpResponse, Http404
from django.views import View
from django.http import JsonResponse
from .models import Page, Versions
from django.core import serializers
from django.shortcuts import get_object_or_404
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError


""" class Index(View):
    def get(self, *args, **kwargs):
        if len(kwargs) == 0:
            pages = serializers.serialize(
                'json', Page.objects.all())
            return JsonResponse(pages, safe=False)
        elif len(kwargs) == 1:
            pass
 """


@csrf_exempt
def creat_new_page(request):
    if request.method == 'POST':
        try:
            title = request.POST["title"]
            text = request.POST["text"]
            page = Page.objects.create(title=title, text=text)
            page.save()
            version = page.versions_set.create(
                title=title, text=text, page=page)
            version.save()
        except MultiValueDictKeyError as err:
            raise Http404("Not all required inputs have been submitted")
        except IntegrityError as err:
            raise Http404("This page already exists")
        return HttpResponse(status=201)


def get_all_pages(request):
    if request.method == 'GET':
        pages = serializers.serialize(
            'json', Page.objects.all())
        return JsonResponse(pages, safe=False)


def get_page_current_version(request, page_id, *args):
    if request.method == 'GET':
        try:
            page = Page.objects.get(id=page_id)
        except Page.DoesNotExist:
            page = get_object_or_404(Page, title=page_id)
        if len(args) != 0:
            return page
        else:
            return JsonResponse(serializers.serialize(
                'json', page), safe=False)


def get_page_versions(request, page_id):
    if request.method == 'GET':
        page = get_page_current_version(request, page_id, query_unsver=True)
        versions = serializers.serialize(
            'json', page.versions_set)
        return JsonResponse(versions, safe=False)


def get_page_any_versions(request, page_id):
    if request.method == 'GET':
        versions = list(get_page_versions(request, page_id).items())
        rand_version = versions[randint(0, len(versions)-1)]
        return JsonResponse(rand_version, safe=False)


@csrf_exempt
def make_version_active(request, page_id):
    if request.method == 'POST':
        page = get_page_current_version(request, page_id, query_unsver=True)
        version = request.POST["version"]
        version = get_object_or_404(Versions, id=version)
        page.title = version.title
        page.text = version.text
        page.save()
        return HttpResponse(status=200)


def make_changes(request, page_id):
    if request.method == 'PUT':
        page = get_page_current_version(request, page_id, query_unsver=True)
        title = ""
        text = ""
        title = request.PUT.get("title")
        text = request.PUT.get("text")
        if title == "":
            title = page.title
        if text == "":
            text = page.text
        if page.title != title or page.text != text:
            page.title = title
            page.text = text
            page.save()
            version = page.versions_set.create(
                title=title, text=text, page=page)
            version.save()
            return HttpResponse(status=200)
        else:
            raise Http404("No chages were sent.")
