from django.db import models
from django.contrib import admin

# Create your models here.

class DataStandard(models.Model):
    codename = models.CharField(max_length=255, blank=True, null=True)
    standardnum = models.CharField(max_length=255, blank=True, null=True)
    codetable = models.CharField(max_length=255, blank=True, null=True)
    datasource = models.CharField(max_length=255, blank=True, null=True)
    registertime = models.CharField(max_length=255, blank=True, null=True)
    codesetname = models.CharField(max_length=255, blank=True, null=True)
    structuretype = models.CharField(max_length=255, blank=True, null=True)
    businessclass = models.CharField(max_length=255, blank=True, null=True)
    codestandardclass = models.CharField(max_length=255, blank=True, null=True)
    resourceproperty = models.CharField(max_length=255, blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.codename

class DataStandardDisplay(admin.ModelAdmin):
    list_display = ('codename', 'standardnum', 'codetable', 'datasource', 'registertime')

class StandardData(models.Model):
    cnname = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(primary_key=True, max_length=255)
    objectbelong = models.CharField(max_length=255, blank=True, null=True)
    datatype = models.CharField(max_length=255, blank=True, null=True)
    standard_sou = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    tabtype = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.codename
class StandardDataDisplay(admin.ModelAdmin):
    list_display = ('cnname','identifier', 'objectbelong', 'datatype', 'state')

class ComboBoxData(models.Model):
    typeid = models.AutoField(primary_key=True)
    value = models.CharField(max_length=255, blank=True, null=True)
    cnname = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.typeid
class ComboBoxDataDisplay(admin.ModelAdmin):
    list_display = ('typeid','value', 'cnname', 'type')

class DataType(models.Model):
    dataname = models.CharField(max_length=255, blank=True, null=True)
    mainword = models.CharField(max_length=255, blank=True, null=True)
    standardcode = models.CharField(max_length=255, blank=True, null=True)
    classify = models.CharField(max_length=255, blank=True, null=True)
    userecognize = models.CharField(max_length=255, blank=True, null=True)
    dataid = models.AutoField(primary_key=True)

    def __str__(self):
        return self.dataname

class DataTypeDisplay(admin.ModelAdmin):
    list_display = ('dataid','dataname', 'mainword', 'standardcode', 'classify')

class BusCode(models.Model):
    codeid = models.AutoField(primary_key=True)
    codename = models.CharField(max_length=255, blank=True, null=True)
    codetable = models.CharField(max_length=255, blank=True, null=True)
    busclass = models.CharField(max_length=255, blank=True, null=True)
    registertime = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.codeid

class BusCodeDisplay(admin.ModelAdmin):
    list_display = ('codeid','codename', 'codetable', 'busclass', 'registertime')

class StandardDataInfo(models.Model):
    rule = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    inseridentifier = models.CharField(max_length=255, blank=True, null=True)
    samilarname = models.CharField(max_length=255, blank=True, null=True)
    object = models.CharField(max_length=255, blank=True, null=True)
    feature = models.CharField(max_length=255, blank=True, null=True)
    relation = models.CharField(max_length=255, blank=True, null=True)
    impressword = models.CharField(max_length=255, blank=True, null=True)
    datatype = models.CharField(max_length=255, blank=True, null=True)
    datarule = models.CharField(max_length=255, blank=True, null=True)
    valuerange = models.CharField(max_length=255, blank=True, null=True)
    measunit = models.CharField(max_length=255, blank=True, null=True)
    subrecogn = models.CharField(max_length=255, blank=True, null=True)
    mainwriter = models.CharField(max_length=255, blank=True, null=True)
    introduce = models.CharField(max_length=255, blank=True, null=True)
    approvedate = models.CharField(max_length=255, blank=True, null=True)
    datafrom = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    cnspell = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    cnname = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=25, blank=True, null=True)
    tabtype = models.CharField(max_length=25, blank=True, null=True)
    nameid = models.AutoField(primary_key=True)


    def __str__(self):
        return self.rule

class StandardDataInfoDisplay(admin.ModelAdmin):
    list_display = ('rule','identifier', 'inseridentifier', 'samilarname', 'object')

class RecognInfo(models.Model):
    rid = models.AutoField(primary_key=True)
    recognid = models.CharField(max_length=255, blank=True, null=True)
    recognname = models.CharField(max_length=255, blank=True, null=True)
    recogntype = models.CharField(max_length=255, blank=True, null=True)
    recognnumber = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.rid

class RecognInfoDisplay(admin.ModelAdmin):
    list_display = ('rid','recognid', 'recognname', 'recogntype', 'recognnumber')

class DataBase(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.id
class DataBaseDisplay(admin.ModelAdmin):
    list_display = ('id','name', 'type')

