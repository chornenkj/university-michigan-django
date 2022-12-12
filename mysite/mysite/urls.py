"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import os
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from django.views.generic import TemplateView
from hello import views as hv

# Up two folders to serve "site" content
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.join(BASE_DIR, 'site')

urlpatterns = [
    # admin app
    path('admin/', admin.site.urls),

    # apps home page
    path('', TemplateView.as_view(template_name='home/main.html'), name='home'),

    # Guess Game by Chornenkj
    path('guess/', include('guess.urls')),

    #Ads app to pass DJ4E module on Owned Rows and Users` permittions
    path('ads/', include('ads.urls')),

    # Autos CRUD app to pass course DJ4E module
    # on creating, retreaving, updating and deleting forms
    path('autos/', include('autos.urls')),

    # Cats app to pass course DJ4E module
    # on creating a database
    path('cats/', include('cats.urls')),

    # Unesco app to create database from csv-file
    path('unesco/', include('unesco.urls')),

    # URLs for login and logout
    path('accounts/', include('django.contrib.auth.urls')),

    # these two apps are created just to pass course DJ4E
    path('polls/', include('polls.urls')),
    path('hello/', hv.myview, name='hello'),

    # this is just to browse files in the course DJ4E
    re_path(r'^site/(?P<path>.*)$', serve,
        {'document_root': SITE_ROOT, 'show_indexes': True},
        name='site_path'
    ),
]
