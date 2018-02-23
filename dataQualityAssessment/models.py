from django.db import models
from django.contrib import admin

# Create your models here.

class Assess(models.Model):
    resourcechname = models.CharField(db_column='resourcechname', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    resourcename = models.CharField(db_column='resourcename', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    datasource = models.CharField(db_column='datasource', max_length=100, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    samplingnumber = models.IntegerField(db_column='samplingnumber', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    evaluationstate = models.CharField(db_column='evaluationstate', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taskstate = models.CharField(db_column='taskstate', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    card = models.CharField(db_column='card', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    assesstime = models.CharField(db_column='assesstime', max_length=100, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    def _str_(self):
        return self.resourcechname


class AssessDisplay(admin.ModelAdmin):
    list_display = ('resourcechname','resourcename', 'datasource', 'samplingnumber', 'evaluationstate','taskstate','card','assesstime')



class Logassessment(models.Model):
    datasource = models.CharField(db_column='datasource', max_length=100, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    resourcename = models.CharField(db_column='resourcename', max_length=100, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    resourcemingcheng = models.CharField(db_column='resourcemingcheng', max_length=100, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    truesampling = models.CharField(max_length=100, blank=True, null=True)
    assesstime = models.CharField(max_length=100, blank=True, null=True)
    taskstate = models.CharField(max_length=100, blank=True, null=True)

    def _str_(self):
        return self.datasource

class LogassessmentDisplay(admin.ModelAdmin):
    list_display = ('datasource','resourcename', 'resourcemingcheng', 'truesampling', 'assesstime','taskstate')


class Result(models.Model):
    fieldname = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    completeness = models.CharField(max_length=100, blank=True, null=True)
    uniqueness = models.CharField(max_length=100, blank=True, null=True)
    valuerange = models.CharField(max_length=100, blank=True, null=True)
    lengthrange = models.FloatField(blank=True, null=True)
    zifucharacter = models.CharField(max_length=100, blank=True, null=True)
    id = models.IntegerField(primary_key=True)

    def _str_(self):
        return self.fieldname

class ResultDisplay(admin.ModelAdmin):
    list_display = ('fieldname','type', 'completeness', 'uniqueness', 'valuerange','lengthrange','zifucharacter','id')
