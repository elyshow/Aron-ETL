from django.shortcuts import render,HttpResponse
import json
from .models import Release,CatalogueStandardLibrary,FieldTable
from releaseRegisterManagement.models import MasterdataTable
from catalogueManagement.models import Catalogue
from dataProfile.models import ResourceField,ReleaseCatalogue
from django.http import JsonResponse
from releaseRegisterManagement import gobal
from django.db.models import Q
from django.db import connection
dataid = '0'
import datetime,time

# Create your views here.
def index(request):
    return render(request, 'releaseRegisterManagement/index.html')

#未注册数据
def unregisterIndex(request):
    #局部刷新传值
    dataid = request.POST.get('dataid', 0)
    page = int(request.POST.get('page', 1))
    rows = int(request.POST.get('rows', 10))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = MasterdataTable.objects.filter(tablechinese=request.POST.get('condition')).count()
        data = MasterdataTable.objects.filter( tablechinese=request.POST.get('condition'))[start:end]
    #刷新datagrid区域
    elif dataid != 0:
        counts = MasterdataTable.objects.filter(remark=dataid).count()
        data = MasterdataTable.objects.filter(remark=dataid)[start:end]
    else:
        counts = MasterdataTable.objects.all().count()
        data = MasterdataTable.objects.all()[start:end]
    unregisterList = []
    for num in range(len(data)):
        temp = {
            "table_english":data[num].tableenglish,
            "table_chinese":data[num].tablechinese,
            "table_id":data[num].tableid,
            "source": data[num].source,
            "id": data[num].id,
        }
        unregisterList.append(temp)
    return JsonResponse({'total':counts,'rows':unregisterList})

#递归函数
def getTree(pid = 0,res = []):
    data = CatalogueStandardLibrary.objects.filter(typeparentid= pid)
    lens = len(data)
    for num in range(0, lens):
        num = int(num)
        temp = {
             'id':  data[num].typeid,
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
    lists = getTree(0,[])
    return HttpResponse(json.dumps(lists), content_type="application/json")

# 拖拽
def dragData(request):

    a = request.POST.get('dataid')
    print('a', a)
    counts = FieldTable.objects.filter(tableid = a).count()
    print(connection.queries)
    data = FieldTable.objects.filter(tableid = a)
    print('counts', counts)
    dragDataList = []
    for num in range(len(data)):
        temp = {
            "field_english": data[num].fieldenglish,
            "field_chinese": data[num].fieldchinese,
            "show_type": data[num].showtype,
            'field_length':data[num].fieldlength,
            'element_identifier':data[num].elementidentifier,
        }
        dragDataList.append(temp)
    return JsonResponse({'total':counts,'rows': dragDataList})

#存
def saveCleaningRules(request):
    result = {'errorCode': '0x0000', 'errorString': ''}
    if request.method == 'POST':
        postData = request.POST
        resourceid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        registertime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        releaseData = Release()
        fields = releaseData._meta.get_all_field_names()
        print(fields)
        for field in fields:
            setattr(releaseData, field, postData.get(field, ''))
        releaseData.resourceid = resourceid
        releaseData.registertime = registertime
        releaseData.resourcetype = "1"
        releaseData.save()
        releasetable = request.POST.get('releasetable')
        data = json.loads(request.POST.get('hierarchy'))
        for num in range(len(data)):
            newResourcefield = ResourceField()
            newResourcefield.fieldenglish = json.dumps(data[num])
            newResourcefield.resourceid = resourceid
            newResourcefield.tableenglish = releasetable
            newResourcefield.save()
        return JsonResponse(result)
    else:
        result.errorCode = '0x0002'
        result.errorString = '参数错误'
    return JsonResponse(result)

#注册完成
def registerIndex(request):
    #局部刷新传值
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Release.objects.filter(resourcename=request.POST.get('condition')).count()
        # n_list = Basetype.objects.filter(Q(taskid=selectName) | Q(taskname=selectName))
        data = Release.objects.filter( resourcename=request.POST.get('condition'))[start:end]
    else:
        counts = Release.objects.filter(resourcetype='1').count()
        data = Release.objects.filter(resourcetype='1')[start:end]
    registerList = []
    for num in range(len(data)):
        temp = {
            "resourceid": data[num].resourceid,
            "resourcename":data[num].resourcename,
            "resourcetype":data[num].resourcetype,
            "registertime":data[num].registertime,
        }
        registerList.append(temp)
    return JsonResponse({'total':counts,'rows':registerList})

#拖拽2
def dragData2(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = MasterdataTable.objects.filter(tablechinese=request.POST.get('condition')).count()
        data = MasterdataTable.objects.filter( tablechinese=request.POST.get('condition'))[start:end]
    else:
        counts = Catalogue.objects.all().count()
        data = Catalogue.objects.all()[start:end]
    releaseList = []
    for num in range(len(data)):
        temp = {
            "cataloguename":data[num].cataloguename,
            "typeid":data[num].typeid,
            "typeparentid":data[num].typeparentid,
        }
        releaseList.append(temp)
    return JsonResponse({'total':counts,'rows':releaseList})


def release(request):
    result = {'errorCode': '0x0000', 'errorString': ''}
    if request.method == 'POST':
        print(111111)
        catalogueid = request.POST.get('ids')
        catalogueidData = catalogueid.split(',')
        resourcename = request.POST.get('resourcename')
        resourceid = request.POST.get('resourceid')
        releasetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        releaseData = Release.objects.get(resourceid=resourceid)
        releaseData.releasetime = releasetime
        releaseData.resourcetype = "2"
        releaseData.save()
        print(catalogueidData)
        for num in range(len(catalogueidData)):
            rcat = ReleaseCatalogue()
            fields = rcat._meta.get_all_field_names()
            for field in fields:
                setattr(rcat, field, request.POST.get(field))

            rcat.resourceid = resourceid
            rcat.typeid = catalogueidData[num]
            idcount1 = catalogueidData[num][0:1]
            idcount2 = catalogueidData[num][0:4]
            idcount3 = catalogueidData[num][0:7]


            rcat.resourcename = resourcename
            rcat.releasetime = releasetime
            cl = Catalogue.objects.get(typeid=rcat.typeid)

            rcat.cataloguename = cl.cataloguename
            rcat.save()
            cl1 = Catalogue.objects.get(typeid=idcount1)
            cl1.count = cl1.count + 1
            cl1.save()
            if idcount2 != '' and len(idcount2) == 4:
                cl2 = Catalogue.objects.get(typeid=idcount2)
                cl2.count = cl2.count + 1
                cl2.save()
                if idcount3 != '' and len(idcount3) == 7:
                    cl3 = Catalogue.objects.get(typeid=idcount3)
                    cl3.count = cl3.count + 1
                    cl3.save()

        return JsonResponse(result)
    else:
        result['errorCode'] = '0x0002'
        result['errorString'] = '参数错误'
    return JsonResponse(result)


def releaseIndex(request):
    #局部刷新传值
    dataid = request.POST.get('dataid', 0)
    # condition = request.POST.get('condition')
    # print(condition)
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = Release.objects.filter(resourcename=request.POST.get('condition')).count()
        data = Release.objects.filter( resourcename=request.POST.get('condition'))[start:end]
    elif dataid != 0:
        counts = ReleaseCatalogue.objects.filter(typeid=dataid).count()
        data = ReleaseCatalogue.objects.filter( typeid=dataid)[start:end]
    else:
        counts = Release.objects.order_by("-resourceid").filter(resourcetype='2').count()
        data = Release.objects.order_by("-resourceid").filter(resourcetype='2')[start:end]
    registerList = []
    for num in range(len(data)):
        temp = {
            "resourceid": data[num].resourceid,
            "resourcename":data[num].resourcename,
            "releasetime":data[num].releasetime,
        }
        registerList.append(temp)
    return JsonResponse({'total':counts,'rows':registerList})

def registerCancel(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    ResourceField.objects.extra(where=['resourceid IN (' + idstring + ')']).delete()
    Release.objects.extra(where=['resourceid IN (' + idstring + ')']).update(resourcetype='0')

    return HttpResponse('ok')

def fabuCancel(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    print(stp)
    for index in stp:
        rel=ReleaseCatalogue.objects.filter(resourceid=index)
        print(77)
        for i in rel:
            ss1=i.typeid[0:1]
            ss2=i.typeid[0:4]
            ss3=i.typeid[0:7]

            cl = Catalogue.objects.get(typeid=ss1)
            cl.count = cl.count - 1
            cl.save()
            if ss2 != '' and len(ss2)==4:
                cl2 = Catalogue.objects.get(typeid=ss2)
                cl2.count = cl2.count - 1
                cl2.save()
                if ss3 != '' and len(ss3)==7:
                    cl3 = Catalogue.objects.get(typeid=ss3)
                    cl3.count = cl3.count - 1
                    cl3.save()
    ReleaseCatalogue.objects.extra(where=['resourceid IN (' + idstring + ')']).delete()
    Release.objects.extra(where=['resourceid IN (' + idstring + ')']).update(resourcetype='1')

    return HttpResponse('ok')






















