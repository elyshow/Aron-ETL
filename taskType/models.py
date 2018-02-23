from django.db import models
from django.contrib import admin
# Create your models here.
class DataIncrement(models.Model):
    incrementid = models.CharField(primary_key=True, max_length=255)
    incrementWay = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.incrementid

class dataIncrementDisplay(admin.ModelAdmin):
    list_display = ('incrementid', 'incrementWay')


class BaseType(models.Model):
    taskid = models.CharField(primary_key=True, max_length=255)
    domid = models.CharField(max_length=255, blank=True, null=True)
    filetype = models.CharField(max_length=255, blank=True, null=True)
    taskname = models.CharField(max_length=255, blank=True, null=True)
    belongto = models.CharField(max_length=1000, blank=True, null=True)
    belongtype = models.CharField(max_length=25, blank=True, null=True)
    taskstate = models.CharField(max_length=25, blank=True, null=True)
    state_run = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.taskid

class BaseTypeDisplay(admin.ModelAdmin):
    list_display = ('taskid', 'domid','taskname')


class DataInterface(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    sjyname = models.CharField(max_length=255, blank=True, null=True)
    domid = models.CharField(max_length=255, blank=True, null=True)
    databasename = models.CharField(max_length=255, blank=True, null=True)
    databasetype = models.CharField(max_length=255, blank=True, null=True)
    incrementway = models.CharField(max_length=255, blank=True, null=True)
    fwqadress = models.CharField(max_length=255, blank=True, null=True)
    dkname = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    pwd = models.CharField(max_length=255, blank=True, null=True)
    tablename = models.CharField(max_length=255, blank=True, null=True)
    ziduanname = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.id

class DataInterfaceDisplay(admin.ModelAdmin):
    list_display = ('sjyname', 'domid','databasename','username')


class RunTask(models.Model):
    id = models.AutoField(primary_key=True)
    taskid = models.CharField( blank=True, null=True, max_length=255)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    domid = models.CharField(max_length=255, blank=True, null=True)
    lastcollecttime = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.id

class RunTaskDisplay(admin.ModelAdmin):
    list_display = ('taskid', 'starttime','endtime','state')

class FileDownload(models.Model):
    taskid = models.CharField(primary_key=True, max_length=255)
    domid = models.CharField(max_length=255, blank=True, null=True)
    ipinfo = models.CharField(max_length=255, blank=True, null=True)
    pwdinfo = models.CharField(max_length=255, blank=True, null=True)
    pathinfo = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.taskid

class FileDownloadDisplay(admin.ModelAdmin):
    list_display = ('taskid', 'domid','ipinfo','pathinfo')

class InfoFile(models.Model):
    taskid = models.CharField(primary_key=True, max_length=255)
    domid = models.CharField(max_length=255, blank=True, null=True)
    tasktype = models.CharField(max_length=255, blank=True, null=True)
    fileway = models.CharField(max_length=255, blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.taskid

class InfoFileDisplay(admin.ModelAdmin):
    list_display = ('taskid', 'domid','tasktype')

class TimeTask(models.Model):
    taskid = models.CharField(primary_key=True, max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    runstate = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)
    schedule = models.CharField(max_length=255, blank=True, null=True)
    rate = models.CharField(max_length=255, blank=True, null=True)
    runtime = models.CharField(max_length=255, blank=True, null=True)
    hours = models.CharField(max_length=255, blank=True, null=True)
    minutes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.taskid



