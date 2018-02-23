from django.db import models
from django.contrib import admin

# Create your models here.
class MasterdataTable(models.Model):
    tableenglish = models.CharField(max_length=255, blank=True, null=True)
    tablechinese = models.CharField(max_length=255, blank=True, null=True)
    tableid = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.tableid

    codename = models.CharField(u'代码名称', max_length=255, blank=True, null=True)
    standardnum = models.CharField(u'标准编号', max_length=255, blank=True, null=True)
    codetable = models.CharField(u'代码表', max_length=255, blank=True, null=True)
    datasource = models.CharField(u'数据源', max_length=255, blank=True, null=True)
    registertime = models.CharField(u'注册时间', max_length=255, blank=True, null=True)
    structuretype = models.CharField(u'结构类型', max_length=255, blank=True, null=True)
    businessclass = models.CharField(u'业务分类', max_length=255, blank=True, null=True)
    codestandardclass = models.CharField(u'代码分类', max_length=255, blank=True, null=True)
    resourceproperty = models.CharField(u'资源属性分类', max_length=255, blank=True, null=True)
    other = models.CharField(u'备注说明', max_length=255, blank=True, null=True)

# class MasterdataTableDisplay(admin.ModelAdmin):
#     list_display = ('id','remark', 'source', 'tableid', 'tablechinese','tableenglish')

class Release(models.Model):
    resourceid = models.CharField(primary_key=True,max_length=24)
    resourcetype = models.CharField(max_length=12, blank=True, null=True)
    resourcename = models.CharField(max_length=12, blank=True, null=True)
    resourcecatalogue = models.CharField(max_length=108, blank=True, null=True)
    releasetime = models.CharField(max_length=24, blank=True, null=True)
    registertime = models.CharField(max_length=24, blank=True, null=True)
    businessClassification = models.CharField(max_length=50, blank=True, null=True)
    dataSource = models.CharField(max_length=50, blank=True, null=True)
    industryClassification = models.CharField(max_length=50, blank=True, null=True)
    eleOneClassification = models.CharField(max_length=50, blank=True, null=True)
    eleTwoClassification = models.CharField(max_length=50, blank=True, null=True)
    eleBreakDown = models.CharField(max_length=50, blank=True, null=True)
    updateCycle = models.CharField(max_length=50, blank=True, null=True)
    updateMode = models.CharField(max_length=50, blank=True, null=True)
    resourceAttrClassification = models.CharField(max_length=50, blank=True, null=True)
    sourceSystem = models.CharField(max_length=50, blank=True, null=True)
    sourceUnit = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.resourceid

# class ReleaseDisplay(admin.ModelAdmin):
#     list_display = ('resourceid','resourcetype', 'resourcename', 'resourcecatalogue', 'releasetime','registertime')


class FieldTable(models.Model):
    tableenglish = models.CharField(max_length=255, blank=True, null=True)
    tablechinese = models.CharField(max_length=255, blank=True, null=True)
    tableid = models.CharField(max_length=255, blank=True, null=True)
    fieldenglish = models.CharField(max_length=255, blank=True, null=True)
    fieldchinese = models.CharField(max_length=255, blank=True, null=True)
    fieldlength = models.CharField(max_length=255, blank=True, null=True)
    sqltype = models.CharField(max_length=255, blank=True, null=True)
    showtype = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    elementidentifier = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.tableid

    inseridentifier = models.CharField(u'内部标识符', max_length=255, blank=True, null=True)
    cnname = models.CharField(u'中文名称', max_length=255, blank=True, null=True)
    enname = models.CharField(u'英文名称', max_length=255, blank=True, null=True)
    cnspell = models.CharField(u'中文全拼', max_length=255, blank=True, null=True)
    identifier = models.CharField(u'标识符', max_length=255, blank=True, null=True)
    language = models.CharField(u'语境', max_length=255, blank=True, null=True)
    version = models.CharField(u'版本', max_length=255, blank=True, null=True)
    samilarname = models.CharField(u'同义词', max_length=255, blank=True, null=True)
    introduce = models.CharField(u'说明', max_length=255, blank=True, null=True)
    object = models.CharField(u'对象类词', max_length=255, blank=True, null=True)
    feature = models.CharField(u'特征词', max_length=255, blank=True, null=True)
    constraint = models.CharField(u'应用约束', max_length=255, blank=True, null=True)
    scheme = models.CharField(u'分类方案', max_length=255, blank=True, null=True)
    schemeword = models.CharField(u'分类方案值', max_length=255, blank=True, null=True)
    approvedate = models.CharField(u'批准日期', max_length=255, blank=True, null=True)
    relation = models.CharField(u'关系', max_length=255, blank=True, null=True)
    impressword = models.CharField(u'表示词', max_length=255, blank=True, null=True)
    datatype = models.CharField(u'数据类型', max_length=255, blank=True, null=True)
    dataformat = models.CharField(u'表示格式', max_length=255, blank=True, null=True)
    measunit = models.CharField(u'计量单位', max_length=255, blank=True, null=True)
    valuerange = models.CharField(u'值域', max_length=255, blank=True, null=True)
    state = models.CharField(u'状态', max_length=25, blank=True, null=True)
    suborg = models.CharField(u'提交机构',max_length=255, blank=True, null=True)
    regorg = models.CharField(u'注册机构', max_length=255, blank=True, null=True)
    mainwriter = models.CharField(u'主要起草人', max_length=255, blank=True, null=True)
    remark = models.CharField(u'备注', max_length=255, blank=True, null=True)
    datafrom = models.CharField(u'引用标准代码', max_length=255, blank=True, null=True)
    tabtype = models.CharField(max_length=25, blank=True, null=True)
    rule = models.CharField(max_length=255, blank=True, null=True)

# class FieldTableDisplay(admin.ModelAdmin):
#     list_display = ('tableenglish','tablechinese', 'tableid', 'fieldenglish', 'fieldchinese')

class FieldRelease(models.Model):
    resourceid = models.CharField(max_length=24, blank=True, null=True)
    field = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.id

# class FieldReleaseDisplay(admin.ModelAdmin):
#     list_display = ('resourceid','field', 'id')


class CatalogueStandardLibrary(models.Model):
    cataloguename = models.CharField(max_length=12, blank=True, null=True)
    typeid = models.AutoField(primary_key=True)
    typeparentid = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.typeid

# class CatalogueStandardLibraryDisplay(admin.ModelAdmin):
#     list_display = ('cataloguename','typeid', 'typeparentid')


