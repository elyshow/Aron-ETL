
from django.db import models
from django.contrib import admin



class Problems(models.Model):
    schemename = models.CharField(max_length=255, blank=True, null=True)
    schemetype = models.CharField(max_length=255, blank=True, null=True)
    checkobject = models.CharField(max_length=255, blank=True, null=True)
    problemtable = models.CharField(max_length=255, blank=True, null=True)
    problemrecords = models.CharField(max_length=255, blank=True, null=True)
    repairrecords = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.schemename



class ProblemsDisplay(admin.ModelAdmin):
    list_display = ('schemename','schemetype', 'checkobject', 'problemtable', 'problemrecords','repairrecords')


class Catalogue(models.Model):
    cataloguename = models.CharField(max_length=12, blank=True, null=True)
    typeid = models.CharField(max_length=12,primary_key=True)
    typeparentid = models.CharField(max_length=12,blank=True, null=True)
    typetime = models.CharField(max_length=24, blank=True, null=True)

    def _str_(self):
        return self.cataloguename



class CatalogueDisplay(admin.ModelAdmin):
    list_display = ('cataloguename','typeid', 'typeparentid', 'typetime')






class Release(models.Model):
    resourceid = models.CharField(primary_key=True, max_length=24)
    resourcetype = models.CharField(max_length=12, blank=True, null=True)
    resourcename = models.CharField(max_length=12, blank=True, null=True)
    resourcecatalogue = models.CharField(max_length=108, blank=True, null=True)
    time = models.CharField(max_length=24, blank=True, null=True)

    def _str_(self):
        return self.resourceid


class ReleaseDisplay(admin.ModelAdmin):
    list_display = ('resourceid','resourcetype', 'resourcename', 'resourcecatalogue','time')




class Resourcefield(models.Model):
    fieldenglish = models.CharField(max_length=255, blank=True, null=True)
    resourceid = models.CharField(max_length=24, blank=True, null=True)

    def _str_(self):
        return self.fieldenglish

class ResourcefieldDisplay(admin.ModelAdmin):
    list_display = ('fieldenglish','resourceid')


class Assesstb(models.Model):
    schoolname = models.CharField(max_length=255, blank=True, null=True)
    provideunit = models.CharField(max_length=255, blank=True, null=True)
    datasource = models.CharField(max_length=255, blank=True, null=True)
    updatetime = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.schoolname

class AssesstbDisplay(admin.ModelAdmin):
    list_display = ('schoolname','provideunit','datasource','updatetime')

