from django.urls import path
from . import views

app_name = 'cats'

urlpatterns = [
    path('', views.CatListView.as_view(), name='all'),
    path('cat/create/', views.CatCreateView.as_view(), name='cat_create'),
    path('cat/<int:pk>/update/', views.CatUpdateView.as_view(), name='cat_update'),
    path('cat/<int:pk>/delete/', views.CatDeleteView.as_view(), name='cat_delete'),

    path('breed/', views.BreedListView.as_view(), name='breed'),
    path('breed/create/', views.BreedCreateView.as_view(), name='breed_create'),
    path('breed/<int:pk>/update/', views.BreedUpdateView.as_view(), name='breed_update'),
    path('breed/<int:pk>/delete/', views.BreedDeleteView.as_view(), name='breed_delete'),

    path('cats_refresh', views.cats_refresh, name='refresh'),
]