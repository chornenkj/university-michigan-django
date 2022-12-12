from django.contrib import admin
from .models import Site, Category, State, Iso, Region

# Register your models here.

admin.site.register(Site)
admin.site.register(Category)
admin.site.register(State)
admin.site.register(Iso)
admin.site.register(Region)