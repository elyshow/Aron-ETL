from django.db import models

# Create your models here.

class dataElementsCode(models.Model):
    """docstring for ClassName"""
    code = models.CharField(max_length = 255, null=True,blank=True)
    name = models.CharField(max_length = 255, blank = True, null = True)
    notes = models.CharField(max_length = 255, blank = True, null = True)