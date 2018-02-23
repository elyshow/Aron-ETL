#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import render_to_response
import random,time
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import DataStandard,StandardData,ComboBoxData,DataType
from releaseRegisterManagement.models import MasterdataTable,FieldTable
from .models import BusCode,StandardDataInfo,RecognInfo,DataBase
import json,pymysql
# Create your views here.


def standardIndex(request):
    return render_to_response("codeStandard/standardIndex.html")


def standardData(request):
    if not 'type' in request.POST:
        return JsonResponse({'errorCode': '0x0000', 'errorString': '参数错误'})
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = StandardDataInfo.objects.filter(tabtype=request.POST.get('type'),identifier=request.POST.get('condition')).count()
        data = StandardDataInfo.objects.filter(tabtype=request.POST.get('type'), identifier=request.POST.get('condition'))[start:end]
    else:
        counts = StandardDataInfo.objects.filter(tabtype=request.POST.get('type')).count()
        data = StandardDataInfo.objects.filter(tabtype=request.POST.get('type'))[start:end]
    list = []
    type = request.POST.get('type')
    for num in range(len(data)):
            temp = {
                'cnname': data[num].cnname,
                'identifier': data[num].identifier,
                'object': data[num].object,
                'datatype': data[num].datatype,
                'standardsou': data[num].datafrom,
                'state': data[num].state,
                'id':data[num].nameid,
                'rule':data[num].rule,
            }
            list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

print('baobao1')
def addStandardData(request):
    print('baobao2')
    if request.POST.get('save_type') == 'add':
        print(000)
        rule = request.POST.get('Rule')
        insideIdenti = request.POST.get('insideIdentifier')
        cnName = request.POST.get('chineseName')
        cnSpell = request.POST.get('cn_spell')
        identi = request.POST.get('identifier')
        version = request.POST.get('version')
        samilarName = request.POST.get('samilarName')
        definIntro = request.POST.get('definedIntro')
        objBelong = request.POST.get('object')
        featureWord = request.POST.get('featureWord')
        relation = request.POST.get('relation')
        meanWord = request.POST.get('showWord')
        dataType = request.POST.get('datatype')
        dataFormat = request.POST.get('dataFormat')
        valueRange = request.POST.get('valueRange')
        measUnit = request.POST.get('measurementUnit')
        subOrg = request.POST.get('subOrganization')
        writer = request.POST.get('draftsman')
        approvedDate = request.POST.get('approvedDate')
        quotdStandard = request.POST.get('quotdStandard')
        remark = request.POST.get('remark')
        state=rule
        if identi[0]>='A' and identi[0]<='D':    #判断标识符所属分类
            type = '0'
        if identi[0]>='E' and identi[0]<='H':
            type ='1'
        if identi[0]>='I' and identi[0]<='L':
            type = '2'
        if identi[0]>='M' and identi[0]<='P':
            type = '3'
        if identi[0]>='Q' and identi[0]<='T':
            type = '4'
        if identi[0]>='U' and identi[0]<='Z':
            type = '5'
        sdi = StandardDataInfo(nameid = str(random.random())[2:8],rule=rule, identifier=identi, inseridentifier=insideIdenti, samilarname=samilarName,
                               object=objBelong,feature=featureWord, relation=relation, impressword=meanWord, datatype=dataType,datarule=dataFormat,
                               valuerange=valueRange, measunit=measUnit, subrecogn=subOrg, mainwriter=writer, introduce=definIntro,
                               approvedate=approvedDate, datafrom=quotdStandard, version=version, cnspell=cnSpell,remark=remark, cnname=cnName,
                               tabtype=type,state=rule)
        sdi.save()
    elif request.POST.get('save_type') == 'edit':
        id = request.POST.get('id')
        print(999)
        rule = request.POST.get('Rule')
        insideIdenti = request.POST.get('insideIdentifier')
        cnName = request.POST.get('chineseName')
        cnSpell = request.POST.get('cn_spell')
        identi = request.POST.get('identifier')
        version = request.POST.get('version')
        samilarName = request.POST.get('samilarName')
        definIntro = request.POST.get('definedIntro')
        objBelong = request.POST.get('object')
        featureWord = request.POST.get('featureWord')
        relation = request.POST.get('relation')
        meanWord = request.POST.get('showWord')
        dataType = request.POST.get('datatype')
        dataFormat = request.POST.get('dataFormat')
        valueRange = request.POST.get('valueRange')
        measUnit = request.POST.get('measurementUnit')
        subOrg = request.POST.get('subOrganization')
        writer = request.POST.get('draftsman')
        approvedDate = request.POST.get('approvedDate')
        quotdStandard = request.POST.get('quotdStandard')
        remark = request.POST.get('remark')
        state = rule
        if identi[0] >= 'A' and identi[0] <= 'D':  # 判断标识符所属分类
            type = '0'
        if identi[0] >= 'E' and identi[0] <= 'H':
            type = '1'
        if identi[0] >= 'I' and identi[0] <= 'L':
            type = '2'
        if identi[0] >= 'M' and identi[0] <= 'P':
            type = '3'
        if identi[0] >= 'Q' and identi[0] <= 'T':
            type = '4'
        if identi[0] >= 'U' and identi[0] <= 'Z':
            type = '5'
        sdi = StandardDataInfo(nameid=id, rule=rule, identifier=identi,
                               inseridentifier=insideIdenti, samilarname=samilarName,
                               object=objBelong, feature=featureWord, relation=relation, impressword=meanWord,
                               datatype=dataType, datarule=dataFormat,
                               valuerange=valueRange, measunit=measUnit, subrecogn=subOrg, mainwriter=writer,
                               introduce=definIntro,
                               approvedate=approvedDate, datafrom=quotdStandard, version=version, cnspell=cnSpell,
                               remark=remark, cnname=cnName,
                               tabtype=type,state=rule)
        sdi.save()
    return HttpResponse('ok')


#删除数据
def delData(request):
    cancel = request.GET.getlist("data")
    identistring = ','.join(cancel)
    # print (identistring)
    StandardDataInfo.objects.extra(where=['nameid IN (' + identistring + ')']).delete()
    return HttpResponse('ok')


def recognizeData(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = DataStandard.objects.filter(codetable=request.POST.get('condition')).count()
        data = DataStandard.objects.filter(codetable=request.POST.get('condition'))[start:end]
    else:
        counts = DataStandard.objects.all().count()
        data = DataStandard.objects.all()[start:end]
    list = []
    for num in range(len(data)):
             temp ={
            'codename':data[num].codename,
            'codetable':data[num].codetable,
            'datasource':data[num].datasource,

            }
             list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

def Detail(request):
    id = request.GET['data']
    detail_list = StandardDataInfo.objects.filter(identifier=id)
    list = []
    for i in detail_list:
        temp = {
            'id':i.nameid,
            'rule': i.rule,
            'insertIdenti':i.inseridentifier,
            'identi': i.identifier,
            'samilarname': i.samilarname,
            'object': i.object,
            'feature': i.feature,
            'impressword': i.impressword,
            'datatype': i.datatype,
            'datarule': i.datarule,
            'valuerange': i.valuerange,
            'meas_unit': i.measunit,
            'sub_recogn': i.subrecogn,
            'main_writer': i.mainwriter,
            'introduce': i.introduce,
            'approve_date': i.approvedate,
            'datafrom': i.datafrom,
            'version': i.version,
            'cn_spell': i.cnspell,
            'remark': i.remark,
            'cn_name': i.cnname,
            'state': i.state,
            'relation':i.relation,
        }
        list.append(temp)
    print(list)
    return HttpResponse(json.dumps(list),content_type='application/json')


def recognize(request):
    re_info = RecognInfo.objects.all()
    print(re_info)
    list = []
    for i in re_info:
        temp = {
            'recognid':i.recognid,
            'recognname':i.recognname,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')

def comboboxData(request):
    type = request.POST.get('type')
    print (type)
    list = []
    if type=='1':
        meanWord = ComboBoxData.objects.filter(type='1')
        for m in meanWord:
            temp = {
                'value':m.value,
                'cn_name':m.cnname,
            }
            list.append(temp)
    if type=='2':
        meanWord = ComboBoxData.objects.filter(type='2')
        for m in meanWord:
            temp = {
                'value':m.value,
                'cn_name':m.cnname,
            }
            list.append(temp)
    if type=='3':
        meanWord = ComboBoxData.objects.filter(type='3')
        for m in meanWord:
            temp = {
                'value':m.value,
                'cn_name':m.cnname,
            }
            list.append(temp)
    if type == '4':
        re_info = RecognInfo.objects.all()
        list = []
        for i in re_info:
            temp = {
                'recognid': i.recognid,
                'recognname': i.recognname,
            }
            list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')


def recognizeIndex(request):
    return render_to_response("codeStandard/recognizeIndex.html")


def recognAddData(request):
    a=request.POST.get('save_type')
    if request.POST.get('save_type') == 'add':
        print(111)
        print(a)
        name = request.POST.get('recognName')
        print(name)
        number = request.POST.get('recognNumber')
        simpleName = request.POST.get('recognSimple')
        nature = request.POST.get('nature')
        re = RecognInfo(rid=str(random.random())[2:7],recognname=name,recognid=simpleName,recogntype=nature,recognnumber=number)
        re.save()
    elif request.POST.get('save_type') == 'edit':
        print(a)
        id = request.POST.get('id')
        print(id)
        name = request.POST.get('recognName')
        number = request.POST.get('recognNumber')
        simpleName = request.POST.get('recognSimple')
        nature = request.POST.get('nature')
        re = RecognInfo(rid=id,recognname=name, recognid=simpleName, recogntype=nature,recognnumber=number)
        re.save()
    return HttpResponse('ok')

def recognInfo(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = RecognInfo.objects.filter(recognname=request.POST.get('condition')).count()
        data = RecognInfo.objects.filter(recognname=request.POST.get('condition'))[start:end]
    else:
        counts = RecognInfo.objects.all().count()
        data = RecognInfo.objects.all()[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'simplename': data[num].recognid,
            'name': data[num].recognname,
            'nature': data[num].recogntype,
            'number': data[num].recognnumber,
            'id': data[num].rid,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


def recognDel(request):
    cancel = request.GET.getlist("data")
    identistring = ','.join(cancel)
    RecognInfo.objects.extra(where=['rid IN (' + identistring + ')']).delete()
    return HttpResponse('ok')

def checkData(request):
    id = request.GET['data']
    recond = RecognInfo.objects.filter(rid=id)
    list = []
    for r in recond:
        temp = {
            'id':r.rid,
            'name':r.recognname,
            'recognid':r.recognid,
            'recogntype':r.recogntype,
            'recognNumber':r.recognnumber,

        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')


def dataTypeIndex(request):

    return render_to_response("codeStandard/dataTypeIndex.html")

def typeData(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = DataType.objects.filter(dataname=request.POST.get('condition')).count()
        data = DataType.objects.filter(dataname=request.POST.get('condition'))[start:end]
    else:
        counts = DataType.objects.all().count()
        data = DataType.objects.all()[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'dataname': data[num].dataname,
            'mainword': data[num].mainword,
            'standardcode': data[num].standardcode,
            'classify': data[num].classify,
            'userecognize': data[num].userecognize,
            'id': data[num].dataid,

        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


def addInfoData(request):
    print(111)
    if request.POST.get('save_type') == 'add':
        dataname = request.POST.get('dataname')
        mainWord = request.POST.get('mainWord')
        standardCode = request.POST.get('standardCode')
        classify = request.POST.get('classify')
        useRcognize = request.POST.get('useRcognize')
        dt = DataType()
        dt.dataid = str(random.random())[2:7]
        dt.dataname = dataname
        dt.mainword = mainWord
        dt.standardcode = standardCode
        dt.classify = classify
        dt.userecognize = useRcognize
        dt.save()
    elif request.POST.get('save_type') == 'edit':
        dataid = request.POST.get('dataid')
        dataname = request.POST.get('dataname')
        mainWord = request.POST.get('mainWord')
        standardCode = request.POST.get('standardCode')
        classify = request.POST.get('classify')
        useRcognize = request.POST.get('useRcognize')
        dt = DataType()
        dt.dataid = dataid
        dt.dataname = dataname
        dt.mainword = mainWord
        dt.standardcode = standardCode
        dt.classify = classify
        dt.userecognize = useRcognize
        dt.save()
    return HttpResponse('ok')


def dataDel(request):
    cancel = request.GET.getlist("data")
    identistring = ','.join(cancel)
    DataType.objects.extra(where=['dataid IN (' + identistring + ')']).delete()
    return HttpResponse('ok')

def dataEdit(request):
    id = request.GET['data']
    recond = DataType.objects.filter(dataid=id)
    list = []
    for r in recond:
        temp = {
            'dataname': r.dataname,
            'mainword': r.mainword,
            'standardcode': r.standardcode,
            'classify': r.classify,
            'userecognize': r.userecognize,
            'id': r.dataid,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')



#业务代码管理
def busCodeIndex(request):
    return render_to_response("codeStandard/busCodeIndex.html")

def busCode(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    print(end)
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = BusCode.objects.filter(codetable=request.POST.get('condition')).count()
        data = BusCode.objects.filter(codetable=request.POST.get('condition'))[start:end]
        print(counts)
    else:
        counts = BusCode.objects.all().count()
        data = BusCode.objects.all()[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'codeid': data[num].codeid,
            'codename': data[num].codename,
            'codetable': data[num].codetable,
            'busclass': data[num].busclass,
            'registertime': data[num].registertime,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})

    # return HttpResponse("od")

def addBusCode(request):
    busCodename=request.POST['busCodeName']
    busCodetable=request.POST['busCodeTable']
    bu=BusCode()
    bu.registertime=time.strftime("%Y-%m-%d %X", time.localtime())
    bu.codename = busCodename
    bu.codetable = busCodetable
    bu.save()
    return HttpResponseRedirect('/busCodeIndex/')

def delBusCode(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    BusCode.objects.extra(where=['codeid IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/busCodeIndex/')

def dataElementIndex(request):
    return render_to_response("codeStandard/codeIndex.html")

#标准代码管理
def databaseIndex(request):
    return render_to_response("codeStandard/databaseIndex.html")

def getList(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = DataBase.objects.filter(type=request.POST.get('condition')).count()
        d_list = DataBase.objects.filter(type=request.POST.get('condition'))[start:end]
    else:
        d_list = DataBase.objects.all()[start:end]
        counts = DataBase.objects.all().count()
    list = []
    for i in range(len(d_list)):
        temp = {
            'id': d_list[i].id,
            'name': d_list[i].name,
            'type': d_list[i].type,
        }
        list.append(temp)
    return JsonResponse({'rows':list,'total':counts})

def saveList(request):
    name = request.POST.get('name')
    type = request.POST.get('type')
    st = DataBase()
    st.name = name
    st.type = type
    st.save()
    return HttpResponse('OK')

def savechangeList(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    type = request.POST.get('type')
    st = DataBase()
    st.id = id
    st.name = name
    st.type = type
    st.save()
    return HttpResponse('OK')

def delDbList(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    DataBase.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/databaseIndex/')

#数据库类型管理
def taskIndex(request):
    return render_to_response('codeStandard/taskIndex.html')

#下拉框读取数据库
def sjygl(request):
    s_list = BusCode.objects.all()
    list=[]
    for i in s_list:
        temp = {
        'codeid':i.codeid,
        'codename':i.codename,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')

def deleteTask(request):
    stp = request.GET.getlist("data")
    # print(stp)
    idstring = ','.join(stp)
    DataStandard.objects.extra(where=['id IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/taskIndex/')


def getDataList(request):
    if not 'type' in request.POST:
        return JsonResponse({'errorCode':'0x0000','errorString':'参数错误'})
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    b = request.POST.get('type')
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = DataStandard.objects.filter(codestandardclass=request.POST.get('type'), codename=request.POST.get('condition')).count()
        data = DataStandard.objects.filter(codestandardclass=request.POST.get('type'), codename=request.POST.get('condition'))[start:end]
    else:
        counts = DataStandard.objects.filter(codestandardclass = request.POST.get('type')).count()
        data = DataStandard.objects.filter(codestandardclass = request.POST.get('type'))[start:end]
    list = []
    for i in range(len(data)):
            temp = {
            'id':data[i].id,
            'codename':data[i].codename,
            'standardnum':data[i].standardnum,
            'codetable':data[i].codetable,
            'datasource':data[i].datasource,
            'registertime':data[i].registertime,
            'codesetname':data[i].codesetname,
            }
            list.append(temp)
    if b=='0':
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = DataStandard.objects.filter(codename=request.POST.get('condition')).count()
            data = DataStandard.objects.filter(codename=request.POST.get('condition'))[start:end]
        else:
            data = DataStandard.objects.all()[start:end]
            counts = DataStandard.objects.all().count()
        for i in range(len(data)):
            temp = {
                'id':data[i].id,
                'codename': data[i].codename,
                'standardnum': data[i].standardnum,
                'codetable': data[i].codetable,
                'datasource': data[i].datasource,
                'registertime': data[i].registertime,
                'codesetname': data[i].codesetname,
            }
            list.append(temp)
    # print(list)
    return JsonResponse({'total':counts,'rows':list})


def changeList(request):
    id = request.GET['data']
    s_list = DataStandard.objects.filter(id=id)
    list =[]
    for i in s_list:
        temp ={
             'id':i.id,
             'codename':i.codename,
             'standardnum':i.standardnum,
             'codetable':i.codetable,
             'datasource':i.datasource,
             'structuretype':i.structuretype,
             'businessclass':i.businessclass,
             'codestandardclass':i.codestandardclass,
             'resourceproperty':i.resourceproperty,
             'other':i.other,
        }
        list.append(temp)
    print(temp)
    return HttpResponse(json.dumps(list),content_type='application/json')

def save(request):
    if request.POST.get('save_type') == 'add':
        codename = request.POST.get('codename')
        standardnum = request.POST.get('standardnum')
        codetable = request.POST.get('codetable')
        datasource = request.POST.get('datasource')
        registertime = time.strftime("%Y-%m-%d %X", time.localtime())
        structuretype = request.POST.get('structuretype')
        businessclass = request.POST.get('businessclass')
        resourceproperty = request.POST.get('resourceproperty')
        codestandardclass = request.POST.get('codestandardclass')
        other = request.POST.get('other')
        st = DataStandard()
        st.id = str(random.random())[2:7]
        st.codename = codename
        st.standardnum = standardnum
        st.codetable = codetable
        st.datasource = datasource
        st.registertime = registertime
        st.structuretype = structuretype
        st.businessclass = businessclass
        st.resourceproperty = resourceproperty
        st.codestandardclass = codestandardclass
        st.other = other
        st.save()
    elif request.POST.get('save_type') == 'edit':
        id = request.POST.get('id')
        codename = request.POST.get('codename')
        standardnum = request.POST.get('standardnum')
        codetable = request.POST.get('codetable')
        datasource = request.POST.get('datasource')
        registertime = time.strftime("%Y-%m-%d %X", time.localtime())
        structuretype = request.POST.get('structuretype')
        businessclass = request.POST.get('businessclass')
        resourceproperty = request.POST.get('resourceproperty')
        codestandardclass = request.POST.get('codestandardclass')
        other = request.POST.get('other')
        st = DataStandard()
        st.id = id
        st.codename = codename
        st.standardnum = standardnum
        st.codetable = codetable
        st.datasource = datasource
        st.registertime = registertime
        st.structuretype = structuretype
        st.businessclass = businessclass
        st.resourceproperty = resourceproperty
        st.codestandardclass = codestandardclass
        st.other = other
        st.save()
    return JsonResponse('ok')

def delList(request):
    stp = request.GET.getlist("data")
    namestring = ','.join(stp)
    DataStandard.objects.extra(where=['id IN (' + namestring + ')']).delete()
    return HttpResponseRedirect("/taskIndex/")

def insertTable(request):
    dodo = MasterdataTable.objects.all()
    ds = DataStandard.objects.all()
    for i in dodo:
        a = 0
        for j in ds:
            if i.tablechinese == j.codename:
                print('null')
                print(22)
                a = 1
                break
        if a == 0:
            print(11)
            tableenglish=i.tableenglish,
            tablechinese=i.tablechinese,
            tableid=i.tableid,
            source=i.source,
            remark=i.remark
            stt=DataStandard()
            stt.id = str(random.random())[2:7]
            stt.codename = tablechinese[0]
            stt.codetable = tableenglish[0]
            stt.standardnum = tableid[0]
            stt.datasource = source[0]
            stt.type = remark[0]
            stt.registertime = time.strftime("%Y-%m-%d %X", time.localtime())
            stt.codestandardclass = 2
            stt.save()
    return HttpResponseRedirect("/taskIndex/")


def insertStandard(request):
    com = FieldTable.objects.all()
    dy = StandardDataInfo.objects.all()
    for i in com:
        a = 0
        for j in dy:
            if i.fieldchinese == j.cnname:
                print('null')
                print(22)
                a = 1
                break
        if a == 0:
            print(11)
            tablechinese = i.tablechinese,
            showtype = i.showtype,
            source = i.source,
            remark = i.remark,
            fieldenglish0 = i.fieldenglish[0]
            fieldenglish = i.fieldenglish
            fieldchinese = i.fieldchinese
            tableenglish = i.tableenglish
            stt = StandardDataInfo()
            stt.cnname = fieldchinese
            stt.identifier = fieldenglish
            stt.object = tablechinese[0]
            stt.datatype = showtype[0]
            stt.datafrom = source[0]
            stt.remark = remark[0]
            stt.rule = '2'
            stt.inseridentifier = tableenglish
            stt.state = '标准'
            if  fieldenglish0>= 'A' and fieldenglish0 <= 'D':  # 判断标识符所属分类
                stt.tabtype = '0'
            if fieldenglish0 >= 'E' and fieldenglish0 <= 'H':
                stt.tabtype = '1'
            if fieldenglish0 >= 'I' and fieldenglish0 <= 'L':
                stt.tabtype = '2'
            if fieldenglish0 >= 'M' and fieldenglish0 <= 'P':
                stt.tabtype = '3'
            if fieldenglish0 >= 'Q' and fieldenglish0 <= 'T':
                stt.tabtype = '4'
            if fieldenglish0 >= 'U' and fieldenglish0 <= 'Z':
                stt.tabtype = '5'
            stt.save()
    return HttpResponseRedirect("/standardIndex/")



def DetailTask(request):
    id = request.GET['datas']
    print (id)
    ds = DataStandard.objects.get(id=id)
    dsbus=ds.businessclass
    print(dsbus)
    b_list = BusCode.objects.all()
    print(type(b_list))
    for i in b_list:
        print(type(i))
        print(i.codeid)
        if i.codeid == int(dsbus):
            codename = i.codename
            print(i.codename)
    bs=DataStandard.objects.filter(id=id)
    list = []
    for b in bs:
            temp = {
                'codenameDetail': b.codename,
                'standardnumDetail': b.standardnum,
                'codetableDetail': b.codetable,
                'datasourceDetail': b.datasource,
                'registertimeDetail': b.registertime,
                'businessclassDetail': codename,
                'codestandardclassDetail': b.codestandardclass,
                'structuretypeDetail': b.structuretype,
            }
            list.append(temp)
    print(list)
    return HttpResponse(json.dumps(list), content_type='application/json')



def detilList(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    counts = StandardDataInfo.objects.filter(inseridentifier=request.POST.get('data')).count()
    data = StandardDataInfo.objects.filter(inseridentifier=request.POST.get('data'))[start:end]
    list = []
    for i in range(len(data)):
        temp = {
            'rule': data[i].rule,
            'identifier': data[i].identifier,
            'inseridentifier': data[i].inseridentifier,
            'object': data[i].object,
            'datatype': data[i].datatype,
            'datafrom': data[i].datafrom,
            'remark': data[i].remark,
            'cnname': data[i].cnname,
            'state': data[i].state,
            'tabtype': data[i].tabtype
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})
