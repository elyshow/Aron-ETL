from django.db import models
from django.contrib import admin



class ApiData(models.Model):
    id = models.AutoField(primary_key=True)  # Field name made lowercase.
    url = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    filetype = models.CharField(max_length=255, blank=True, null=True)
    byteamount = models.IntegerField(blank=True, null=True)
    apitype = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    paramate = models.CharField(max_length=255, blank=True, null=True)
    taskid = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.id

class ApiDataDisplay(admin.ModelAdmin):
    list_display = ('url','paramate','taskid')

class Dommana(models.Model):
    cjdomid = models.CharField(primary_key=True, max_length=255)
    cjdomname = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.state


class InfoSqlFile(models.Model):
    taskid = models.CharField(primary_key=True, max_length=255)
    domid = models.CharField(max_length=255, blank=True, null=True)
    tasktype = models.CharField(max_length=255, blank=True, null=True)
    fileway = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.taskid

class InfoSqlFileDisplay(admin.ModelAdmin):
    list_display = ('taskid', 'domid','fileway')

