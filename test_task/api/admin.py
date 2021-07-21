from django.contrib import admin
from django.http.response import Http404
from .models import Page, Versions
# Register your models here.


@admin.action(description='Make selected version active')
def make_active(modeladmin, request, queryset):
    if queryset.count() > 1:
        admin.ModelAdmin.message_user(
            modeladmin, request, message='Please select only one version', level='ERROR')
        return
    version = queryset.first()
    #page = page = Page.objects.get(id=version.page)
    page = version.page
    if page.title == version.title and page.text == version.text:
        admin.ModelAdmin.message_user(
            modeladmin, request, message='Please select unactive version', level='WARNING')
        return
    page.title = version.title
    page.text = version.text
    page.save()


class Version_activate(admin.ModelAdmin):
    list_display = ['id', 'title', 'text', 'page']
    ordering = ['id']
    actions = [make_active]


admin.site.register(Versions, Version_activate)
admin.site.register(Page)
