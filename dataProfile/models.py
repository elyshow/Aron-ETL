from django.db import models
from django.contrib import admin

class ResourceField(models.Model):
    fieldenglish = models.CharField(max_length=255)
    resourceid = models.CharField(max_length=24)
    tableenglish = models.CharField(max_length=24, null=True)

    def __str__(self):
        return self.resourceid

class ResourceFieldDisplay(admin.ModelAdmin):
	list_display = ('fieldenglish','resourceid','tableenglish')

class ReleaseCatalogue(models.Model):
    resourceid = models.CharField(max_length=24)
    cataloguename = models.CharField(max_length=24)
    typeid = models.CharField(max_length=12)
    releasetime = models.CharField(max_length=24)
    resourcename = models.CharField(max_length=12)
    resourceNum = models.CharField(max_length=100 ,null=True, blank=True)
    industryInfo = models.CharField(max_length=100,null=True, blank=True)
    cadastre = models.CharField(max_length=100,null=True, blank=True)
    resourceAttrCatalog = models.CharField(max_length=100,null=True, blank=True)
    sharedScope = models.CharField(max_length=100,null=True, blank=True)
    sharedArea = models.CharField(max_length=100,null=True, blank=True)
    sharedDepartment = models.CharField(max_length=100,null=True, blank=True)
    sharedMode = models.CharField(max_length=100,null=True, blank=True)
    sourceUnit = models.CharField(max_length=100,null=True, blank=True)
    businessCatalog = models.CharField(max_length=100,null=True, blank=True)
    resourceProUnit = models.CharField(max_length=100,null=True, blank=True)
    updateMode = models.CharField(max_length=100,null=True, blank=True)
    updateCycleAndDes = models.CharField(max_length=255,null=True, blank=True)
    #def __str__(self):
        #return self.resourceid

class ReleaseCatalogueDisplay(admin.ModelAdmin):
	list_display = ('resourceid','cataloguename', 'typeid', 'releasetime', 'resourcename')