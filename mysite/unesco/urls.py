from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'unesco'

urlpatterns = [
    path('', TemplateView.as_view(template_name='unesco/index.html'), name='index'),
    path('reload/', views.unesco_reload, name='reload'),
    path('succeed/', views.unesco_succeed, name='succeed'),
]