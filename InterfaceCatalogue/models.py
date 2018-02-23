from django.db import models
from django.contrib import admin

class Admintwo(models.Model):
    nameapi = models.CharField(db_column='nameAPI', max_length=12)  # Field name made lowercase.
    idapi = models.CharField(db_column='idAPI', max_length=24)  # Field name made lowercase.
    warehouseapi = models.CharField(db_column='warehouseAPI', max_length=12)  # Field name made lowercase.
    tableapi = models.CharField(db_column='tableAPI', max_length=12)  # Field name made lowercase.
    createtime = models.CharField(db_column='createTime', max_length=24)  # Field name made lowercase.
    typeid = models.CharField(max_length=24, blank=True, null=True)
    weiyi = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.idAPI

class AdmintwoDisplay(admin.ModelAdmin):
    list_display = ('nameapi','idapi','warehouseapi','tableapi','createtime','typeid','weiyi')
        

