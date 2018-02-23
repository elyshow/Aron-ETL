# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings



from .models import Assess,AssessDisplay
from .models import Logassessment,LogassessmentDisplay
from .models import Result,ResultDisplay

from django.db.models import Q
from django.http import JsonResponse
import json
import os,time
import pymysql
import os.path





# Create your views here.
def index(request):
    return render_to_response('dataQualityAssessment/index.html')

def showData(request):
    print(666666666666)
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    #create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Assess.objects.filter(id=request.POST.get('condition')).count()
        data = Assess.objects.filter(id=request.POST.get('condition'))[start:end]
    else:
        counts = Assess.objects.all().count()
        data = Assess.objects.all()[start:end]

    list = []
    for num in range(len(data)):          #遍历
        # data[num].create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # data[num].save()
        temp={
            'resourcechname':data[num].resourcechname,
            'resourcename':data[num].resourcename,
            'datasource':data[num].datasource,
            'samplingnumber': data[num].samplingnumber,
            'evaluationstate': data[num].evaluationstate,
            'assesstime': data[num].assesstime,
            'taskstate':data[num].taskstate,
            'id': data[num].id,

        }
        list.append(temp)
    #return HttpResponse(6)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据
# 后台增加方法
def addData(request):
    resourcechname=request.POST['resourcechname']
    resourcename=request.POST['resourcename']
    datasource = request.POST['datasource']
    samplingnumber = request.POST['samplingnumber']
    card = request.POST['card']
    taskstate = request.POST['taskstate']
    evaluationstate = request.POST['evaluationstate']
    assesstime = request.POST['assesstime']

    print(evaluationstate)

    tb1=Assess()
    tb1.resourcechname = resourcechname
    tb1.resourcename = resourcename
    tb1.datasource = datasource
    tb1.samplingnumber = samplingnumber
    tb1.card = card
    tb1.taskstate = taskstate
    tb1.evaluationstate = evaluationstate
    tb1.assesstime = assesstime


    tb1.save()
    return HttpResponse(json.dumps(1), content_type='application/json')

# 立即执行
def runNow3(request):
    id=request.GET['data']
    stateStartId=Assess.objects.get(id=id)
    stateStartId.taskstate = 2
    card = stateStartId.card
    assesstime = stateStartId.assesstime
    datasource = stateStartId.datasource
    resourcename = stateStartId.resourcename
    resourcechname = stateStartId.resourcechname
    samplingnumber = stateStartId.samplingnumber

    str1 = card
    str2 = 18
    # 用len()内置函数来取字符串长度
    if len(str1) == str2:
        result = '成功'
    else:
        result = '失败'
    tb = Assess.objects.get(id=id)
    tb.save()

    table = Logassessment()
    table.taskstate=result
    table.assesstime=assesstime
    table.datasource = datasource
    table.assesstime = assesstime
    table.resourcename = resourcename
    table.resourcemingcheng = resourcechname
    table.truesampling = samplingnumber

    table.save()
    stateStartId.save()
    return HttpResponse('ok')
    # return HttpResponse(json.dumps('99'), content_type='application/json')




#后台删除方法
def delData(request):
    # name = request.GET.get('data')              #获取数据
    # tb1 = Table1.objects.get(method_name=name)  #获取记录
    # tb1.delete()
    #
    # return JsonResponse(result)
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Assess.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityAssessment/index/')


# 后台修改方法
def changeMet(request):
    resourcechname = request.POST['resourcechnamechange']
    resourcename = request.POST['resourcenamechange']
    datasource = request.POST['datasourcechange']
    samplingnumber = request.POST['samplingnumberchange']
    id = request.POST['idchange']
    card = request.POST['cardchange']

    dos = Assess.objects.get(id=id)
    dos.resourcechname = resourcechname
    dos.resourcename = resourcename
    dos.datasource = datasource
    dos.samplingnumber = samplingnumber
    dos.card = card

    dos.id=id
    dos.save()
    return HttpResponse(json.dumps(2), content_type='application/json')


#查看日志对话框
def loadList(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    #create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Logassessment.objects.filter(id=request.POST.get('condition')).count()
        data = Logassessment.objects.filter(id=request.POST.get('condition'))[start:end]
    else:
        counts = Logassessment.objects.all().count()
        data = Logassessment.objects.all()[start:end]
    list = []
    for d in data:            #用 d来遍历data_list
        temp={
                'datasource':d.datasource,         #引号中的内容是dataQualityAssessment.js中fieled后面引号中的内容，是js与后台数据库建立联系的关键。“d.”是后台数据库中相应表的字段，即models中表的相应字段
                'resourcename':d.resourcename,
                'resourcechname':d.resourcemingcheng,
                'truesampling':d.truesampling,
                'assesstime': d.assesstime,
                'taskstate': d.taskstate,
                'id': d.id,
        }
        list.append(temp)
    #return HttpResponse(6)
    return JsonResponse({'total': counts, 'rows': list})      #返回json数据


#日志删除方法
def delData02(request):
    # name = request.GET.get('data')              #获取数据
    # tb1 = Table1.objects.get(method_name=name)  #获取记录
    # tb1.delete()
    #
    # return JsonResponse(result)
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    Logassessment.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataQualityAssessment/index/')









#检测对话框
def loadList2(request):
    data_list = Result.objects.all()  # 将“Result”表中的数据以data_list获取出来
    list=[]
    for d in data_list:            #用 d来遍历data_list
        temp={
                'id':d.id,         #引号中的内容是dataMonnitoringStatistics.js中fieled后面引号中的内容，是js与后台数据库建立联系的关键。“d.”是后台数据库中相应表的字段，即models中表的相应字段
                'fieldname':d.fieldname,
                'type':d.type,
                'completeness':d.completeness,
                'uniqueness': d.uniqueness,
                'valuerange': d.valuerange,
                'lengthrange': d.lengthrange,
                'zifucharacter': d.zifucharacter,
                  }
        list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')                      #返回的格式，。为固定格式。只有导入json之后在可以用



