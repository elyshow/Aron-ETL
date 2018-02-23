#-*- coding:utf-8 -*-

from django.db import models

class CheckRule(models.Model):
        name = models.CharField(u'名称', max_length=255)
        type = models.IntegerField(u'类别')
        description = models.TextField(u'描述', null=True, blank=True)
        content = models.TextField(u'具体内容')
        createTime = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)
        editTime = models.DateTimeField(u'修改时间', auto_now=True)
        def __str__(self):
                return self.name


class CleanRule(models.Model):
        name = models.CharField(u'名称', max_length=255)
        type = models.IntegerField(u'类别')
        description = models.TextField(u'描述', null=True, blank=True)
        content = models.TextField(u'具体内容')
        createTime = models.DateTimeField(u'创建时间', auto_now_add=True, null=True)
        editTime = models.DateTimeField(u'修改时间', auto_now=True)

        def __str__(self):
                return self.name