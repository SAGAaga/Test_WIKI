from django.urls import path
from .views import creat_new_page, get_all_pages, get_page_current_version, get_page_versions, get_page_any_versions, make_version_active, make_changes

urlpatterns = [
    path('create/', creat_new_page),
    path('<str:page_id>/any/', get_page_any_versions),
    path('<str:page_id>/versions/', get_page_versions),
    path('<str:page_id>/', get_page_current_version),
    path('make_active/<str:page_id>/', make_version_active),
    path('change/<str:page_id>/', make_changes),
    path('', get_all_pages),


]
