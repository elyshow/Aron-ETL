from django.db import models
from django.contrib import admin

# Create your models here.
class Userpermission(models.Model):
    userid = models.CharField(primary_key=True, max_length=255)
    username = models.CharField(max_length=255, blank=True, null=True)
    usertel = models.CharField(max_length=255, blank=True, null=True)
    usermail = models.CharField(max_length=255, blank=True, null=True)
    userbelong = models.CharField(max_length=255, blank=True, null=True)
    userother = models.CharField(max_length=255, blank=True, null=True)
    permissionway = models.TextField(blank=True, null=True)
    usertype = models.CharField(max_length=255, blank=True, null=True)
    userpwd = models.CharField(max_length=255, blank=True, null=True)
    userapipower = models.TextField(blank=True, null=True)
    userapicommnt = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.userid


class UserpermissionDisplay(admin.ModelAdmin):
    list_display = ('userid', 'username', 'usertel', 'usermail', 'userbelong')


