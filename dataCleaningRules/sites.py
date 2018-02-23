from functools import update_wrapper
from .models import *
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.db import connection
from django.conf import settings
import json


class CleanRuleSite(object):
    def __init__(self, name='dataCleaningRules'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name

    def get_urls(self):
        from django.conf.urls import url, include

        urlpatterns = [
            url(r'^$', self.index, name='index'),
            url(r'^getCheckRuleList/$', self.getCheckRuleList, name='getCheckRuleList'),
            url(r'^deleteCheckRule/$', self.deleteCheckRule, name='deleteCheckRule'),
            url(r'^saveCheckRule/$', self.saveCheckRule, name='saveCheckRule'),

            url(r'^getCleanRuleList/$', self.getCleanRuleList, name='getCleanRuleList'),
            url(r'^deleteCleanRule/$', self.deleteCleanRule, name='deleteCleanRule'),
            url(r'^saveCleanRule/$', self.saveCleanRule, name='saveCleanRule'),

            url(r'^checkRuleComboData/$', self.checkRuleComboData, name='checkRuleComboData'),
            url(r'^cleanRuleComboData/$', self.cleanRuleComboData, name='cleanRuleComboData'),
        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'dataCleaningRules', self.name

    def index(self, request):
        return render(request, 'dataCleaningRules/index.html')

    def getCheckRuleList(self, request):
        if not 'type' in request.POST:
            return JsonResponse({'errorCode': '0x0000', 'errorString': '参数错误'})
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = CheckRule.objects.filter(type=request.POST.get('type'), name=request.POST.get('condition')).count()
            data = CheckRule.objects.filter(type=request.POST.get('type'), name=request.POST.get('condition'))[start:end]
        else:
            counts = CheckRule.objects.filter(type=request.POST.get('type')).count()
            data = CheckRule.objects.filter(type=request.POST.get('type'))[start:end]

        # fields = CheckRule._meta.get_all_field_names()

        list = []
        for num in range(len(data)):
            temp = {
                'id': getattr(data[num], 'id'),
                'name': getattr(data[num], 'name'),
                'type': getattr(data[num], 'type'),
                'description': getattr(data[num], 'description'),
                'content': getattr(data[num], 'content'),
                'createTime': getattr(data[num], 'createTime'),
                'editTime': getattr(data[num], 'editTime'),
            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def deleteCheckRule(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        if request.method == 'POST':
            ids = request.POST.get('data')
            try:
                CheckRule.objects.extra(where=['id in (' + ids + ')']).delete()
            except:
                result['errorCode'] = '0x0001'
                result['errorString'] = '数据库操作失败'
        else:
            result['errorCode'] = '0x0002'
            result['errorString'] = '参数错误'
        return JsonResponse(result)

    def saveCheckRule(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        if request.method == 'POST':
            newCheckRule = CheckRule()
            fields = CheckRule._meta.get_all_field_names()
            for field in fields:
                setattr(newCheckRule, field, request.POST.get(field))
            if newCheckRule.id == '':
                newCheckRule.id = None
            else:
                newCheckRule.createTime = CheckRule.objects.get(id= request.POST.get('id')).createTime
            newCheckRule.save()
            print(connection.queries)
        else:
            result['errorCode'] = '0x0002'
            result['errorString'] = '参数错误'
        return JsonResponse(result)

    def checkRuleComboData(self, request):
        list = []
        if not request.POST.get('type'):
            return HttpResponse(json.dumps(list), content_type="application/json")
        data = CheckRule.objects.filter(type=request.POST.get('type')).only("id", "name")
        for i in range(len(data)):
            temp = {}
            temp['id'] = getattr(data[i], 'id')
            temp['name'] = getattr(data[i], 'name')
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type="application/json")

    def cleanRuleComboData(self, request):
        list = []
        if not request.POST.get('type'):
            return HttpResponse(json.dumps(list), content_type="application/json")
        data = CleanRule.objects.filter(type=request.POST.get('type')).only("id", "name")
        for i in range(len(data)):
            temp = {}
            temp['id'] = getattr(data[i], 'id')
            temp['name'] = getattr(data[i], 'name')
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type="application/json")

    def getCleanRuleList(self, request):

        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = CleanRule.objects.filter(type=request.POST.get('type'), ruleName=request.POST.get('condition')).count()
            data = CleanRule.objects.filter(type=request.POST.get('type'), ruleName=request.POST.get('condition'))[start:end]
        else:
            counts = CleanRule.objects.filter(type=request.POST.get('type')).count()
            data = CleanRule.objects.filter(type=request.POST.get('type'))[start:end]

        fields = CleanRule._meta.get_all_field_names()

        list = []
        for num in range(len(data)):
            temp = {}
            for t in range(len(fields)):
                temp[fields[t]] = getattr(data[num], fields[t])
            list.append(temp)

        return JsonResponse({'total': counts, 'rows': list})

    def deleteCleanRule(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        if request.method == 'POST':
            ids = request.POST.get('data')
            try:
                CleanRule.objects.extra(where=['id in (' + ids + ')']).delete()
            except:
                result['errorCode'] = '0x0001'
                result['errorString'] = '数据库操作失败'
        else:
            result['errorCode'] = '0x0002'
            result['errorString'] = '参数错误'
        return JsonResponse(result)

    def saveCleanRule(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        if request.method == 'POST':
            newCleanRule = CleanRule()
            fields = CleanRule._meta.get_all_field_names()
            for field in fields:
                setattr(newCleanRule, field, request.POST.get(field))
                print(field, getattr(newCleanRule, field))
            if newCleanRule.id == '':
                newCleanRule.id = None
            else:
                newCleanRule.createTime = CleanRule.objects.get(id=request.POST.get('id')).createTime
            print(request.POST)
            print(newCleanRule)
            newCleanRule.save()
            print(connection.queries)

        else:
            result['errorCode'] = '0x0002'
            result['errorString'] = '参数错误'
        return JsonResponse(result)


site = CleanRuleSite()
