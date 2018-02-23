# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse,JsonResponse ,HttpResponseRedirect
from django.conf import settings
from .models import Table1,Table1Display
from .models import Table2,Table2Display
from .models import Table4,Table4Display
from .models import Table5,Table5Display
from .models import Table6,Table6Display
from .models import Parameters,ParametersDisplay
from .models import Totable,TotableDisplay
from .models import Rules,RulesDisplay
from .models import Log,LogDisplay
from .models import Base,BaseDisplay
from .models import BasicTesting,TestMethod
from dataQualityManagement import gobal
from django.http import JsonResponse
import json
import os,time, random
import pymysql
import os.path
import re
#from .models import FangAn, FangAnPlanMag, TestMethod
from datetime import datetime
from catalogueManagement.models import Catalogue
from releaseRegisterManagement.models import FieldTable
from dataCleaningRules.models import CheckRule
from .models import TestMethod
from .models import OftenRules
from .models import BasicTesting
from releaseRegisterManagement.models import MasterdataTable
import logging
logger=logging.getLogger('sourceDns.webdns.views')

# Create your views here.
#数据质量检测管理主页面
def index(request):
    return render_to_response('dataQualityManagement/index.html')

#第一个选项卡
# 加载数据 # 点击datagrid的分页按钮，自动向后台发送2个参数, rows和page，代表每页记录数和页索引
def showData(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    #create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Table1.objects.filter(id=request.POST.get('condition')).count()
        data = Table1.objects.filter(id=request.POST.get('condition'))[start:end]
    else:
        counts = Table1.objects.all().count()
        data = Table1.objects.all()[start:end]
    list = []
    for num in range(len(data)):          #遍历
        # data[num].create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # data[num].save()
        temp={
            'methodname':data[num].methodname,
            'methodtype':data[num].methodtype,
            'predefinedmethod':data[num].predefinedmethod,
            'createtime':data[num].createtime,
            'id': data[num].id,
            'checkfun': data[num].checkfun,
            'methoddetail': data[num].methoddetail,


        }
        list.append(temp)
    #return HttpResponse(6)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据
# 后台增加方法
def addData(request):
    methodname=request.POST['methodname']
    methodtype=request.POST['methodtype']
    predefinedmethod = request.POST['predefinedmethod']
    methoddetail = request.POST['methoddetail']
    createtime= time.strftime("%Y-%m-%d %X", time.localtime())
    tb1=Table1()
    tb1.methodname = methodname
    tb1.methodtype = methodtype
    tb1.predefinedmethod = predefinedmethod
    tb1.methoddetail = methoddetail
    tb1.createtime = createtime
    tb1.save()
    #return HttpResponseRedirect('/dataQualityManagement/index/')
    return HttpResponse(json.dumps(1), content_type='application/json')

#后台删除方法
def delData(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Table1.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityManagement/index/')


# 后台修改方法
def changeMet(request):
    methodname = request.POST['methodnamechange']
    methodtype = request.POST['methodtypechange']
    predefinedmethod = request.POST['predefinedmethodchange']
    id = request.POST['idchange']
    dos = Table1.objects.get(id=id)
    dos.methodname = methodname
    dos.methodtype = methodtype
    dos.id=id
    dos.predefinedmethod = predefinedmethod
    dos.save()
    return HttpResponse(json.dumps(2), content_type='application/json')
#详情对话框
def loadList(request):
    data_list = Parameters.objects.all()  # 将“Parameters”表中的数据以data_list获取出来
    list=[]
    for d in data_list:            #用 d来遍历data_list
        temp={
                'id':d.id,         #引号中的内容是dataMonnitoringStatistics.js中fieled后面引号中的内容，是js与后台数据库建立联系的关键。“d.”是后台数据库中相应表的字段，即models中表的相应字段
                'parametername':d.parametername,
                'parameterchinese':d.parameterchinese,
                'parametertype':d.parametertype,
                'datatype': d.datatype,
                'defaultvalue': d.defaultvalue,
                'remark': d.remark,
                'nonempty': d.nonempty,
                  }
        list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')                      #返回的格式，。为固定格式。只有导入json之后在可以用
#检测对话框
def loadList2(request):
    data_list = Parameters.objects.all()  # 将“Parameters”表中的数据以data_list获取出来
    list=[]
    for d in data_list:            #用 d来遍历data_list
        temp={
                'id':d.id,         #引号中的内容是dataMonnitoringStatistics.js中fieled后面引号中的内容，是js与后台数据库建立联系的关键。“d.”是后台数据库中相应表的字段，即models中表的相应字段
                'parametername':d.parametername,
                'parameterchinese':d.parameterchinese,
                'parametertype':d.parametertype,
                'datatype': d.datatype,
                'defaultvalue': d.defaultvalue,
                'remark': d.remark,
                'nonempty': d.nonempty,
                  }
        list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')                      #返回的格式，。为固定格式。只有导入json之后在可以用


#第二个选项卡
def showData2(request):             #主页面第二个选项卡显示数据
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Table2.objects.filter(id=request.POST.get('condition')).count()
        data = Table2.objects.filter(id=request.POST.get('condition'))[start:end]
    else:
        counts = Table2.objects.all().count()
        data = Table2.objects.all()[start:end]
    list = []
    for num in range(len(data)):  # 遍历
        temp = {
            'rulename':data[num].rulename,
            'methodname':data[num].methodname,
            'identifier':data[num].identifier,
            'chinesename':data[num].chinesename,
            'datatype': data[num].datatype,
            'id':data[num].id,
              }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据
# 增加
def addData2(request):
    rulename=request.POST['rulename']
    identifier = request.POST['identifier']
    chinesename = request.POST['chinesename']
    datatype = request.POST['datatype']
    tb2=Table2()
    tb2.rulename = rulename
    tb2.identifier = identifier
    tb2.chinesename = chinesename
    tb2.datatype = datatype
    tb2.save()
    return HttpResponseRedirect('/dataQualityManagement/index/')
#删除
def delData2(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Table2.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityManagement/index/')
# 修改
def changeRul(request):
    rulename = request.POST['rulenamechange']
    object = request.POST['objectchange']
    identifier = request.POST['identifierchange']
    chinesename = request.POST['chinesenamechange']
    datatype = request.POST['datatypechange']
    ruletype = request.POST['ruletypechange']
    methodname = request.POST['methodnamechange']
    id = request.POST['idchange']
    dos = Table2.objects.get(id=id)
    dos.rulename = rulename
    dos.object = object
    dos.identifier = identifier
    dos.chinesename = chinesename
    dos.datatype = datatype
    dos.ruletype = ruletype
    dos.methodname = methodname
    dos.save()
    return HttpResponse(json.dumps(rulename), content_type='application/json')
#增加对话框
def loadList21(request):
    data_list = Parameters.objects.all()  # 将“Parameters”表中的数据以data_list获取出来
    list=[]
    for d in data_list:            #用 d来遍历data_list
        temp={
                'id':d.id,         #引号中的内容是dataMonnitoringStatistics.js中fieled后面引号中的内容，是js与后台数据库建立联系的关键。“d.”是后台数据库中相应表的字段，即models中表的相应字段
                'parametername':d.parametername,
                'parameterchinese':d.parameterchinese,
                'parametertype':d.parametertype,
                'datatype': d.datatype,
                'defaultvalue': d.defaultvalue,
                'remark': d.remark,
                'nonempty': d.nonempty,
                  }
        list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')                      #返回的格式，。为固定格式。只有导入json之后在可以用


# 第三个选项卡
def showData3(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Base.objects.filter(id=request.POST.get('condition')).count()
        data = Base.objects.filter(id=request.POST.get('condition'))[start:end]
    else:
        counts = Base.objects.all().count()
        data = Base.objects.all()[start:end]
    list = []
    for num in range(len(data)):  # 遍历
        temp = {
            'schemename': data[num].schemename,
            'methodname': data[num].methodname,
            'card': data[num].card,
            'dotime': data[num].dotime,
            'id': data[num].id,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})  # 返回json数据
#删除
def delData3(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Base.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityManagement/index/')
# 修改
def changeBas(request):
    schemename = request.POST['schemenamechange']
    checkobject = request.POST['checkobjectchange']
    schemetype = request.POST['schemetypechange']
    id = request.POST['id']
    dos = Base.objects.get(id=id)
    dos.schemename = schemename
    dos.checkobject = checkobject
    dos.schemetype = schemetype
    dos.id = id
    dos.save()
    return HttpResponse(json.dumps(schemename), content_type='application/json')
#取对话框数据

#新增监测方案
def baseschedum(request):
    return render_to_response('dataQualityManagement/addindex.html')

def add(request):
    datasource = request.POST['datasource']
    keyword = request.POST['keyword']
    ruletype = request.POST['ruletype']
    methodname = request.POST['methodname']
    card = request.POST['card']
    rulename =  request.POST['rulename']

    schemename = request.POST['schemename']
    inputperson = request.POST['inputperson']
    detail = request.POST['detail']
    schedumplan = request.POST['schedumplan']
    dotime = request.POST['dotime']
    starttime = request.POST['starttime']
    endtime = request.POST['endtime']

    l3=Base()
    l3.schemename = schemename
    l3.inputperson = inputperson
    l3.detail = detail
    l3.schedumplan = schedumplan
    l3.dotime = dotime
    l3.starttime = starttime
    l3.endtime = endtime
    l3.ruletype = ruletype
    l3.methodname = methodname
    l3.card = card
    l3.keyword = keyword
    l3.datasource = datasource
    l3.rulename = rulename
    l3.save()
    return HttpResponseRedirect('/dataQualityManagement/index/')


def showData5(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Table5.objects.filter(id=request.POST.get('condition')).count()
        data = Table5.objects.filter(id=request.POST.get('condition'))[start:end]
    else:
        counts = Table5.objects.all().count()
        data = Table5.objects.all()[start:end]
    list = []
    for num in range(len(data)):  # 遍历
        temp = {
            'schemename': data[num].schemename,
            'rulename': data[num].rulename,
            'methodname': data[num].methodname,
            'lastexecutionstatus': data[num].lastexecutionstatus,
            'starttime': data[num].starttime,
            'currentstatus': data[num].currentstatus,
            'id': data[num].id,
            'taskstate':data[num].taskstate,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})  # 返回json数据
# 未激活
def stateStop(request):
    id = request.GET['data']
    stateStartId=Table5.objects.get(id=id)
    stateStartId.taskstate = 0
    stateStartId.currentstatus=0
    stateStartId.lastexecutionstatus = 0
    stateStartId.save()
    return HttpResponse('ok')

# 激活
def stateStart(request):
    id = request.GET['data']
    lastexecutiontime = time.strftime("%Y-%m-%d %X", time.localtime())
    stateStartId=Table5.objects.get(id=id)
    stateStartId.taskstate = 2
    stateStartId.currentstatus = 2
    stateStartId.lastexecutiontime = lastexecutiontime
    stateStartId.lastexecutionstatus = 2

    stateStartId.save()
    return HttpResponse('ok')



# 立即执行
def runNow(request):
    id=request.GET['data']
    runNowId=Table5.objects.get(id=id)
    schemename = runNowId.schemename
    card = runNowId.card
    starttime = runNowId.starttime
    endtime = runNowId.endtime

    str1 = card
    str2 = 18
    # 用len()内置函数来取字符串长度
    if len(str1) == str2:
        result = '成功'
    else:
        result = '失败'


    table = Log()
    table.state=result
    table.schemename=schemename
    table.starttime=starttime
    table.endtime = endtime
    table.card = card

    table.save()
    return HttpResponse(json.dumps('99'), content_type='application/json')

# 增加
def addData5(request):
    schemename=request.POST['schemename']
    methodname=request.POST['methodname']
    rulename = request.POST['rulename']
    lastexecutionstatus = request.POST['lastexecutionstatus']
    taskstate = request.POST['taskstate']
    starttime = request.POST['starttime']
    endtime = request.POST['endtime']
    card = request.POST['card']


    tb5=Table5()
    tb5.schemename = schemename
    tb5.methodname = methodname
    tb5.rulename = rulename
    tb5.lastexecutionstatus = lastexecutionstatus
    tb5.taskstate = taskstate
    tb5.starttime = starttime
    tb5.endtime = endtime
    tb5.card = card


    tb5.save()
    return HttpResponseRedirect('/dataQualityManagement/index/')
#删除
def delData5(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Table5.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityManagement/index/')

# 修改
def changeTas(request):
    schemename = request.POST['schemenamechange2']
    rulename = request.POST['rulenamechange2']
    methodname = request.POST['methodnamechange2']
    id = request.POST['idchange2']
    dos = Table5.objects.get(id=id)
    dos.schemename = schemename
    dos.rulename = rulename
    dos.methodname = methodname
    dos.id = id
    dos.save()
    return HttpResponse(json.dumps(methodname), content_type='application/json')

#删除日志
def delData6(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Log.objects.extra(where=['id IN (' + idstring + ')']).delete()
    #Log.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityManagement/index/')

#删除Table6
def deData6(request):
    stp = request.GET.getlist("data")
    print(stp)
    idstring = ','.join(stp)
    Table6.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityManagement/index/')

#查看日志
def logList(request):
    return render_to_response('dataQualityManagement/logindex.html')

def loadList6(request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        # create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = Log.objects.filter(id=request.POST.get('condition')).count()
            data = Log.objects.filter(id=request.POST.get('condition'))[start:end]

        else:
            counts = Log.objects.all().count()
            data = Log.objects.all()[start:end]
        list = []
        print(len(data))
        for num in range(len(data)):  # 遍历
            temp = {
                'id': data[num].id,
                'schemename': data[num].schemename,
                'starttime': data[num].starttime,
                'endtime': data[num].endtime,
                'state': data[num].state,
                'card': data[num].card,

            }
            list.append(temp)
        # return HttpResponse(6)
        return JsonResponse({'total': counts, 'rows': list})  # 返回json数据




#检验方法管理
#---------------------------------------------caibin--------------------------------------------

def getMethodList(request):
    rows = int(request.GET.get('rows', 10))
    page = int(request.GET.get('page', 1))
    start = (page - 1) * rows
    end = page * rows
    data = request.POST.get('condition', '')
    if data != '':
        object = TestMethod.objects.filter(method_name__contains=data)[start:end]
        total = TestMethod.objects.filter(method_name__contains=data).count()
    else:
        object = TestMethod.objects.all()[start:end]
        total = TestMethod.objects.all().count()

    rows = []
    for row in object:
        if row.method_type == '1':
            m_type = '空值校验'
        elif row.method_type == '2':
            m_type = '格式校验'
        elif row.method_type == '3':
            m_type = '范围校验'
        elif row.method_type == '4':
            m_type = '长度校验'
        elif row.method_type == '5':
            m_type = '字段间逻辑校验'
        elif row.method_type == '6':
            m_type = '代码校验'
        elif row.method_type == '7':
            m_type = '唯一性校验'
        elif row.method_type == '8':
            m_type = '表间一致性校验'
        elif row.method_type == '9':
            m_type = '引用完整性校验'
        elif row.method_type == '10':
            m_type = '其它'
        str11 = str(row.createtime)
        temp = {
            'id': row.id,
            'Method_name': row.method_name,
             'Method_type': m_type,
            'Predef_method': row.predef_method,
            'Createtime': str11,
            'Func_code': row.func_code,
            'M_description': row.m_description
        }
        rows.append(temp)
    return JsonResponse({'total': total, 'rows': rows}, content_type='application/json')


def method_save(request):
    data = request.POST
    user = TestMethod()
    method_type = data.get('Method_type')
    if method_type == '1' or method_type == '空值校验':
        method_type = '1'
    elif method_type == '2' or method_type == '格式校验':
        method_type = '2'
    elif method_type == '3' or method_type == '范围校验':
        method_type = '3'
    elif method_type == '4' or method_type == '长度校验':
        method_type = '4'
    elif method_type == '5' or method_type == '字段间逻辑校验':
        method_type = '5'
    elif method_type == '6' or method_type == '代码校验':
        method_type = '6'
    elif method_type == '7' or method_type == '唯一性校验':
        method_type = '7'
    elif method_type == '8' or method_type == '表间一致性校验':
        method_type = '8'
    elif method_type == '9' or method_type == '引用完整性校验':
        method_type = '9'
    elif method_type == '10' or method_type == '其它':
        method_type = '10'

    # fields = TestMethod._meta.get_fields()

    # for field in fields:
    #     setattr(user, field.name, data.get(field.name))
    user.method_name = data.get('Method_name')
    user.method_type = method_type
    user.predef_method = data.get('Predef_method')
    user.m_description = data.get('M_description')
    user.createtime = datetime.now()
    
    fields = TestMethod.objects.all()

    if data.get('id') == '':
        user.id = None
        for field in fields:
            if field.method_name == data.get('Method_name'):
                return JsonResponse({'errorCode': '0x0001', 'errorString': '规则名称不能重复！'})
    else:
        user.id = data.get('id')
        if data.get('Method_name') != TestMethod.objects.get(id=data.get('id')).method_name:
            for field in fields:
                if field.method_name == data.get('Method_name'):
                    return JsonResponse({'errorCode': '0x0001', 'errorString': '规则名称不能重复！'})
    if data.get('id') == '':
        user.id = None
    else:
        user.id = data.get('id')

    try:
        user.save()

    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '失败'})
    return JsonResponse({'errorCode': '0x0000', 'errorString': '成功'})

def method_delete(request):
    IDs = request.POST.get('ids')
    try:
        TestMethod.objects.extra(where=['id in (' + IDs + ')']).delete()
    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '失败'})

    return JsonResponse({'errorCode': '0x0000', 'errorString': '成功'})

#---------------------------------------------caibin--------------------------------------------

#---------------------------------------------方国巍--------------------------------------------
def dataTaskMag(request):
    return render(request, 'dataTaskMag.html')                                 #测试主页


def getDataTaskMagList(request):                                             #用户信息内容
    rows = int(request.POST.get('rows', 10))
    page = int(request.POST.get('page', 1))
    start = (page - 1) * rows
    end = page * rows
    object = BasicTesting.objects.all()[start:end]
    total = BasicTesting.objects.all().count()
    rows = []
    for row in object:
        temp = {
            'id':row.id,
                        'SchemeName':row.SchemeName,
            'flag': row.flag,
                        'SchedulingPlan': row.SchedulingPlan,
            'Current_State': row.Current_State,
                        'CheckField': row.CheckField,
                        'CheckMethod_id': row.CheckMethod_id,
                        'MethodName':TestMethod.objects.get(id=row.CheckMethod_id).method_name,
        }
        rows.append(temp)
    return JsonResponse({'total': total, 'rows': rows}, content_type='application/json')


def taskMagActivation(request):
    taskMagActivation = request.POST
    data = taskMagActivation.get('data')
    try:        
        tmp= data.split()
        ids=''
        ids=tmp[0]

        object = BasicTesting.objects.get(id = str(ids))
        Flag = tmp[1]
        object.flag = int(Flag)
        # Current_State=0 未激活  Current_State=1 执行失败 Current_State=10 准备执行   Current_State=11 正在执行   Current_State=12 执行完成  其他等于0
        if Flag == '0':
            object.Current_State = '未激活'
        elif Flag == '1':
            object.Current_State = '执行失败'
        elif Flag == '10':
            object.Current_State = '激活'
        elif Flag == '11':
            object.Current_State = '正在执行'
        elif Flag == '12':
            object.Current_State = '执行完成'
        else:
            object.Current_State = '未激活'

        object.save()
    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': 'F','da':data})
    return JsonResponse({'errorCode': '0x0000', 'errorString': 'T','ids':ids,'flag':object.flag,'Current_State':object.Current_State})


def saveTaskMag(request):
    data = request.POST
    try:
        object = BasicTesting.objects.get(id = data.get('ids'))
        SchedulingPlan=data.get('SchedulingPlan')
        if SchedulingPlan=='1':
            if data.get('cycle')=='1':
                object.SchedulingPlan = '每月：'+ data.get('days')+' 工作时间 ' + data.get('hours') +':' + data.get('minutes')


            if data.get('cycle')=='2':
                object.SchedulingPlan = '每周：'+ data.get('week_day')+' 工作时间 ' + data.get('hours') +':' + data.get('minutes')
            if data.get('cycle')=='3':
                object.SchedulingPlan = '每日：工作时间 '+ data.get('hours') +':' + data.get('minutes')

        if SchedulingPlan=='2':
            object.SchedulingPlan = '工作时间 '+ data.get('once_time')

        if SchedulingPlan=='3':
            object.SchedulingPlan = '手动'

        if SchedulingPlan=='4':
            object.SchedulingPlan = '时间间隔：'+ data.get('intervalDay')+' 工作时间 ' + data.get('hours') +':' + data.get('minutes')



        object.save()

    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': 'F','s':data})
    return JsonResponse({'errorCode':'0x0000','errorString':'T'})

   
#----------------------------------------------方国巍-------------------------------------------



#---------------------------------------------常用规则设置-------------------------------------------

def oftenRules_getRulesList(request):
    #常用规则设置----list
    rows = int(request.POST.get('rows', 10))
    page = int(request.POST.get('page', 1))
    start = (page - 1) * rows
    end = page * rows

    data = request.POST.get('condition', '')

    if data != '':
        object = OftenRules.objects.filter(rule_name__contains=data)[start:end]
        total = OftenRules.objects.filter(rule_name__contains=data).count()
    else:
        object = OftenRules.objects.all()[start:end]
        total = OftenRules.objects.all().count()


    rows = []

    for row in object:
        object_words = {}
        object_words['cid'] = row.object_words.typeid
        object_words['cname'] = row.object_words.cataloguename
        
        identifier = {}
        identifier['fid'] = row.identifier.id
        identifier['fname'] = row.identifier.fieldenglish
        
        rule_type = {}
        rule_type['hid'] = row.rule_type.id
        rule_type['hname'] = row.rule_type.name
        
        check_method = {}
        check_method['tid'] = row.check_method.id
        check_method['tname'] = row.check_method.method_name
        temp = {
            'id':row.id,
            'Rule_name': row.rule_name,
            'Object_words': object_words,
            'Identifier': identifier,
            'Chinese_name': row.chinese_name,
            'Data_type': row.data_type,
            'Rule_type': rule_type,
            'Check_method': check_method,
        }
        rows.append(temp)
    return JsonResponse({'total': total, 'rows': rows}, content_type='application/json')
    
def oftenRules_save(request):
    # 常用规则设置----save
    data = request.POST
    rules = OftenRules()

    fields = OftenRules.objects.all()

    if data.get('id') == '':
        rules.id = None
        for field in fields:
            if field.rule_name == data.get('Rule_name'):
                return JsonResponse({'errorCode': '0x0001', 'errorString': '规则名称不能重复！'})
    else:
        rules.id = data.get('id')
        if data.get('Rule_name') != OftenRules.objects.get(id=data.get('id')).rule_name:
            for field in fields:
                if field.rule_name == data.get('Rule_name'):
                    return JsonResponse({'errorCode': '0x0001', 'errorString': '规则名称不能重复！'})

    if data.get('Rule_name') != '':
        rules.rule_name = data.get('Rule_name')
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '规则名称不能为空！'})

    if data.get('Chinese_name') != '':
        rules.chinese_name = data.get('Chinese_name')
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '中文名称不能为空！'})

    if data.get('Data_type') != '':
        rules.data_type = data.get('Data_type')
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': ' 数据类型不能为空！'})

    if data.get('Check_method') != '':
        rules.check_method = TestMethod.objects.get(id = data.get('Check_method'))
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '校验方法不能为空！'})

    if data.get('Object_words') != '':
        rules.object_words = Catalogue.objects.get(typeid = data.get('Object_words'))
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '对象类词不能为空！'})

    if data.get('Identifier') != '':
        rules.identifier = FieldTable.objects.get(id = data.get('Identifier'))
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '标识符不能为空！'})

    if data.get('Rule_type') != '':
        rules.rule_type = CheckRule.objects.get(id = data.get('Rule_type'))
    else:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '规则类型不能为空！'})

    if not re.match('^[\u0391-\uFFE5]+$', rules.chinese_name):
        return JsonResponse({'errorCode': '0x0001', 'errorString': '中文名称只能输入中文'})

    try:
        rules.save()
    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '失败'})
    return JsonResponse({'errorCode':'0x0000','errorString':'成功'})
    

def oftenRules_delete(request):
    #常用规则设置----delete
    ids = request.POST.get('ids')
    try:
        OftenRules.objects.extra(where=['id in (' + ids + ')']).delete()
    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '失败'})

    return JsonResponse({'errorCode':'0x0000','errorString':'成功'})



def getObject(request):
    # 对象词类下拉框
    data = FieldTable.objects.all()
    lst = []
    for num in data:
        temp = {
            'Object_words': num.object
        }
        lst.append(temp)
    from functools import reduce
    func = lambda x, y: x if y in x else x + [y]
    lst = reduce(func, [[], ] + lst)
    return HttpResponse(json.dumps(lst), content_type='application/json')

def getFieldTable(request):
    # 标识符下拉框
    data = FieldTable.objects.filter(object = request.POST.get('Object_words'))
    lists = []
    for num in range(len(data)):
        temp = {
            'ids': getattr(data[num], 'id'),
            'cnname': getattr(data[num], 'cnname'),
            'identifier': getattr(data[num], 'identifier'),
            'idf': getattr(data[num], 'identifier'),
            'canshu': getattr(data[num], 'cnname'),
            'daty': getattr(data[num], 'datatype'),
            'format': getattr(data[num], 'dataformat'),
            'rule': getattr(data[num], 'rule'),
        }
        lists.append(temp)
    return HttpResponse(json.dumps(lists), content_type='application/json')

def getcnname(request):
    # 标识符下拉框
    data = FieldTable.objects.filter(identifier = request.POST.get('identifier'))
    lists = []
    for num in range(len(data)):
        temp = {
            'ids': getattr(data[num], 'id'),
            'cnname': getattr(data[num], 'cnname'),
            'identifier': getattr(data[num], 'identifier'),

            'csm': getattr(data[num], 'enname'),
            'canshu': getattr(data[num], 'cnname'),
            'daty': getattr(data[num], 'datatype'),
            'format': getattr(data[num], 'dataformat'),
            'rule': getattr(data[num], 'rule'),
        }
        lists.append(temp)
    return HttpResponse(json.dumps(lists), content_type='application/json')

def getFieldList(request):
    rows = int(request.POST.get('rows', 10))
    page = int(request.POST.get('page', 1))
    start = (page - 1) * rows
    end = page * rows
    data = FieldTable.objects.all()[start:end]
    total = FieldTable.objects.all().count()
    rows = []
    for num in data:
        temp = {
            'ids': getattr(data[num], 'id'),
            'idf': getattr(data[num], 'identifier'),
            'canshu': getattr(data[num], 'cnname'),
            'daty': getattr(data[num], 'datatype'),
            'format': getattr(data[num], 'dataformat'),
            'rule': getattr(data[num], 'rule'),

        }
        rows.append(temp)
    return JsonResponse({'total': total, 'rows': rows}, content_type='application/json')


def getTestMethod(request):
    # 效验方法下拉框
    data = TestMethod.objects.all()
    lists = []
    for num in range(len(data)):
        temp = {
            'tid':getattr(data[num], 'id'),
            'tname':getattr(data[num], 'method_name'),
        }
        lists.append(temp)
    return HttpResponse(json.dumps(lists), content_type='application/json')

def getCheckRule(request):
    # 规则类型下拉框
    data = CheckRule.objects.all()
    lists = []
    for num in range(len(data)):
        temp = {
            'hid':getattr(data[num], 'id'),
            'hname':getattr(data[num], 'name'),
        }
        lists.append(temp)
    return HttpResponse(json.dumps(lists), content_type='application/json')
    

#---------------------------------------------常用规则设置-------------------------------------------
#基础检测方案管理模块

#1.获取校验对象列表
def getCheckObjectList(request):
    data = MasterdataTable.objects.all()
    mlist = []
    for num in range(len(data)):
        temp = {
            'tid': getattr(data[num], 'id'),
            'tcname': getattr(data[num], 'codename'),
        }
        mlist.append(temp)
    return HttpResponse(json.dumps(mlist), content_type='application/json')

#2.获取方案基本信息_20161208_wyw
def getSchemeBasicInfo(request):
    checkobj = MasterdataTable.objects.filter(id = request.GET.get('tid'))
    infodict={
        'famc':'['+getattr(checkobj, 'id')+']_基础质量检测',
        'zlzd':request.GET.get('tid'),
        'dwzd':'xxx',
        'ywsjzd':datetime.now(),
        'lrrzd':'xxx',
    }
    return JsonResponse(infodict)

#3.获取校验字段_20161207_wyw
def getCheckFieldList(request):
    data = FieldTable.objects.filter(tablechinese = request.GET.get('tcname'))
    fieldlist = []
    for num in range(len(data)):
        fieldlist.append(getattr(data[num], 'fieldchinese'))
    return HttpResponse(json.dumps(fieldlist), content_type='application/json')

#4.获取校验参数列表_20161209_wyw
def getParamList(request):
    data = MasterdataTable.objects.filter(id = request.GET.get('ruleid'))

#5.获取常用规则列表_20161209_wyw
def getOftenRules(request):
    data = OftenRules.objects.all()
    oftenrulelist = []
    for num in range(len(data)):
        temp = {
            'fieldName':getattr(data[num],'RuleName'),
            'chineseName':getattr(data[num],'ChineseName'),
            'nullRate':'',
            'identifier':getattr(data[num],'Identifier'),
            'standardDE':'',
        }
        oftenrulelist.append(temp)
    return HttpResponse(json.dumps(oftenrulelist), content_type='application/json')

#6.获取规则参数列表_20161210_wyw
def getRuleParamList(request):
    data = Parameters.objects.filter(remark=request.POST.get('ids'))
    print(request.POST.get('ids'))
    paramList = []
    for num in range(len(data)):
        temp = {
            'paramName':getattr(data[num],'parametername'),
            'paramChiName':getattr(data[num],'parameterchinese'),
            'dataType':getattr(data[num],'datatype'),
            'isNull':getattr(data[num],'nonempty'),
            'paramValue':getattr(data[num],'defaultvalue'),
        }
        paramList.append(temp)
    return  HttpResponse(json.dumps(paramList), content_type='application/json')

#7.获取方案规则列表_20161210_wyw
# def getCaseRules(request):

def getNameList(request):
    #增量字段、单位字段、业务时间字段、录入人字段
    data = MasterdataTable.objects.all()
    mlist = []
    for num in range(len(data)):
        temp = {
            'fid': getattr(data[num], 'id'),
            'fename': getattr(data[num], 'codetable'),
        }
        mlist.append(temp)
    return HttpResponse(json.dumps(mlist), content_type='application/json')

def getList():
    pass

#获取基础检测方案信息列表_20161210_wyw_xg
def getBasicTestingList(request):  # 信息内容
    page = int(request.POST.get('page',1))
    rows = int(request.POST.get('rows',10))
    start = (page - 1) * rows
    end = page * rows
    if ('condition' in request.POST) and (request.POST.get('condition') != ''):
        # counts = BasicTesting.objects.filter(cn_name=request.POST.get('condition')).count()
        data = BasicTesting.objects.filter(cn_name=request.POST.get('condition'))[start:end]
    else:
        # counts = BasicTesting.objects.all().count()
        data = BasicTesting.objects.all()[start:end]
    nlist = []
    # fields = BasicTesting._meta.get_all_field_names()
    for num in range(len(data)):
        temp={
            'schemeName':getattr(data[num],'SchemeName'),
            'checkObject':getattr(data[num],'CheckObject'),
            'checkRule':getattr(data[num],'CheckRule_id'),
            'executionDate':str(getattr(data[num],'ExecutionDate')),
        }
        # temp = {}
        # for t in range(len(fields)):
            # if 'ExecutionDate'==fields[t]:
            #     temp[fields[t]] = str(getattr(data[num], 'ExecutionDate'))
            # elif 'CheckRule_id'==fields[t]:
            #     temp['CheckRule_id'] = OftenRules.objects.filter(id=getattr(data[num], 'CheckRule_id'))
            # else:
            #     temp[fields[t]] = getattr(data[num], fields[t])
        nlist.append(temp)
    # return JsonResponse({'total': counts, 'rows': nlist})
    return HttpResponse(json.dumps(nlist), content_type='application/json')

def saveBasicTesting(request):
    data = request.POST
    test = BasicTesting()
    # fields = BasicTesting.objects.all()
    # print("data.get('id') ==========> %s" % data.get('id'))
    # if data.get('id') == '':
    #     for field in fields:
    #         if field.SchemeName == data.get('SchemeName'):
    #             return JsonResponse({'errorCode': '0x0001', 'errorString': '方案名称不能重复！'})
    # else:
    #     test.id = data.get('id')
    #     if data.get('SchemeName') != BasicTesting.objects.get(id=data.get('id')).SchemeName:
    #         for field in fields:
    #             if field.SchemeName == data.get('SchemeName'):
    #                 return JsonResponse({'errorCode': '0x0001', 'errorString': '方案名称不能重复！'})
    test.SchemeName = data.get('SchemeName')
    test.CheckObject = data.get('Checkobject')
    test.IncrementField = data.get('IncrementField')
    test.UnitField = data.get('UnitField')
    test.ServiceTimeField = data.get('ServiceTimeField')
    test.EntryField = data.get('EntryFieldField')
    test.timeType = data.get('timeType')
    if data.get('timeType') == '1':
        if data.get('cycle1') == '1':
            test.ExecutionCycle = '每月%s号' % (int(data.get('days1')))
            test.ExecutionDate = '%s:%s' % (int(data.get('hours1')), int(data.get('minutes1')))
        elif data.get('cycle1') == '2':
            if data.get('week_day') == '0':
                test.ExecutionCycle = '每周周日'
                test.ExecutionDate = '%s:%s' % (int(data.get('hours1')), int(data.get('minutes1')))
            else:
                test.ExecutionCycle = '每周周%s' % (int(data.get('week_day')))
                test.ExecutionDate = '%s:%s' % (int(data.get('hours1')), int(data.get('minutes1')))
        elif data.get('cycle1') == '3':
            test.ExecutionCycle = '每日'
            test.ExecutionDate = '%s:%s' % (int(data.get('hours1')), int(data.get('minutes1')))

    elif data.get('timeType') == '2':
        test.ExecutionDate = data.get('once_time1')

    elif data.get('timeType') == '4':
        test.ExecutionCycle = data.get('intervalDay1')
        test.ExecutionDate = '%s:%s' % (int(data.get('hours1')), int(data.get('minutes1')))
    test.save()
    return JsonResponse({'errorCode': '0x0000', 'errorString': '保存成功'})



def deleteBasicTesting(request):
    ids = request.POST.get('ids')
    print(ids)
    BasicTesting.objects.extra(where=['id in (' + ids + ')']).delete()
    try:
        BasicTesting.objects.extra(where=['id in (' + ids + ')']).delete()
    except:
        return JsonResponse({'errorCode': '0x0001', 'errorString': '删除失败'})

    return JsonResponse({'errorCode': '0x0000', 'errorString': '删除成功'})

def checkMethodList(request):
    id = request.POST.get('ids')
    methodtype = TestMethod.objects.filter(method_type = id)
    mlist = []
    for one in methodtype:
        temp = {
            'ids': one.id,
            'texts': one.method_name
        }
        mlist.append(temp)
    print(mlist)
    return HttpResponse(json.dumps(mlist), content_type='application/json')


