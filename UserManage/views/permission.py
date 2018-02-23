#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from UserManage.models import User,GroupList,PermissionList,UserLog
import json
def PermissionVerify():
    '''权限认证模块,
        此模块会先判断用户是否是管理员（is_superuser为True），如果是管理员，则具有所有权限,
        如果不是管理员则获取request.user和request.path两个参数，判断两个参数是否匹配，匹配则有权限，反之则没有。
    '''
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            log = UserLog()
            log.usernamelog = request.user
            log.pathlog = request.path
            # log.flag = 
            iUser = User.objects.get(username = request.user)
            if not iUser.is_superuser:
                if not iUser.group:
                    log.flag = 0
                    log.descriptions = '%s visit %s ,url is %s, result is false' % (request.user, view_func.__name__, request.path)
                    print(log.descriptions)
                    log.save()
                    return HttpResponseRedirect(reverse('permissiondenyurl'))

                group_permission = GroupList.objects.get(name = iUser.group)
                group_permission_list = group_permission.permission.all()
                
                #精确匹配
                matchUrl = []
                for x in group_permission_list:
                    if request.path == x.url or request.path.rstrip('/') == x.url:
                        matchUrl.append(x.url)
                    elif request.path.startswith(x.url):
                        matchUrl.append(x.url)

                if len(matchUrl) == 0:
                    # return HttpResponseRedirect(reverse('permissiondenyurl'))
                    log.flag = 0
                    log.descriptions = '%s visit %s ,url is %s, result is false' % (request.user, view_func.__name__, request.path)
                    print(log.descriptions)
                    log.save()
                    if request.method == 'POST':
                        return JsonResponse({
                            'errorCode': '0x0010',
                            'errorString': '没有权限'
                            })
                    else:
                        return HttpResponseRedirect(reverse('permissiondenyurl'))
                log.flag = 1
                log.descriptions = '%s visit %s ,url is %s, result is true' % (request.user, view_func.__name__, request.path)
                print(log.descriptions)
                log.save()
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    return decorator

@login_required
def NoPermission(request):

    return render_to_response('UserManage/permission_no.html')

@login_required
@PermissionVerify()
def AddPermission(request):
    if request.method == 'POST':
        permission = PermissionList()
        if 'name' in request.POST and request.POST.get('name') != '':
            data = PermissionList.objects.all()
            for num in range(len(data)):
                if getattr(data[num], 'name') != request.POST.get('name'):
                    permission.name = request.POST.get('name')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '权限名重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0001',
                    'errorString': '必须输入权限名'
                    })
        permission.url = request.POST.get('url')
        permission.save()
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def ListPermission(request):

    return render_to_response('UserManage/permission_list.html', RequestContext(request))


@login_required
@PermissionVerify()
def EditPermission(request):
    ID = request.POST.get('id')
    iPermission = PermissionList.objects.get(id = ID)

    if request.method == 'POST':
        if 'name' in request.POST and request.POST.get('name') != '':
            data = PermissionList.objects.exclude(id = ID)
            for num in range(len(data)):
                if getattr(data[num], 'name') != request.POST.get('name'):
                    iPermission.name = request.POST.get('name')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '权限名重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '必须输入权限名'
                    })
        iPermission.url = request.POST.get('url')
        iPermission.save()
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def DeletePermission(request):
    IDs = request.POST.get('ids')
    PermissionList.objects.extra(where=['id in (' + IDs + ')']).delete()

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

def getPerList(request):

    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = PermissionList.objects.filter(name=request.POST.get('condition')).count()
        data = PermissionList.objects.filter(name=request.POST.get('condition'))[start:end]
    else:
        counts = PermissionList.objects.all().count()
        data = PermissionList.objects.all()[start:end]
    nlist = []
    for num in range(len(data)):
        temp = {
        'id': getattr(data[num], 'id'),
        'name': getattr(data[num], 'name'),
        'url': getattr(data[num], 'url'),
        }

        nlist.append(temp)
    return JsonResponse({'total': counts, 'rows': nlist})

def getName(request):
    if 'condition' in request.POST and request.POST.get('condition') != '':
        data = PermissionList.objects.filter(name=request.POST.get('condition'))
    else:
        data = PermissionList.objects.all()

    mlist = []
    for num in range(len(data)):
        temp = {
        'id': getattr(data[num], 'id'),
        'name': getattr(data[num], 'name'),
        }
        mlist.append(temp)

    return HttpResponse(json.dumps(mlist), content_type='application/json')