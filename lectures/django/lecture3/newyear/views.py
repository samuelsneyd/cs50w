from datetime import datetime
from django.shortcuts import render


def index(request):
    now = datetime.now()
    return render(
        request, "newyear/user.html", {"newyear": now.month == 1 and now.day == 1}
    )
