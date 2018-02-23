# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class CleanWork(models.Model):
    name = models.CharField(u'名称', max_length=255)
    description = models.TextField(u'描述', null=True, blank=True)
    fromTable = models.CharField(u'汇集库表', max_length=255)
    toTable = models.CharField(u'标准库表', max_length=255)
    # 单数据源多数据源
    # 1: 单数据源, 2: 多数据源
    resNum = models.IntegerField(u'单数据源或者多数据源', default=1)

    # example
    # {"fromField1": "toField1", "fromField2": "toField2"}
    fromFieldAndToField = models.TextField(u'汇集库表字段与标准库表字段对应关系', null=True)

    fieldFromTable = models.TextField(u'每个字段所属表', null=True)

    joinTableFields = models.TextField(u'表与表之间的关联关系', null=True)

    # example
    # {"field1": rule1, "field2": rule2}
    fromFieldAndCheckRule = models.TextField(u'汇集库表字段与校验规则对应关系', null=True)

    # example
    # {"field1": [rule1, rule2], "field2": [rule2, rule3]}
    fromFieldAndCleanRule = models.TextField(u'汇集库表字段与清洗规则(字典转换)对应关系', null=True)

    # check if this work is enabled
    flag = models.BooleanField(u'是否启用标志')
    # 任务运行状态
    # 0: 未运行状态 1: 运行中 2: 运行出错
    status = models.IntegerField(u'任务执行状态', default=0)
    # 1: 固定时间, 2: 一次性 , 3: 手动 4: 间隔
    timeType = models.IntegerField(u'执行时间分类')
    # example
    # 1: {"day": "2,10,13", "week": "1,5", "hour": "0,4,13", "min": "1,53"}
    # 2: NULL
    # 3: {"year": "2016", "month": "12", "day": "30", "hour": "12", "min": "59"}
    # 4: {"day": 30, "hour": 4, "min": 30}
    timeStr = models.TextField(u'执行时间字符串')
    crontabStr = models.TextField(u'crontab字符串', null=True, blank=True)

    lastStartTime = models.DateTimeField(u'最后启动时间', null=True, blank=True)
    nextStartTime = models.DateTimeField(u'下次启动时间', null=True, blank=True)

    createTime = models.DateTimeField(u'创建时间', auto_now_add=True, editable=True, null=True)
    editTime = models.DateTimeField(u'修改时间', auto_now=True, null=True)

    # 任务清洗方式
    # 0: 全量清洗 1: 增量清洗
    cleanWay = models.IntegerField(u'清洗方式', default=0)
    # 增量字段
    databaseIncrementField = models.CharField(u'增量字段', max_length=255, blank=True, null=True)

    def __str__(self):
            return self.name


class StandFieldToCheckRule(models.Model):
    fieldName = models.CharField(u'字段名称', max_length=255)
    ruleId = models.IntegerField(u'对应的校验规则ID', null=True, blank=True)

    def __str__(self):
            return self.fieldName + ':' + str(self.ruleId)


class CleanWorkLog(models.Model):
    fromtable = models.CharField(u'来源表', max_length=100, blank=True, null=True)
    totable = models.CharField(u'入库表', max_length=100, blank=True, null=True)
    datacounts = models.CharField(u'数据总量', max_length=100, blank=True, null=True)
    successrate = models.CharField(u'正确率', max_length=100, blank=True, null=True)
    time = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)
    workid = models.IntegerField(u'任务id', null=True, blank=True)
    maxtime = models.DateTimeField(u'信息入库最大时间', blank=True, null=True)
    # 0: 任务开始, 1: 任务成功完成, 2: 任务失败
    status = models.IntegerField(u'任务执行状态', default=0)
    incrementContent = models.CharField(u'增量字段内容记录', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.totable

