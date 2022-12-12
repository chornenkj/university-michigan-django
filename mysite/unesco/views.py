from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from scripts import unesco

from .models import Site

# Create your views here.

def unesco_reload(request):
    unesco.create_db_file_from_csv()
    return HttpResponseRedirect(reverse_lazy('unesco:succeed'))

def unesco_succeed(request):
    count = Site.objects.using('unesco').all().count()
    return render(request, 'unesco/succeed.html', {'count':count})
