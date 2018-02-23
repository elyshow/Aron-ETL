# -*- coding: utf-8 -*-
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login, logout
from .models import Userpermission
from catalogueManagement.models import Catalogue
from cataloguedataway.models import Cataloguedataway
from codeStandard.models import RecognInfo
from dataway.models import Adminapi
import datetime
import random,json

# Create your views here.

def login(request):
    return render(request, 'user/login.html')

def startlogin(request):
    errors = []
    uname = request.POST.get('uname')
    password = request.POST.get('pwd')
    try:
        userexist=Userpermission.objects.get(username=uname)
    except Userpermission.DoesNotExist:
        errors.append('此用户不存在')
        return render_to_response('user/login.html',{'errors':errors})
    hfuser = Userpermission.objects.get(username=uname)
    hfuserid = hfuser.userid
    user = auth.authenticate(username=hfuserid, password=password)
    if user and hfuser.usertype=='0':
            auth.login(request, user)
            return HttpResponseRedirect("/userIndex/")
    elif user and hfuser.usertype=='1' or '2':
            auth.login(request, user)
            return HttpResponseRedirect("/cjjdglIndex/")
    else:
            errors.append('账号或密码错误！')
    return render_to_response("user/login.html", {'errors': errors})

def loginout(request):
    auth.logout(request)
    return render_to_response('user/login.html')

def userIndex(request):
    return render(request,'user/userIndex.html')

def userInfo(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    print(end)
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Userpermission.objects.filter(userid=request.POST.get('condition')).count()
        data = Userpermission.objects.filter(userid=request.POST.get('condition'))[start:end]
        print(counts)
    else:
        counts = Userpermission.objects.all().count()
        data = Userpermission.objects.all()[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'userid': data[num].userid,
            'username': data[num].username,
            'usertel': data[num].usertel,
            'usermail': data[num].usermail,
            'userbelong': data[num].userbelong,
            'userother': data[num].userother,
            'usertype': data[num].usertype,
            'permissionway': data[num].permissionway,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

def userDel(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Userpermission.objects.extra(where=['userid IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/userIndex/')

def getTree(pid = 0,res = []):
    data = Catalogue.objects.filter(typeparentid= pid)
    lens = len(data)
    for num in range(0, lens):
        num = int(num)
        temp = {
             'id':data[num].typeid,
             'typeparentid':data[num].typeparentid,
             'text':data[num].cataloguename,

        }
        res.append(temp)
        if not hasattr(res[num],'children'):
            res[num]['children'] = []
        res[num]['children'] = getTree(data[num].typeid, res[num]['children'])
    return res

def getTree2(pid = 0,res = []):
    data = Cataloguedataway.objects.filter(typeparentid= pid)
    lens = len(data)
    for num in range(0, lens):
        num = int(num)
        temp = {
             'id':data[num].typeid,
             'typeparentid':data[num].typeparentid,
             'text':data[num].cataloguename,

        }
        res.append(temp)
        if not hasattr(res[num],'children'):
            res[num]['children'] = []
        res[num]['children'] = getTree(data[num].typeid, res[num]['children'])
    return res

#发布的列表树
def getTreeData(request):
    a=request.GET['data']
    if a=='1':
        lists = getTree(0,[])
        return HttpResponse(json.dumps(lists), content_type="application/json")
    else:
        lists = getTree2(0,[])
        return HttpResponse(json.dumps(lists), content_type="application/json")


def passTreeData(request):
    username=request.POST['username']
    userpwd=request.POST['userpwd']
    usertel=request.POST['usertel']
    usermail=request.POST['usermail']
    comboBelong=request.POST['comboBelong']
    userother=request.POST['userother']
    perway=request.POST['ids']
    rowids=request.POST['rowids']
    usertype=request.POST['userType']
    userid=str(random.random())[2:7]
    up=Userpermission(userid=userid,usertype=usertype,username=username,usertel=usertel,userbelong=comboBelong,usermail=usermail,userother=userother,permissionway=perway,userapipower=rowids)
    up.save()
    user = User.objects.create_user(userid, usermail, userpwd)
    user.is_active = True
    user.save
    return HttpResponse(111)

def recognCombobox(request):
    s_list = RecognInfo.objects.all()
    list = []
    for i in s_list:
        temp = {
            'recognid': i.recognname,
            'recognname': i.recognname,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')

def userInfoSave(request):
    userid=request.POST['userid']
    username=request.POST['username']
    usertel=request.POST['usertel']
    usermail=request.POST['usermail']
    comboBelong=request.POST['comboBelong']
    userother=request.POST['userother']
    ids=request.POST['ids']
    getUser=Userpermission.objects.get(userid=userid)
    getUser.username=username
    getUser.usertel=usertel
    getUser.usermail=usermail
    getUser.userbelong=comboBelong
    getUser.userother=userother
    getUser.permissionway=ids
    getUser.save()
    return HttpResponse('1111')

def showData(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Adminapi.objects.filter(nameapi=request.POST.get('condition')).count()
        data = Adminapi.objects.filter(nameapi=request.POST.get('condition'))[start:end]
    else:
        counts = Adminapi.objects.order_by("-idapi").all().count()
        data = Adminapi.objects.all()[start:end]
    list = []
    for num in range(len(data)):          #遍历
        temp={
            'nameapi':data[num].nameapi,
            'idapi':data[num].idapi,
            'warehouseapi':data[num].warehouseapi,
            'createtime': data[num].createtime,
            'tableapi': data[num].tableapi,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据