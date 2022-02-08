from django.http import HttpResponse, Http404
from django.shortcuts import render


texts = ["Lorem Ipsum", "Hello there"]


def index(request):
    return render(request, "singlepage/index.html")


def section(request, num):
    if 1 <= num <= len(texts):
        return HttpResponse(texts[num - 1])
    else:
        raise Http404("Not found")
