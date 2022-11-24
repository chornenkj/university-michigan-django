from django.urls import path

from . import views

app_name = 'guess'

urlpatterns = [
    path('', views.index, name='index'),
    path('try/', views.TryView.as_view(), name='next_try'),
]