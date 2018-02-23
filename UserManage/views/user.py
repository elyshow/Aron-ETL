#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render_to_response,RequestContext, render, redirect
from django.contrib.auth.decorators import login_required
from UserManage.views.permission import PermissionVerify
from django.contrib import auth
from django.contrib.auth import get_user_model
from UserManage.models import User,GroupList
import logging
    
logger=logging.getLogger('sourceDns.webdns.views')

REDIRECT_FIELD_NAME = 'next'

def LoginUser(request):
    '''用户登录'''
    count = User.objects.all().count()
    logger.error(count)
    if count == 0:
        user = User()
        user.name = 'admin'
        user.set_password('admin') 
        user.is_active = 1
        user.is_superuser = 1
        user.save()
    if request.method == 'GET' and request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    # if request.method == 'GET' and 'next' in request.GET:
    #     next = request.GET['next']
    # else:
    #     next = '/'

    redirect_to = request.POST.get(REDIRECT_FIELD_NAME,
                                   request.GET.get(REDIRECT_FIELD_NAME, ''))

    errorString = ''

    if request.method == 'POST':
        user_cache = auth.authenticate(username = request.POST['username'], password = request.POST['password'])
        print(user_cache)
        if user_cache is not None:
            if user_cache.is_active:
                auth.login(request, user_cache)
                return HttpResponseRedirect(redirect_to)
            else:
                errorString = '账号被禁用!'
        else:
            errorString = '账号密码不匹配'

    kwvars = {
        'request': request,
        'next': redirect_to,
        'errorString': errorString
    }
    return render_to_response('UserManage/login.html', kwvars, RequestContext(request))

@login_required
def LogoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP REFERER', '/'))

@login_required
def ChangePassword(request):
    ID = request.user.id
    iUser = User.objects.get(id = ID)
    if request.method == 'POST':   
        if request.POST.get('pwdd') == request.POST.get('countersign '):
            iUser.set_password(request.POST.get('countersign '))
            iUser.save()
            return JsonResponse({
                'errorCode': '0x0002',
                'errorString': '密码修改成功'
                })
        else:
            return JsonResponse({
                'errorCode': '0x0010',
                'errorString': '两次输入密码不相同'
                })

    return render_to_response('UserManage/password_change.html', RequestContext(request))

@login_required
@PermissionVerify()
def ListUser(request):

    return render_to_response('UserManage/user_list.html',RequestContext(request))


def getList(request):

    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = User.objects.filter(username=request.POST.get('condition')).count()
        data = User.objects.filter(username=request.POST.get('condition'))[start:end]
    else:
        counts = User.objects.all().count()
        data = User.objects.all()[start:end]
       
    nlist = []

    for num in range(len(data)):
        ID = getattr(data[num], 'id')
        GROUP = getattr(data[num], 'group')
        temp = {
        'id': getattr(data[num], 'id'),
        'username': getattr(data[num], 'username'),
        'department': getattr(data[num], 'department'),
        'email': getattr(data[num], 'email'),
        'telephone': getattr(data[num], 'telephone'),
        'is_active': getattr(data[num], 'is_active'),
        'group': int(getattr(data[num], 'group_id')),
        'group_name': GroupList.objects.get(id = int(getattr(data[num], 'group_id'))).name
        }
        nlist.append(temp)
    return JsonResponse({'total': counts, 'rows': nlist})



@login_required
@PermissionVerify()
def AddUser(request):
    
    if request.method == 'POST':
        user = User()
        if 'username' in request.POST and request.POST.get('username') != '':
            data = User.objects.all()
            for num in range(len(data)):
                if getattr(data[num], 'username') != request.POST.get('username'):
                    user.username = request.POST.get('username')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '用户名重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '必须输入用户名'
                    })
        if 'password' in request.POST and request.POST.get('password') == '':
            return JsonResponse({
                    'errorCode': '0x0004',
                    'errorString': '必须输入密码'
                    })
        elif len(request.POST.get('password')) < 8:
            return JsonResponse({
                    'errorCode': '0x0005',
                    'errorString': '密码必须大于8位'
                    })
        else:
            user.set_password(request.POST.get('password'))
        user.telephone = request.POST.get('telephone')
        user.email = request.POST.get('email')
        user.department = request.POST.get('department')
        if 'group' in request.POST and request.POST.get('group') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须选择用户组'
                    })
        else:
            user.group = GroupList.objects.get(id=request.POST.get('group'))
        user.is_active = request.POST.getlist('is_active')
        user.save()

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def EditUser(request):
    ID = request.POST.get('id')
    iUser = User.objects.get(id = ID)
    if request.method == 'POST':
        if 'username' in request.POST and request.POST.get('username') != '':
            data = User.objects.exclude(id = ID)
            for num in range(len(data)):
                if getattr(data[num], 'username') != request.POST.get('username'):
                    iUser.username = request.POST.get('username')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '用户名重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '必须输入用户名'
                    })
        iUser.telephone = request.POST.get('telephone')
        iUser.email = request.POST.get('email')
        iUser.department = request.POST.get('department')
        if 'group' in request.POST and request.POST.get('group') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须选择用户组'
                    })
        else:
            iUser.group = GroupList.objects.get(id=request.POST.get('group'))
        if request.POST.get('is_active') == 'False':
            iUser.is_active = 0
        else:
            iUser.is_active = 1
        iUser.save()

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def DeleteUser(request):
    IDs = request.POST.get('ids')
    for ID in IDs.split(','):
        iUser = get_user_model().objects.get(id = ID)
        if int(iUser.is_active) == 1:
            return JsonResponse({
                'errorCode': '0x00099',
                'errorString': '请先禁用用户后再删除'
                })
        elif int(iUser.is_superuser) == 1:
            return JsonResponse({
                'errorCode': '0x00099',
                'errorString': '超级管理员不能删除'
                })
    get_user_model().objects.extra(where=['id in (' + IDs + ')']).delete()
    print(123)
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

@login_required
@PermissionVerify()
def ResetPassword(request):
    try:
        ID = request.POST.get('id')
        user = get_user_model().objects.get(id = ID)
        if request.method == 'POST':
            if request.POST.get('newpsw1') == request.POST.get('newpsw2'):
                user.set_password(request.POST.get('newpsw2'))
                user.save()
                return JsonResponse({
                    'errorCode': '0x0000',
                    'errorString': '密码修改成功'
                    })
            else:
                return JsonResponse({
                    'errorCode': '0x0010',
                    'errorString': '两次输入密码不相同'
                    })
    except Exception as e:
        # log
        print(e)
        return JsonResponse({
            'errorCode': '0x0011',
            'errorString': '修改密码出错'
        })