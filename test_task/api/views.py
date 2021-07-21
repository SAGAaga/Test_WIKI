from django.http.response import HttpResponse, Http404
from django.http import JsonResponse
from .models import Page, Versions
from django.shortcuts import get_object_or_404
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
import json


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
    else:
        raise Http404()


def get_all_pages(request):
    if request.method == 'GET':
        pages = Page.objects.all().values('id', 'title', 'text')
        pages = [entry for entry in pages]
        # to allow non-dict objects to be serialized set the safe parameter to False
        return JsonResponse(pages, safe=False)
    else:
        raise Http404()


def get_page_by_id(page_id):
    try:
        page = Page.objects.get(id=page_id)
    except Page.DoesNotExist:
        page = get_object_or_404(Page, title=page_id)
    return page


def get_page_current_version(request, page_id):
    if request.method == 'GET':
        page = get_page_by_id(page_id)
        return JsonResponse(page.get_dict())
    else:
        raise Http404()


def get_page_versions(request, page_id):
    if request.method == 'GET':
        page = get_page_by_id(page_id)
        versions = [entry for entry in page.versions_set.all().values(
            'id', 'title', 'text', 'page')]
        # to allow non-dict objects to be serialized set the safe parameter to False
        return JsonResponse(versions, safe=False)
    else:
        raise Http404()


def get_page_any_versions(request, page_id):
    if request.method == 'GET':
        versions = json.loads(get_page_versions(request, page_id).content)
        rand_version = versions[randint(0, len(versions)-1)]
        return JsonResponse(rand_version)
    else:
        raise Http404()


@csrf_exempt
def make_version_active(request, page_id):
    if request.method == 'POST':
        page = get_page_by_id(page_id)
        version = request.POST["version"]
        version = get_object_or_404(Versions, id=version)
        page.title = version.title
        page.text = version.text
        page.save()
        return HttpResponse(status=200)
    else:
        raise Http404()


@csrf_exempt
def make_changes(request, page_id):
    if request.method == 'POST':
        page = get_page_by_id(page_id)
        title = request.POST.get("title")
        text = request.POST.get("text")
        if title is None:
            title = page.title
        if text is None:
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
    else:
        raise Http404()
