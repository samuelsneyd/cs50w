from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:page>', views.wiki_page, name='wiki_page'),
    path('wiki/<str:page>/edit', views.edit_wiki_page, name='edit_wiki_page'),
    path('search', views.search_page, name='search'),
    path('new', views.new_page, name='new'),
    path('random', views.random_page, name='random'),
    path('error', views.error, name='error'),
]
