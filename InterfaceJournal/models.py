from django.db import models
from django.contrib import admin

class Protslog(models.Model):
    username = models.CharField(max_length=24)
    password = models.CharField(max_length=24)
    apiID = models.CharField(max_length=24)
    data = models.CharField(max_length=128)
    requesttime = models.CharField(max_length=24)
    returnvalue = models.CharField(max_length=255)
    returntime = models.CharField(max_length=24)
    def __str__(self):
        return self.apiID

class ProtslogDisplay(admin.ModelAdmin):
    list_display = ('apiID','username','password','apiID','data','requesttime','returnvalue','returntime')
