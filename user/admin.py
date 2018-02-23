from django.contrib import admin
from .models import Userpermission,UserpermissionDisplay
# Register your models here.
admin.site.register(Userpermission,UserpermissionDisplay)