from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from markdown2 import markdown
from . import util


def index(request: HttpRequest):
    """
    Renders the home page.
    """
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_page(request: HttpRequest, page: str):
    """
    Renders each wiki page in the encyclopedia
    or an error page if page is not in entries.
    """
    contents = util.get_entry(page)
    if contents:
        return render(request, 'encyclopedia/wiki_page.html', {
            'page': page,
            'contents': markdown(contents)
        })

    return render(request, 'encyclopedia/error.html', {
        'page': page,
    })


def search_page(request: HttpRequest):
    """
    If there is an exact match, redirects to the query's wiki page.
    If not, displays a list of partial matches to the search query.
    """
    try:
        q = request.GET['q'].lower()
    except MultiValueDictKeyError:
        return render(request, 'encyclopedia/search.html')

    entries = util.list_entries()
    results = []

    for entry in entries:
        if q == entry.lower():
            return redirect(f'wiki/{q}')
        elif entry.lower().find(q) > -1:
            results.append(entry)

    return render(request, 'encyclopedia/search.html', {
        'results': results
    })
