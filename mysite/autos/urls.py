from django.urls import path
from . import views

app_name = 'autos'
urlpatterns = [
    # App main page and list of Autos
    path('', views.MainView.as_view(), name='all'),

    # Create Auto
    path('main/create/', views.AutoCreate.as_view(), name='auto_create'),

    # Update Auto
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='auto_update'),

    # Delete Auto
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='auto_delete'),

    # Browse list of Makes
    path('lookup/', views.MakeView.as_view(), name='make_list'),

    # Create Make
    path('lookup/create/', views.MakeCreate.as_view(), name='make_create'),

    # Update Make
    path('lookup/<int:pk>/update/', views.MakeUpdate.as_view(), name='make_update'),

    # Delete Make
    path('lookup/<int:pk>/delete/', views.MakeDelete.as_view(), name='make_delete'),
]
