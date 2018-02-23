# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from dataCleaning.models import CleanWorkLog
from taskApp.models import Dommana
from taskType.models import RunTask,BaseType

from dataCollect.models import CollectNode, CollectTask, CollectTaskLog
from django.db.models import Sum

from django.http import HttpResponse
from releaseRegisterManagement.models import MasterdataTable
from django.conf import settings
import json
from django.http import JsonResponse
import os,time
from shujujiankong import myGlobal

def dataMonitoringStatistics(request):
    #显示的主页面的方法
    return render_to_response('shujujiankong/dataMonitoringStatistics.html')

def getData(request):
#     点击datagrid的分页按钮，自动向后台发送2个参数, rows和page，代表每页记录数和页索引
    page = int(request.POST.get('page'))
    print(page)
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        # counts = Dommana.objects.filter(region=request.POST.get('condition')).count()
        # data = Dommana.objects.filter(region=request.POST.get('condition'))[start:end]
        counts = 0
        data = []
        collectNodes = CollectNode.objects.filter(collectNodeRegion=request.POST.get('condition'))
        for collectNode in collectNodes:
            collectTasks = CollectTask.objects.filter(collectNodeId=collectNode.id)
            counts += collectTasks.count()
            data.extend(collectTasks)
        data = data[start:end]
    else:
        counts = CollectTask.objects.all().count()
        data = CollectTask.objects.all()[start:end]

    print(data)
    for oneData in data:
        oneData.allCount = CollectTaskLog.objects.filter(taskId=oneData.id).aggregate(Sum('allCount'))['allCount__sum'] or 0
        oneData.successCount = CollectTaskLog.objects.filter(taskId=oneData.id).aggregate(Sum('successCount'))['successCount__sum'] or 0
        if oneData.allCount:
            oneData.successRate = format(oneData.successCount/oneData.allCount, '0.2%')
        else:
            oneData.successRate = '0%'

    fields = CollectTask._meta.get_all_field_names()
    list = []
    for num in range(len(data)):
        temp = {}
        # 基本赋值
        for t in range(len(fields)):
            temp[fields[t]] = getattr(data[num], fields[t])
        # 赋值节点信息
        if temp['collectNodeId']:
            temp['collectNodeName'] = CollectNode.objects.get(id=temp['collectNodeId']).collectNodeName
            temp['collectNodeRegion'] = CollectNode.objects.get(id=temp['collectNodeId']).collectNodeRegion
        # 赋值日志统计信息
        temp['allCount'] = CollectTaskLog.objects.filter(taskId=temp['id']).aggregate(Sum('allCount'))['allCount__sum'] or 0
        temp['successCount'] = CollectTaskLog.objects.filter(taskId=temp['id']).aggregate(Sum('successCount'))['successCount__sum'] or 0
        if temp['allCount']:
            temp['successRate'] = format(temp['successCount']/temp['allCount'], '0.2%')
        else:
            temp['successRate'] = '0%'

        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据


def getData1(request):
    # 点击datagrid的分页按钮，自动向后台发送2个参数, rows和page，代表每页记录数和页索引
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = CleanWorkLog.objects.filter(fromtable=request.POST.get('condition')).count()
        data = CleanWorkLog.objects.filter(fromtable=request.POST.get('condition'))[start:end]
    else:
        counts = CleanWorkLog.objects.all().count()
        data = CleanWorkLog.objects.all()[start:end]
    list = []
    for num in range(len(data)):          #遍历
        temp={
            'fromtable':data[num].fromtable,
            'totable':data[num].totable,
            'datacounts': data[num].datacounts,
            'successrate': data[num].successrate,
            'time': data[num].time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        list.append(temp)
    print(list)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据

def biaozhunku_request(request):
    print("0000")
    data = request.GET['data']
    myGlobal.biaozhunHierarchy=data
    print(data)
    return render_to_response('shujujiankong/huijiku.html')

def secondPage(request):
    #显示汇集库页面的方法
    return render_to_response('shujujiankong/huijiku.html')

def getData5(request):
    print(1111)
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = RunTask.objects.filter(taskid=request.POST.get('condition'),domid=myGlobal.biaozhunHierarchy).count()
        data = RunTask.objects.filter(taskid=request.POST.get('condition'),domid=myGlobal.biaozhunHierarchy)[start:end]
        baseData = BaseType.filter(taskid=request.POST.get('condition'))[start:end]

    else:
        counts = RunTask.objects.filter(domid=myGlobal.biaozhunHierarchy).count()
        print(counts)
        data = RunTask.objects.filter(domid=myGlobal.biaozhunHierarchy)[start:end]
        print(data[0].domid)
        baseData = BaseType.objects.all()
    list = []
    type='0'
    taskname=''
    for num in range(len(data)):  # 遍历
        print(len(data))
        for bd in baseData:
            print(bd.taskid)
            print(data[num].taskid)
            if data[num].taskid == bd.taskid:
                print(1)
                type = bd.filetype
                taskname = bd.taskname
                break
            else:
                print(222)
        temp = {
            'taskid': data[num].taskid,
            'starttime': data[num].starttime,
            'endtime': data[num].endtime,
            'state':data[num].state,
            'taskname': taskname,
            'type': type,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})  # 返回json数据

def returnBack(request, tabIndex):
    return render_to_response('shujujiankong/returnBack.html', {'tabIndex': tabIndex})

