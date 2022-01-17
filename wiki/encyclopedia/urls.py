from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:page>', views.wiki_page, name='wiki_page'),
    path('search', views.search_page, name='search')
]
