from django.db import models
from django.contrib import admin

class Catalogue(models.Model):
    cataloguename = models.CharField(max_length=12)
    typeid = models.AutoField(primary_key=True)
    typeparentid = models.IntegerField()
    typetime = models.CharField(max_length=24)
    count = models.IntegerField()

    def __str__(self):
        return self.cataloguename

class CatalogueDisplay(admin.ModelAdmin):
    list_display = ('typeid','cataloguename', 'typeparentid', 'typetime', 'count')

