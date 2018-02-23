# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from taskType.models import BaseType
from taskType.models import DataInterface
from taskType.models import InfoFile,TimeTask
from taskType.models import RunTask,FileDownload
from codeStandard.models import DataBase,RecognInfo,DataType
from .models import ApiData,InfoSqlFile
from .models import Dommana
from django.db.models import Q
from taskApp import gobal
import time
import random
import json
import os
from django.http import JsonResponse
import pymysql
import os.path
# Create your views here.
# 采集节点管理
def cjjdglIndex(request):
    return render_to_response('taskApp/cjjdglIndex.html')

# 采集json数据
def cjjdgl(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    all_state = ''
    task_data = BaseType.objects.all()
    cjData = Dommana.objects.all()[start:end]
    for num in range(len(cjData)):
        i = 0
        k=0
        j=0
        for td in task_data:
            if td.domid == cjData[num].cjdomid:
                if td.taskstate =='0':
                   i+=1
                if td.taskstate == '1':
                    k+=1
                if td.taskstate == '2':
                    j+=1
        all_state = '启用'+str(i)+" "+'停用'+str(k)+" "+'正在采集'+str(j)
        dn = Dommana.objects.get(cjdomid=cjData[num].cjdomid)
        dn.state =all_state
        dn.save()
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Dommana.objects.filter(cjdomname__icontains=request.POST.get('condition')).count()
        data = Dommana.objects.filter(cjdomname__icontains=request.POST.get('condition'))[start:end]
    else:
        counts = Dommana.objects.all().count()
        data = Dommana.objects.all()[start:end]
    list = []

    for num in range(len(data)):
        temp = {
            'cjdomid': data[num].cjdomid,
            'cjdomname': data[num].cjdomname,
            'region': data[num].region,
            'statetype':data[num].state,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

# 增加采集节点
def addjdTask(request):
    domname=request.POST['domname']
    domregion=request.POST['domregion']
    dommanaData = Dommana.objects.all()
    do=Dommana()
    domid = str(random.random())[2:7]
    while 1:
        i = 0
        for d in dommanaData:
            if d.cjdomid == domid:
                i = 1
        if i == 1:
            domid = int(domid) + random.random()[2:3]
            domid = str(domid)
        else:
            break
    do.cjdomid = domid
    do.cjdomname = domname
    do.region = domregion
    do.save()
    return HttpResponse(json.dumps(111), content_type='application/json')

#节点删除
def cjjdglDel(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Dommana.objects.extra(where=['cjdomid IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/cjjdglIndex/')

# 查看任务详情
def sjyglIndex(request):
    gobal.dataid = request.GET['data']
    return render_to_response("taskApp/sjyglIndex.html")

def newSjygl(request):
    dom=Dommana.objects.get(cjdomid=gobal.dataid)
    gobal.domname=dom.cjdomname
    return render_to_response("taskApp/sjyglIndex.html",{'domname':gobal.domname})

def initExecCutionFre(param):
    i = ''
    if param.rate == 'week':
        t = tuple(param.runtime)
        for tt in t:
            if tt != ']' and tt != '[' and tt != "'" and tt != ',':
                i += tt + ','
        run = '每周' + i + " |" + " " + param.hours + "时" + param.minutes + '分'
    if param.rate == 'mon':
        t = tuple(param.runtime)
        run = '每月' + param.runtime + '日' + " " + " |" + " " + param.hours + "时" + param.minutes + '分'
    if param.rate == 'day':
        run = '每天' + " " + param.hours + "时" + param.minutes + '分'
    if param.rate == 'interv':
        run = '间隔' + " " + param.runtime + "天" + param.hours + "时" + param.minutes + '分'
    if param.schedule == '2':
        run = param.runtime + '执行'
    if param.schedule=='3':
        run='手动执行'
    return run

# 采集任务传数据
def sjygl(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    tk = TimeTask.objects.all()
    baseData = BaseType.objects.filter(domid=gobal.dataid)
    run =''
    for num in range(len(baseData)):
        for td in tk:
            if td.taskid == baseData[num].taskid:
                run = initExecCutionFre(td)
                bt = BaseType.objects.get(taskid=baseData[num].taskid)
                bt.state_run = run
                bt.save()
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = BaseType.objects.filter(taskname__icontains=request.POST.get('condition')).count()
        data = BaseType.objects.filter(taskname__icontains=request.POST.get('condition'))[start:end]

    else:
        counts = BaseType.objects.filter(domid=gobal.dataid).count()
        data =BaseType.objects.filter(domid=gobal.dataid)[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'taskid': data[num].taskid,
            'taskname': data[num].taskname,
            'tasktype': data[num].filetype,
            'taskstate': data[num].taskstate,
            'run_state': data[num].state_run,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

# 任务删除
def sjyglDel(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    ids=idstring
    idstringIndex=idstring.split(',')
    for i in idstringIndex:
        ift=BaseType.objects.get(taskid=i)
        if ift.filetype=='1':
            InfoFile.objects.get(taskid=i).delete()
        if ift.filetype=='2':
            InfoSqlFile.objects.get(taskid=i).delete()
        if ift.filetype=='3':
            DataInterface.objects.get(id=i).delete()
        if ift.filetype=='4':
            ApiData.objects.get(taskid=i).delete()
        if ift.filetype == '5':
            FileDownload.objects.get(taskid=i).delete()
        try:
            RunTask.objects.get(where=['taskid IN (' + i + ')']).delete()
        except:
            print('no data')
        BaseType.objects.get(taskid=i).delete()
    # BaseType.objects.extra(where=['taskid IN (' + ids + ')']).delete()

    return HttpResponseRedirect('/sjyglIndex/newSjygl/')


# 查看采集日志
def collectLogIndex(request):
    return render_to_response('taskApp/collectLogIndex.html',{'domname':gobal.domname})

def collection(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        baseData = BaseType.objects.filter(taskname__icontains=request.POST.get('condition'))[start:end]
        long = len(baseData)
        if long != 0:
            for i in range(len(baseData)):
                counts = RunTask.objects.filter(taskid=baseData[i].taskid).count()
                data = RunTask.objects.filter(taskid=baseData[i].taskid)[start:end]
        else:
            data = []
            counts = 0
    else:
        counts = RunTask.objects.filter(domid=gobal.dataid).count()
        data = RunTask.objects.order_by('-id').filter(domid=gobal.dataid)[start:end]
        baseData = BaseType.objects.all()
    list = []
    type = '0'
    taskname=''
    for num in range(len(data)):
        for bd in baseData:
            if data[num].taskid==bd.taskid:
                   type = bd.filetype
                   taskname = bd.taskname
                   break
        temp = {
            'taskid': data[num].taskid,
            'starttime': data[num].starttime,
            'endtime': data[num].endtime,
            'state': data[num].state,
            'taskname':taskname,
            'type':type,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

def domSearch(request):
    dataSearch=request.GET['dataSearch']
    searchResult=Dommana.objects.get(cjdomid=dataSearch)
    list=[]
    temp = {
        'cjdomid': searchResult.cjdomid,
        'cjdomname': searchResult.cjdomname,
        'region': searchResult.region,
    }
    list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')

# 修改采集节点
def changeDom(request):
    cjdomname = request.POST['cjdomname_change']
    cjregion = request.POST['cjregion_change']
    cjdomid = request.POST['cjdomid_change']
    dos = Dommana.objects.get(cjdomid=cjdomid)
    dos.cjdomname = cjdomname
    dos.region = cjregion
    dos.save()
    return HttpResponse(json.dumps(cjdomname), content_type='application/json')

def sjyglBelongType(request):
    s_list = DataType.objects.all()
    list = []
    for i in s_list:
        temp = {
            'dataid': i.dataname,
            'dataname': i.dataname,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')

def sjyglBelongto(request):
    s_list = RecognInfo.objects.all()
    list = []
    for i in s_list:
        temp = {
            'recognid': i.recognname,
            'recognname': i.recognname,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')

#修改
def taskInfo(request):
    task_id = request.GET['data']
    s_list = BaseType.objects.get(taskid=task_id)
    list=[]
    temp = {
        'taskid': s_list.taskid,
        'taskname': s_list.taskname,
        'belongtype': s_list.belongtype,
        'filetype': s_list.filetype,
        'belongto': s_list.belongto,
        'domid': s_list.domid,
        'refreshChange': s_list.state_run,
    }
    list.append(temp)
    if s_list.filetype=='1':
        fileData = InfoFile.objects.filter(taskid=task_id)
        for f in fileData:
            ftemp = {
            'sfiletype':f.tasktype,
            'fileway':f.fileway,
            'filename':f.filename,
            }
            list.append(ftemp)
    if s_list.filetype=='2':
        sqlData = InfoSqlFile.objects.filter(taskid=task_id)
        for s in sqlData:
            sqlTemp = {
                'tasktype':s.tasktype,
                'filename':s.filename,
                'fileway':s.fileway,
            }
            list.append(sqlTemp)
    if s_list.filetype=='3':
            sqlData = DataInterface.objects.filter(id=task_id)
            for d in sqlData:
                newTemp = {
                    'sjyname':d.sjyname,
                    'databasename':d.databasename,
                    'databasetype':d.databasetype,
                    'fwqadress':d.fwqadress,
                    'dkname':d.dkname,
                    'username':d.username,
                    'pwd':d.pwd,
                    'tablename':d.tablename,
                    'ziduanname':d.ziduanname,

                }
                list.append(newTemp)
    if s_list.filetype=='4':
        apidata = ApiData.objects.filter(taskid=task_id)
        for a in apidata:
            tempApi = {
                'url':a.url,
                'filetype':a.filetype,
                'byteamount':a.byteamount,
                'apitype':a.apitype,
                'param':a.paramate,
            }
            list.append(tempApi)
    if s_list.filetype=='5':
        download_data = FileDownload.objects.filter(taskid=task_id)
        for da in download_data:
            tempApi = {
                'ip': da.ipinfo,
                'pwd': da.pwdinfo,
                'path': da.pathinfo,
                'user': da.userinfo,
            }
            list.append(tempApi)

    return HttpResponse(json.dumps(list),content_type='application/json')

#修改数据库数据
def updateData(request):
    task_id = request.GET.get('taskId')
    task_type = request.GET.get('fileType')
    task_reco = request.GET.get('belong')
    belong_type = request.GET.get('belType')
    task_name = request.GET.get('taskName')
    bt = BaseType.objects.get(taskid=task_id)
    if task_type=='3':
        dt = DataInterface.objects.get(id=task_id)
        db_Sour = request.GET.get('dataSoure')
        db_ip = request.GET.get('connIp')
        ip_port = request.GET.get('port')
        uName = request.GET.get('userName')
        user_pwd = request.GET.get('userPwd')
        dt.sjyname = db_Sour
        dt.fwqadress = db_ip
        dt.dkname = ip_port
        dt.username = uName
        dt.pwd = user_pwd
        dt.save()
    if task_type=='4':
        apd = ApiData.objects.get(taskid=task_id)
        url_ad = request.GET.get('urlAd')
        method_url = request.GET.get('useMethod')
        para = request.GET.get('param')
        btamout = request.GET.get('byteAmout')
        saveType = request.GET.get('saveType')
        apd.url = url_ad
        apd.filetype = saveType
        apd.byteamount = btamout
        apd.apitype = method_url
        apd.paramate = para
        apd.save()
    if task_type=='5':
        fd = FileDownload.objects.get(taskid=task_id)
        dow_ip = request.GET.get('downloadIp')
        user_name = request.GET.get('dUsername')
        dow_pwd = request.GET.get('downloadPwd')
        dow_path = request.GET.get('dfileNameWay')
        fd.ipinfo = dow_ip
        fd.pwdinfo = dow_pwd
        fd.pathinfo = dow_path
        fd.userinfo = user_name
        fd.save()
    bt.taskname =task_name
    bt.belongto = task_reco
    bt.belongtype = belong_type
    bt.save()
    return  HttpResponse('ok')

#测试数据库连接
def testConn(request):
    task_ip = request.GET.get('connIp')
    task_port = request.GET.get('port')
    user_name = request.GET.get('userName')
    pwd = request.GET.get('userPwd')
    databaseN = request.GET.get('dbName')
    conn = pymysql.connect(host=task_ip, port=int(task_port), user=user_name, password=pwd, db=databaseN, charset='utf8')
    cur = conn.cursor()
    cur.close()
    return HttpResponse(json.dumps(1), content_type='application/json')

def getCollectTable(request):
    str = BaseType.objects.all()
    dom = DataInterface.objects.all()
    list = []
    for i in str:
        print (i)
        for j in dom:
           print (j)
           if i.taskid == j.id:
                temp = {
                    'value':j.tablename+j.id,
                    'text':i.taskname,
                }
                list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')

# 修改频率
def updataRefesh(request):
    task_id = request.GET.get('taskId')
    #print(task_id)
    # 定时刷新保存到Timetask表
    dataInfo = BaseType.objects.get(taskid=task_id)
    modifyId=dataInfo.taskid
    FreSetting = request.GET['FreSetting']
   # print(type(FreSetting))
    if FreSetting == '1':
        cycle = request.GET['cycle']
        if cycle == '1':
            cycle = 'mon'
            days = request.GET['days']
            d = days[1:-1]
            hours = request.GET['hours']
            h = hours[1:-1]
            minutes = request.GET['minutes']
            m = minutes[1:-1]
            tt = TimeTask.objects.get(taskid=modifyId)
            tt.schedule = FreSetting
            tt.rate = cycle
            tt.runtime = d
            tt.hours = h
            tt.minutes = m
            tt.save()
        elif cycle == '2':
            cycle = 'week'
            week_day = request.GET.getlist('week_day')
            hours = request.GET['hours']
            h = hours[1:-1]
            minutes = request.GET['minutes']
            m = minutes[1:-1]
            tt = TimeTask.objects.get(taskid=modifyId)
            tt.schedule = FreSetting
            tt.rate = cycle
            tt.runtime = week_day
            tt.hours = h
            tt.minutes = m
            tt.save()
        elif cycle == '3':
            cycle = 'day'
            hours = request.GET['hours']
            h = hours[1:-1]
            minutes = request.GET['minutes']
            m = minutes[1:-1]
            tt = TimeTask.objects.get(taskid=modifyId)
            tt.schedule = FreSetting
            tt.rate = cycle
            tt.hours = h
            tt.minutes = m
            tt.save()
    elif FreSetting == '2':
        once_time = request.GET['once_time']
        tt = TimeTask.objects.get(taskid=modifyId)
        tt.schedule = FreSetting
        tt.runtime = once_time
        tt.save()
    elif FreSetting == '3':
        tt = TimeTask.objects.get(taskid=modifyId)
        tt.schedule='3'
        tt.rate=''
        tt.runtime=''
        tt.hours=''
        tt.minutes=''
        tt.save()
        print('run by yourself')
    elif FreSetting == '4':
        cycle = 'interv'
        interval_day = request.GET['interval_day']
        i = interval_day[1:-1]
        hours = request.GET['hours']
        h = hours[1:-1]
        minutes = request.GET['minutes']
        m = minutes[1:-1]
        tt = TimeTask.objects.get(taskid=modifyId)
        tt.taskid = dataInfo.taskid
        tt.schedule = FreSetting
        tt.runtime = i
        tt.rate = cycle
        tt.hours = h
        tt.minutes = m
        tt.save()

    run = initExecCutionFre(tt)
    return HttpResponse(json.dumps(run),content_type='application/json')

