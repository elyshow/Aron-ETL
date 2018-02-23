from django.contrib import admin
from django.db import models
# Register your models here.
from .models import *

def getModelFields(model=models.Model):
	return model._meta.get_all_field_names()

class CleanWorkAdmin(admin.ModelAdmin):
	list_display = tuple(getModelFields(CleanWork))


class StandFieldToCheckRuleAdmin(admin.ModelAdmin):
	list_display = tuple(getModelFields(StandFieldToCheckRule))

class CleanWorkLogAdmin(admin.ModelAdmin):
	list_display = ('fromtable','totable', 'datacounts', 'successrate')

admin.site.register(CleanWork, CleanWorkAdmin)
admin.site.register(StandFieldToCheckRule, StandFieldToCheckRuleAdmin)
admin.site.register(CleanWorkLog, CleanWorkLogAdmin)



