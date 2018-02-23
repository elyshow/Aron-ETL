#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render_to_response,RequestContext, render
from django.contrib.auth.decorators import login_required
from UserManage.views.permission import PermissionVerify
from UserManage.models import GroupList, PermissionList
import json

@login_required
@PermissionVerify()
def AddGroup(request):
    group = GroupList()
    if request.method == 'POST':    
        if 'name' in request.POST and request.POST.get('name') != '':
            data = GroupList.objects.all()
            for num in range(len(data)):
                if getattr(data[num], 'name') != request.POST.get('name'):
                    group.name = request.POST.get('name')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '用户名组重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0001',
                    'errorString': '必须输入组名'
                    })
        group.save()
        prelist = request.POST.getlist('permission[]')
        for permissionid in prelist:
            group.permission.add(PermissionList.objects.get(id = permissionid))
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def ListGroup(request):

    return render(request, 'UserManage/group_list.html')

@login_required
@PermissionVerify()
def EditGroup(request):
    ID = request.POST.get('id')
    iGroup = GroupList.objects.get(id=ID)
    if request.method == "POST":
        if 'name' in request.POST and request.POST.get('name') != '':
            data = GroupList.objects.exclude(id = ID)
            for num in range(len(data)):
                if getattr(data[num], 'name') != request.POST.get('name'):
                    iGroup.name = request.POST.get('name')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '用户组重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '必须输入用户组名'
                    })
        iGroup.save()
        data = PermissionList.objects.all()
        for num in range(len(data)):
            iGroup.permission.remove(PermissionList.objects.get(id = getattr(data[num], 'id')))

        prelist = request.POST.getlist('permission[]')
        for permissionid in prelist:
            iGroup.permission.add(PermissionList.objects.get(id = permissionid))
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def DeleteGroup(request):
    IDs = request.POST.get('ids')
    GroupList.objects.extra(where=['id in (' + IDs + ')']).delete()
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

def getGroupList(request):

    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = GroupList.objects.filter(name=request.POST.get('condition')).count()
        data = GroupList.objects.filter(name=request.POST.get('condition'))[start:end]
    else:
        counts = GroupList.objects.all().count()
        data = GroupList.objects.all()[start:end]

    nlist = []
    for num in range(len(data)):
        temp = {
        'id': getattr(data[num], 'id'),
        'name': getattr(data[num], 'name'),
        }
        nlist.append(temp)
    return JsonResponse({'total': counts, 'rows': nlist})

def getGroupName(request):

    if 'condition' in request.POST and request.POST.get('condition') != '':
        data = GroupList.objects.filter(name=request.POST.get('condition'))
    else:
        data = GroupList.objects.all()
    mlist = []
    for num in range(len(data)):
        temp = {
        'id': getattr(data[num], 'id'),
        'name': getattr(data[num], 'name'),
        }
        mlist.append(temp)

    return HttpResponse(json.dumps(mlist), content_type='application/json')