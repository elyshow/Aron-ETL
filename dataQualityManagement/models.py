# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primarykey=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename dbtable values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [applabel]'
# into your database.
#from future import unicodeliterals

from django.db import models
from catalogueManagement.models import Catalogue
from releaseRegisterManagement.models import FieldTable
from dataCleaningRules.models import CheckRule
from django.contrib import admin
from releaseRegisterManagement.models import MasterdataTable



class Base(models.Model):
    datasource = models.CharField(max_length=255, blank=True, null=True)
    keyword = models.CharField(max_length=255, blank=True, null=True)
    ruletype = models.CharField(max_length=255, blank=True, null=True)
    methodname = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)
    rulename = models.CharField(max_length=255, blank=True, null=True)
    schemename = models.CharField(max_length=255, blank=True, null=True)
    inputperson = models.CharField(max_length=255, blank=True, null=True)
    checkfun = models.CharField(max_length=255, blank=True, null=True)
    detail = models.CharField(max_length=255, blank=True, null=True)
    schedumplan = models.CharField(max_length=255, blank=True, null=True)
    dotime = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)
    schemetype = models.CharField(max_length=255, blank=True, null=True)
    checkobject = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.datasource



class BaseDisplay(admin.ModelAdmin):
     list_display = ('datasource','keyword', 'ruletype', 'methodname', 'card','rulename','schemename','inputperson','checkfun','detail','schedumplan','dotime','starttime','endtime','schemetype','checkobject')



class Table1(models.Model):
    methodname = models.CharField(max_length=255, blank=True, null=True)
    methodtype = models.CharField(max_length=255, blank=True, null=True)
    predefinedmethod = models.CharField(max_length=255, blank=True, null=True)
    createtime = models.CharField(max_length=255, blank=True, null=True)
    checkfun = models.CharField(max_length=255, blank=True, null=True)
    methoddetail = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.methodname


class Table1Display(admin.ModelAdmin):
    list_display = ('methodname','methodtype', 'predefinedmethod', 'createtime', 'checkfun','methoddetail')


class Table2(models.Model):
    rulename = models.CharField(max_length=255, blank=True, null=True)
    object = models.CharField(max_length=255, blank=True, null=True)
    identifier = models.CharField(max_length=255, blank=True, null=True)
    chinesename = models.CharField(max_length=255, blank=True, null=True)
    datatype = models.CharField(max_length=255, blank=True, null=True)
    ruletype = models.CharField(max_length=255, blank=True, null=True)
    methodname = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.rulename

class Table2Display(admin.ModelAdmin):
        list_display = ('rulename', 'object', 'identifier', 'chinesename', 'datatype', 'ruletype','methodname')



class Table4(models.Model):
    schemename = models.CharField(max_length=255, blank=True, null=True)
    schemetype = models.CharField(max_length=255, blank=True, null=True)
    checkobject = models.CharField(max_length=255, blank=True, null=True)
    businesspolice = models.CharField(max_length=255, blank=True, null=True)
    scheduletime = models.CharField(max_length=255, blank=True, null=True)


    def _str_(self):
        return self.schemename


class Table4Display(admin.ModelAdmin):
    list_display = ('schemename', 'schemetype', 'checkobject', 'businesspolice', 'scheduletime')


class Table5(models.Model):
    schemename = models.CharField(max_length=255, blank=True, null=True)
    rulename = models.CharField(max_length=255, blank=True, null=True)
    methodname = models.CharField(max_length=255, blank=True, null=True)
    lastexecutionstatus = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    currentstatus = models.CharField(max_length=255, blank=True, null=True)
    taskstate = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.schemename

class Table5Display(admin.ModelAdmin):
        list_display = ('schemename', 'rulename', 'methodname', 'lastexecutionstatus', 'starttime','currentstatus','taskstate','card','endtime')


class Table6(models.Model):
    schemename = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    consumingtime = models.CharField(max_length=255, blank=True, null=True)
    checkrecords = models.CharField(max_length=255, blank=True, null=True)
    newrecords = models.CharField(max_length=255, blank=True, null=True)
    foundproblemrecords = models.CharField(max_length=255, blank=True, null=True)
    newproblemrecords = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.schemename

class Table6Display(admin.ModelAdmin):
        list_display = ('schemename', 'starttime', 'consumingtime', 'checkrecords', 'foundproblemrecords','newproblemrecords','card')


class Parameters(models.Model):
    parametername = models.CharField(max_length=255, blank=True, null=True)
    parameterchinese = models.CharField(max_length=255, blank=True, null=True)
    parametertype = models.CharField(max_length=255, blank=True, null=True)
    datatype = models.CharField(max_length=255, blank=True, null=True)
    defaultvalue = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    nonempty = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.parametername


class ParametersDisplay(admin.ModelAdmin):
    list_display = (
    'parametername', 'parameterchinese', 'parametertype', 'datatype', 'defaultvalue', 'remark','nonempty')



class Totable(models.Model):
    tablechinese = models.CharField(max_length=255, blank=True, null=True)
    tableenglish = models.CharField(max_length=255, blank=True, null=True)
    tableid = models.IntegerField(blank=True, null=True)
    database = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.tablechinese

class TotableDisplay(admin.ModelAdmin):
    list_display = ('tablechinese', 'tableenglish', 'tableid', 'database','card')



class Rules(models.Model):
    card = models.CharField(max_length=255, blank=True, null=True)
    fieldchinese = models.CharField(max_length=255, blank=True, null=True)
    infocode = models.CharField(max_length=255, blank=True, null=True)
    dataelement = models.CharField(max_length=255, blank=True, null=True)
    rulename = models.CharField(max_length=255, blank=True, null=True)
    ruletype = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.card

class RulesDisplay(admin.ModelAdmin):
    list_display = (
    'card', 'fieldchinese', 'infocode', 'dataelement','rulename','ruletype')


class Log(models.Model):
    schemename = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=255, blank=True, null=True)
    endtime = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)

    def _str_(self):
        return self.schemename


class LogDisplay(admin.ModelAdmin):
    list_display = ('schemename','starttime', 'endtime', 'state','card')



#检验方法管理
#---------------------------------------------caibin--------------------------------------------
class TestMethod(models.Model):
    method_name = models.TextField(max_length=50, blank=True, null=True)
    method_type = models.TextField(max_length=200, blank=True, null=True)
    predef_method = models.TextField(max_length=50, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)
    func_code = models.CharField(max_length=100, blank=True, null=True)
    m_description = models.TextField(max_length=200, blank=True, null=True)


#---------------------------------------------caibin--------------------------------------------s


#常用规则设置
class OftenRules(models.Model):
    ObjectWords = models.CharField(max_length=50, blank=True, null=True)  # 对象类词
    Identifier = models.CharField(max_length=50, blank=True, null=True)  # 标识符
    RuleName = models.CharField(max_length=50,blank=True, null=True)#规则名称
    ChineseName = models.CharField(max_length=50,blank=True, null=True)#中文名称
    RuleType = models.CharField(max_length=50, blank=True, null=True) #规则类型
    CheckMethod = models.CharField(max_length=50, blank=True, null=True)#校验方法

    ParameterName = models.CharField(max_length=50, blank=True, null=True)  # 参数名
    ParameterChineseName = models.CharField(max_length=50, blank=True, null=True)  # 参数中文名
    DataType = models.CharField(max_length=50, blank=True, null=True)  # 数据类型
    ParameterType = models.CharField(max_length=50, blank=True, null=True)  # 参数类型
    ParameterValues = models.CharField(max_length=50, blank=True, null=True)  # 参数值




#校验规则
class CheckRules(models.Model):
    RuleName = models.CharField(max_length=128, blank=True, null=True)  # 规则名称 RuleName
    CheckMethod = models.ForeignKey(TestMethod, blank=True, null=True)  # 校验方法 CheckMethod
    RuleType = models.CharField(max_length=64, blank=True, null=True) #规则类型
    CheckField = models.CharField(max_length=30, blank=True, null=True)  # 校验字段 CheckField


class BasicTesting(models.Model):
    #1
    SchemeName = models.CharField(max_length=30, blank=True, null=True)  # 方案名称 SchemeName
    CheckObject = models.CharField(max_length=128, blank=True, null=True)  # 校验对象 CheckObject
    IncrementField = models.CharField(max_length=128, blank=True, null=True)  # 增量字段 IncrementField
    UnitField = models.CharField(max_length=128, blank=True, null=True)  # 单位字段 UnitField
    ServiceTimeField = models.CharField(max_length=128, blank=True, null=True)  # 业务时间字段 ServiceTimeField
    EntryField = models.CharField(max_length=128, blank=True, null=True)  # 录入人字段 EntryFieldField
    #2
    OftenRule = models.ForeignKey(OftenRules, blank=True, null=True) #常用规则
    CheckRule = models.ForeignKey(CheckRules, blank=True, null=True) #校验规则
    #3
    #ReferenceList = models.ForeignKey(OftenRules, blank=True, null=True)
    #4
    timeType = models.CharField(max_length=128,blank = True, null = True)
    ExecutionCycle = models.CharField(max_length=128,blank=True, null=True)  # 执行周期Executionycle
    ExecutionDate = models.DateTimeField(blank=True, null=True)  # 执行时间Executionycle





    # CheckField = models.CharField(max_length=30, blank=True, null=True)  # 校验字段 CheckField

    # CheckMethod = models.ForeignKey(TestMethod)  # 校验方法 CheckMethod

    # RunTimePro = models.CharField(max_length=128, blank=True, null=True)  # 执行时间 RunTimePro

    # CheckObject = models.ForeignKey(Catalogue)  # 校验对象 CheckObject

    # IncrementField = models.ForeignKey(Totable)  # 增量字段 IncrementField

    # UnitField = models.ForeignKey(Table5)  # 单位字段 UnitField

    # ServiceTimeField = models.ForeignKey(Log)  # 业务时间字段 ServiceTimeField

    # #EntryField = models.ForeignKey(FieldTable)  # 录入人字段 EntryFieldField

    # CheckRuleType = models.ForeignKey(CheckRule)  # 校验规则类型 CheckRuleType

    # Severity = models.CharField(max_length=128, blank=True, null=True)  # 严重程度 Severity

    # # 添加常用规则
    # '''FieldName = models.CharField(max_length=128,blank=True, null=True)  #字段名 FieldName

    # ChineseName = models.CharField(max_length=128,blank=True, null=True)  #中文名 ChineseName

    # NullRate = models.CharField(max_length=128,blank=True, null=True)  #空值率 NullRate

    # InformationCode  = models.CharField(max_length=128,blank=True, null=True)  #信息代码 InformationCode

    # StandardData  = models.CharField(max_length=128,blank=True, null=True)  #标准数据元 StandardData

    # NullCheck = models.CharField(max_length=128,blank=True, null=True)  #空值校验 NullCheck'''

    # # 添加校验规则
    # RuleName = models.CharField(max_length=128, blank=True, null=True)  # 规则名称 RuleName
    # CheckMethod = models.ForeignKey(TestMethod)  # 校验方法 CheckMethod
    # CheckRuleType = models.ForeignKey(CheckRule)  # 校验规则类型 CheckRuleType
    # CheckField = models.CharField(max_length=30, blank=True, null=True)  # 校验字段 CheckField
    # '''ParameterName = models.CharField(max_length=128,blank=True, null=True)  #参数名 ParameterName

    # ParameterChineseName = models.CharField(max_length=128,blank=True, null=True)  #参数中文名 ParameterChineseName

    # DataType = models.CharField(max_length=128,blank=True, null=True)  #数据类型 DataType

    # NoNull = models.CharField(max_length=128,blank=True, null=True)  #非空 NoNull

    # ParameterValues = models.CharField(max_length=128,blank=True, null=True)  #参数值 ParameterValues'''

    # SchedulingPlan = models.CharField(max_length=128, blank=True, null=True)  # 调度计划 SchedulingPlan

    # ExecutionCycle = models.CharField(max_length=128,blank=True, null=True)  # 执行周期Executionycle

#数据质量监测任务管理
#---------------------------方国巍区域开始-----------------------------------------


    Current_State = models.CharField(max_length=30, blank=True, null=True)    #页面显示当前状态  增加

    flag = models.CharField(max_length=30, blank=True, null=True)             #页面激活 增加



#-------------------------方国巍区域结束-------------------------------------------
