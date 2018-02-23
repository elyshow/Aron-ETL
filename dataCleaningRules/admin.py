from django.contrib import admin

# Register your models here.
from .models import *

class CleanRuleAdmin(admin.ModelAdmin):
        #list_display = ('id', 'name', 'type', 'comment', 'content')
        list_display = tuple(CleanRule._meta.get_all_field_names())


class CheckRuleAdmin(admin.ModelAdmin):
        #list_display = ('id', 'name', 'type', 'comment', 'content')
        list_display = tuple(CheckRule._meta.get_all_field_names())

admin.site.register(CleanRule, CleanRuleAdmin)
admin.site.register(CheckRule, CheckRuleAdmin)
