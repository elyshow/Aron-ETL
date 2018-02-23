from django.db import models
from django.contrib import admin
# Create your models here.

class Cataloguedataway(models.Model):
    cataloguename = models.CharField(max_length=12, blank=True, null=True)
    typeid = models.AutoField(primary_key=True)
    typeparentid = models.IntegerField(blank=True, null=True)
    typetime = models.CharField(max_length=24, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    def _str_(self):
        return self.cataloguename
class CataloguedatawayDisplay(admin.ModelAdmin):
	list_display = ('typeid','cataloguename', 'typeparentid', 'typetime', 'count')

class Cataloguedatawaybm(models.Model):
    typeid = models.CharField(max_length=24, blank=True, null=True)
    cataloguename = models.CharField(max_length=24, blank=True, null=True)
    idapi = models.CharField(max_length=24, blank=True, null=True)

    def _str_(self):
        return self.typeid
class CataloguedatawaybmDisplay(admin.ModelAdmin):
	list_display = ('typeid','cataloguename', 'idapi')


class InterfacejournalProtslog(models.Model):
    username = models.CharField(max_length=24)
    password = models.CharField(max_length=24)
    apiid = models.CharField(max_length=24)
    data = models.CharField(max_length=128)
    requesttime = models.CharField(max_length=24)
    returnvalue = models.CharField(max_length=255)
    returntime = models.CharField(max_length=24)

    def _str_(self):
        return self.username
class InterfacejournalProtslogDisplay(admin.ModelAdmin):
	list_display = ('username','password', 'apiid', 'data', 'requesttime')
