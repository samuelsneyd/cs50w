from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from markdown2 import markdown
import random
from . import util


def index(request: HttpRequest):
    """
    Renders the home page.
    """
    return render(request, "encyclopedia/user.html", {
        "entries": util.list_entries()
    })


def wiki_page(request: HttpRequest, page: str) -> HttpResponse:
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


def edit_wiki_page(request: HttpRequest, page: str) -> HttpResponse:
    """
    Edits any existing encyclopedia entry.
    Redirects to the updated entry on successful update.
    """
    contents = util.get_entry(page)

    if not contents:
        return render(request, 'encyclopedia/error.html', {
            'page': page,
        })

    if request.method == 'POST':
        util.save_entry(page, request.POST['content'])
        return redirect(f'/wiki/{page}')

    return render(request, 'encyclopedia/edit.html', {
        'page': page,
        'contents': contents
    })


def search_page(request: HttpRequest) -> HttpResponse:
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


def new_page(request: HttpRequest) -> HttpResponse:
    """
    Get: renders a page to create new entries.
    Post: save the the post as a new entry and redirects to it.
    """
    if request.method == 'POST':
        title = request.POST['title'].strip()
        content = request.POST['content']

        if not title or not content:
            return redirect('error')

        entries = util.list_entries()

        for entry in entries:
            if title.lower() == entry.lower():
                return redirect('error')

        util.save_entry(title, content)

        return redirect(f'wiki/{title}')

    return render(request, 'encyclopedia/new.html')


def random_page(request: HttpRequest) -> HttpResponse:
    """
    Redirects to a random encyclopedia entry.
    """
    random_entry = random.choice(util.list_entries())
    return redirect(f'wiki/{random_entry}')


def error(request: HttpRequest) -> HttpResponse:
    return render(request, 'encyclopedia/error.html')
