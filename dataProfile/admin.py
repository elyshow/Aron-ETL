from django.contrib import admin
from .models import *


admin.site.register(ResourceField,ResourceFieldDisplay)
admin.site.register(ReleaseCatalogue,ReleaseCatalogueDisplay)