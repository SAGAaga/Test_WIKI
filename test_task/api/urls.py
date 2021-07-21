from django.urls import path
from .views import creat_new_page, get_all_pages, get_page_current_version, get_page_versions, get_page_any_versions

urlpatterns = [
    path('', get_all_pages),
    path('<str:page_id>/versions/', get_page_versions),
    path('<str:page_id>/', get_page_current_version),
    path('<str:page_id>/any/', get_page_any_versions),
    path('create/', creat_new_page),

]
