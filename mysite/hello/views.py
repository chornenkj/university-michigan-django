from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def myview(request):
    view_count = request.session.get('view_count', 0) + 1
    request.session['view_count'] = view_count
    if view_count > 4:
        del request.session['view_count']

    resp = HttpResponse('view count=' + str(view_count))

    resp.set_cookie('dj4e_cookie', 'dfb5185f', max_age=1000)
    return resp