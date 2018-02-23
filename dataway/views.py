# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from releaseRegisterManagement.models import MasterdataTable,FieldTable
from cataloguedataway.models import *
from standardApp.models import *
import standardApp.models as   _testmodel
import json
from django.http import JsonResponse
import os,time,datetime,random
import pymysql
import cx_Oracle
import os.path
from user.models import *
from django.contrib import auth
from django.contrib.auth.models import User

from huafeng.settings import STANDARDDB, DATABASES

from django.db.models import Q
#数据质量检测管理主页面
def index(request):
    return render_to_response('dataway/index.html')

#测试接口，前端页面
def csindex(request, idapi):
    print(idapi)
    conditionObjects = Conditionapi.objects.filter(idapi = idapi)
    conditions = []
    print(conditionObjects)
    for c in conditionObjects:
        objs = json.loads(c.conditionname)
        temp = {
            'name':objs['field_english'],
            'lebal':objs['field_chinese'],
        }
        conditions.append(temp)
    #print(Adminapi.objects.get(idapi=idapi))
    tableName = MasterdataTable.objects.get(tablechinese=Adminapi.objects.get(idapi=idapi).tableapi)
   # print(tableName.tableenglish)
    return render(request, 'dataway/csindex.html',{'conditions':conditions, 'idapi':idapi, 'tablename':tableName.tableenglish})

def csdef(request):
    result = []
    tablename = request.POST.get('tablename')
    print(11)
    if MasterdataTable.objects.filter(tableenglish=tablename):
        data = MasterdataTable.objects.all()
        print(22)
        unregisterList = []
        for num in range(len(data)):
            temp = {
                "table_english":data[num].tableenglish,
                "table_chinese":data[num].tablechinese,
                "table_id":data[num].tableid,
                "source": data[num].source,
            }
            print(temp)
            unregisterList.append(temp)
            print(unregisterList)
        return JsonResponse({'rows':unregisterList})
    else:
        result.append("表名不存在")
    return JsonResponse({'error':result})


# 测试接口。后台处理方法
def resourceSharing(request):
    data = json.loads(request.POST.get('data'))# def resourceSharing(request,data):
    print(data)
    idapi = data['idapi']
    fields = Fieldapi.objects.filter(idapi=idapi)
    selectFields  = ''
    selectFieldList = []
    for f in fields:
         field = json.loads(f.fieldData)
         selectFieldList.append(field['field_english'])
    selectFields = ','.join(selectFieldList)
    print(selectFields)
    print(11111111)
    start = data.get('start')
    end = data.get('end')
    del data['idapi']
    del data['start']
    del data['end']
    where = ' where 1=1 '
    for d,v in data.items():
   #     print(d,v)
        where += 'and '+ d + " like '%" + v + "%' "
    print(where) 
    tableName = MasterdataTable.objects.get(tablechinese=Adminapi.objects.get(idapi=idapi).tableapi)
    tableName = tableName.tableenglish.upper() + '_STANDARDAPP'
    sql = "select %s from (select %s.*,ROWNUM R from %s %s AND ROWNUM <= %s) B where B.R > %s" %(selectFields, tableName,tableName, where,end, start)
    from dataCleaning.sites import CleanSite
    from huafeng.settings import STANDARDDB
    from huafeng import functions as func
    con,_ = CleanSite.getConnection(STANDARDDB)
    cur = con.cursor()
    print(sql)
    res = cur.execute(sql)
    allData = cur.fetchall()
    result = []
    for l in allData:
        temp = []
        for t in l:
            temp.append(func.dataToString(t))
        result.append(dict(zip(selectFieldList,temp)))
    return JsonResponse({'head':selectFieldList,'body':result})  
   # print(allData)
    #result = []
    #requesttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #if request.method == 'POST':
    #    # 检验合法性
    #    # 从 request 中提取基本信息
    #    datawayapi = request.POST.get('datawayapi')
    #    condition1 = request.POST.get('condition1')
    #    condition2 = request.POST.get('condition2')
    #    condition3 = request.POST.get('condition3')
    #    condition4 = request.POST.get('condition4')
    #    condition5 = request.POST.get('condition5')
    #    username = request.POST.get('username')
    #    password = request.POST.get('password')
    #    # datas = request.POST.get('datas')
    #    # username = (datas['username'])
    #    # password = (datas['password'])
    #    # if
    #    # datawayapi = (datas['datawayapi'])
    #    # condition1 = (datas['condition1'])
    #    # condition2 = (datas['condition2'])
    #    # condition3 = (datas['condition3'])
    #    # condition4 = (datas['condition4']
    #    # condition5 = (datas['condition5'])
    #    # if :
    #    if Userpermission.objects.filter(username=username) :
    #        usernameGet=request.user
    #        quanxian=Userpermission.objects.get(username=username)
    #        id = quanxian.userid
    #        user = auth.authenticate(username=id,password=password)
    #        if user:
    #            permissiondata = Userpermission.objects.get(username=username)
    #            lenpermission =  permissiondata.userapipower
    #            a = lenpermission.split(',')
    #            permissionlist = []
    #            for i in a:
    #                temppower = i
    #                permissionlist.append(temppower)
    #            if datawayapi in permissionlist:
    #                # 根据api的id来在api管理表中获取相应数据（取出对应表名）
    #                # 表的验证，是否有这个字段
    #                if Adminapi.objects.filter(idapi=datawayapi):
    #                    apidata = Adminapi.objects.get(idapi=datawayapi)
    #                    # 在采集库总表中获取相应表对应的数据
    #                    tabledata = MasterdataTable.objects.get(tablechinese=apidata.tableapi)
    #                    # 获取采集库相应表的英文名
    #                    tablename = tabledata.tableenglish
    #                    # 获取查询条件
    #                    if len(condition1) > 0:
    #                        # filter判断
    #                        if Conditionapi.objects.filter(idapi=datawayapi):
    #                            conditiondata = Conditionapi.objects.filter(idapi=datawayapi)
    #                            # 将json字典数据取出来并解析
    #                            listcon = []
    #                            # 循环遍历，匹配Conditionapi表中相应数据,并获取conditionname的值，（ 单条conditionname形式如：{'field_chinese': '涉案物品编号', 'field_english': 'SAWPBH', 'show_type': 'string'}  ）
    #                            for num in range(len(conditiondata)):
    #                                con1 = json.loads(conditiondata[num].conditionname)
    #                                # 将单条的conditionname中的field_english取出，作为我们查询条件的变量名
    #                                con2 = (con1['field_english'])
    #                                # 添加到返回字段的列表listfield中
    #                                listcon.append(con2)
    #                                # print(field_english)
    #                                # 设置动态变量，tablename被定义为obj
    #                            obj = getattr(_testmodel, tablename)
    #                            if len(listcon) == 1:
    #                                data = eval("obj.objects.filter(" + listcon[0] + "__icontains=condition1)")
    #                            elif len(listcon) == 2:
    #                                data = eval("obj.objects.filter(" + listcon[0] + "__icontains=condition1," + listcon[1] + "__icontains=condition2)")
    #                            elif len(listcon) == 3:
    #                                data = eval(
    #                                    "obj.objects.filter(" + listcon[0] + "__icontains=condition1," + listcon[1] + "__icontains=condition2," + listcon[
    #                                        2] + "__icontains=condition3)")
    #                            elif len(listcon) == 4:
    #                                data = eval(
    #                                    "obj.objects.filter(" + listcon[0] + "__icontains=condition1," + listcon[1] + "__icontains=condition2," + listcon[
    #                                        2] + "__icontains=condition3," + listcon[3] + "__icontains=condition4)")
    #                            elif len(listcon) == 5:
    #                                data = eval(
    #                                    "obj.objects.filter(" + listcon[0] + "__icontains=condition1," + listcon[1] + "__icontains=condition2," + listcon[
    #                                        2] + "__icontains=condition3," + listcon[3] + "__icontains=condition4," + listcon[4] + "__icontains=condition5)")
    #                            if len(data) > 0:
    #                                lists = []
    #                                # 获取返回字段
    #                                field = Fieldapi.objects.filter(idapi=datawayapi)
    #                                # 创建包含返回字段的列表listfield（ 形式如：['LXDH', 'SAWPBH'] ）
    #                                listfield = []
    #                                # 循环遍历，匹配Fieldapi表中相应数据,并获取fieldData的值，（ 单条fieldData形式如：{'field_chinese': '涉案物品编号', 'field_english': 'SAWPBH', 'show_type': 'string'}  ）
    #                                for num in range(len(field)):
    #                                    field1 = json.loads(field[num].fieldData)
    #                                    # 将单条的fieldData中的field_english取出，作为我们返回字段的变量名
    #                                    field2 = (field1['field_english'])
    #                                    # 添加到返回字段的列表listfield中
    #                                    listfield.append(field2)
    #                                # 遍历我们查询的表的数据并最终返回相应json数据
    #                                for num in range(len(data)):
    #                                    # 遍历返回字段的列表listfield，将返回字段按照顺序依次排列
    #                                    for number in range(len(listfield)):
    #                                        temp = {
    #                                            # 一条返回数据
    #                                            eval(' " ' + listfield[number] + ' " '): eval('data[num].' + listfield[number]),
    #                                        }
    #                                        lists.append(temp)
    #                                Protslog = InterfacejournalProtslog()
    #                                # Protslog.username = username
    #                                # Protslog.password = password
    #                                Protslog.apiid = datawayapi
    #                                # Protslog.data = datas
    #                                Protslog.requesttime = requesttime
    #                                Protslog.returnvalue = lists
    #                                Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                                Protslog.save()
    #                                return HttpResponse(json.dumps(lists, indent=4), content_type="application/json")
    #                            else:
    #                                result.append("004,查询条件有误")
    #                                Protslog = InterfacejournalProtslog()
    #                                # Protslog.username = username
    #                                # Protslog.password = password
    #                                # Protslog.apiid = datawayapi
    #                                # Protslog.data = datas
    #                                Protslog.requesttime = requesttime
    #                                Protslog.returnvalue = result
    #                                Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                                Protslog.save()
    #                                return JsonResponse({"error": result})
    #                        else:
    #                            result.append("003,无查询条件")
    #                            Protslog = InterfacejournalProtslog()
    #                            # Protslog.username = username
    #                            # Protslog.password = password
    #                            # Protslog.apiid = datawayapi
    #                            # Protslog.data = datas
    #                            Protslog.requesttime = requesttime
    #                            Protslog.returnvalue = result
    #                            Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                            Protslog.save()
    #                            return JsonResponse({"error": result})

    #                    else:
    #                        print(datawayapi)
    #                        if Conditionapi.objects.filter(idapi=datawayapi):
    #                            result.append("005,请输入查询条件")
    #                            Protslog = InterfacejournalProtslog()
    #                            # Protslog.username = username
    #                            # Protslog.password = password
    #                            # Protslog.apiid = datawayapi
    #                            # Protslog.data = datas
    #                            Protslog.requesttime = requesttime
    #                            Protslog.returnvalue = result
    #                            Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                            Protslog.save()
    #                            return JsonResponse({"error": result})
    #                        else:
    #                            # print(field_english)
    #                            # 设置动态变量，tablename被定义为obj
    #                            # 设置动态变量，tablename被定义为obj
    #                            obj = getattr(_testmodel, tablename)
    #                            # 使用eval函数拼接，获取最终想要数据的集合
    #                            data = obj.objects.all()
    #                            lists = []
    #                            # 获取返回字段
    #                            field = Fieldapi.objects.filter(idapi=datawayapi)
    #                            # 创建包含返回字段的列表listfield（ 形式如：['LXDH', 'SAWPBH'] ）
    #                            listfield = []
    #                            # 循环遍历，匹配Fieldapi表中相应数据,并获取fieldData的值，（ 单条fieldData形式如：{'field_chinese': '涉案物品编号', 'field_english': 'SAWPBH', 'show_type': 'string'}  ）
    #                            for num in range(len(field)):
    #                                field1 = json.loads(field[num].fieldData)
    #                                # 将单条的fieldData中的field_english取出，作为我们返回字段的变量名
    #                                field2 = (field1['field_english'])
    #                                # 添加到返回字段的列表listfield中
    #                                listfield.append(field2)
    #                            # 遍历我们查询的表的数据并最终返回相应json数据
    #                            for num in range(len(data)):
    #                                # 遍历返回字段的列表listfield，将返回字段按照顺序依次排列
    #                                for number in range(len(listfield)):
    #                                    temp = {
    #                                        # 一条返回数据
    #                                        eval(' " ' + listfield[number] + ' " '): eval('data[num].' + listfield[number]),
    #                                    }
    #                                    lists.append(temp)
    #                            Protslog = InterfacejournalProtslog()
    #                            # Protslog.username = username
    #                            # Protslog.password = password
    #                            Protslog.apiid = datawayapi
    #                            # Protslog.data = datas
    #                            Protslog.requesttime = requesttime
    #                            Protslog.returnvalue = lists
    #                            Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                            Protslog.save()
    #                            return HttpResponse(json.dumps(lists, indent=4), content_type="application/json")
    #                else:
    #                    result.append("002,接口id不合法")
    #                    Protslog = InterfacejournalProtslog()
    #                    Protslog.username = username
    #                    Protslog.password = password
    #                    Protslog.apiid = datawayapi
    #                    # Protslog.data = datas
    #                    Protslog.requesttime = requesttime
    #                    Protslog.returnvalue = result
    #                    Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                    Protslog.save()
    #                    return JsonResponse({"error": result})
    #            else:
    #                result.append("007,没有权限调用接口")
    #                # datas = request.POST.get('datas')
    #                # username = (datas['username'])
    #                # password = (datas['password'])
    #                Protslog = InterfacejournalProtslog()
    #                # Protslog.username = username
    #                # Protslog.password = password
    #                # Protslog.apiid = datawayapi
    #                # Protslog.data = datas
    #                Protslog.requesttime = requesttime
    #                Protslog.returnvalue = result
    #                Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #                Protslog.save()
    #                return JsonResponse({"error": result})
    #        else:
    #            result.append("008,账户密码错误")
    #            # datas = request.POST.get('datas')
    #            # username = (datas['username'])
    #            # password = (datas['password'])
    #            Protslog = InterfacejournalProtslog()
    #            # Protslog.username = username
    #            # Protslog.password = password
    #            # Protslog.apiid = datawayapi
    #            # Protslog.data = datas
    #            Protslog.requesttime = requesttime
    #            Protslog.returnvalue = result
    #            Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #            Protslog.save()
    #            return JsonResponse({"error": result})

    #    else:
    #        result.append("006,用户名错误")
    #        # datas = request.POST.get('datas')
    #        # username = (datas['username'])
    #        # password = (datas['password'])
    #        Protslog = InterfacejournalProtslog()
    #        # Protslog.username = username
    #        # Protslog.password = password
    #        # Protslog.apiid = datawayapi
    #        # Protslog.data = datas
    #        Protslog.requesttime = requesttime
    #        Protslog.returnvalue = result
    #        Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #        Protslog.save()
    #        return JsonResponse({"error": result})

    #else:
    #    result.append("001,请求方式不合法")
    #    # datas = request.POST.get('datas')
    #    # username = (datas['username'])
    #    # password = (datas['password'])
    #    Protslog = InterfacejournalProtslog()
    #    # Protslog.username = username
    #    # Protslog.password = password
    #    # Protslog.apiid = datawayapi
    #    # Protslog.data = datas
    #    Protslog.requesttime = requesttime
    #    Protslog.returnvalue = result
    #    Protslog.returntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #    Protslog.save()
    #    return JsonResponse({"error": result})


#第一个选项卡
# 加载数据 # 点击datagrid的分页按钮，自动向后台发送2个参数, rows和page，代表每页记录数和页索引
def showData(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    #create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
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

#后台删除方法
def delData(request):
    stp = request.GET.getlist("data")
    idstring = ','.join(stp)
    cataloguecount = Cataloguedatawaybm.objects.filter(idapi=idstring)
    for num in range(len(cataloguecount)):
        count = str(cataloguecount[num].typeid)
        idcount1 = count[0:1]
        idcount2 = count[0:4]
        idcount3 = count[0:7]
        countdata = Cataloguedataway.objects.get(typeid=idcount1)
        countdata.count = countdata.count - 1
        countdata.save()
        if idcount2 != '' and len(idcount2) == 4:
            cl2 = Cataloguedataway.objects.get(typeid=idcount2)
            cl2.count = cl2.count - 1
            cl2.save()
            if idcount3 != '' and len(idcount3) == 7:
                cl3 = Cataloguedataway.objects.get(typeid=idcount3)
                cl3.count = cl3.count - 1
                cl3.save()


    Adminapi.objects.extra(where=['idapi IN (' + idstring + ')']).delete()
    Fieldapi.objects.extra(where=['idapi IN (' + idstring + ')']).delete()
    Conditionapi.objects.extra(where=['idapi IN (' + idstring + ')']).delete()
    Cataloguedatawaybm.objects.extra(where=['idapi IN (' + idstring + ')']).delete()
    return HttpResponseRedirect('/dataway/index/')


#保存并刷新drag1
def dragData(request):
    a = request.POST.get('dataid')
    # page = int(request.POST.get('page'))
    # rows = int(request.POST.get('rows'))
    # start = (page - 1) * rows
    # end = page * rows
    counts = FieldTable.objects.filter(tableid = a).count()
    data = FieldTable.objects.filter(tableid = a)#[start:end]
    dragDataList = []
    for num in range(len(data)):
        temp = {
            "field_english": data[num].fieldenglish,
            "field_chinese": data[num].fieldchinese,
            "show_type": data[num].showtype,
        }
        dragDataList.append(temp)
    return JsonResponse({'total':counts,'rows': dragDataList})

def saveData(request):
    result = {'errorCode':'0x0000', 'errorString': ''}
    idapi = request.POST.get('idapi11')
    if len(idapi) < 10 :
        hierarchy3 = request.POST.get('hierarchy3')
        print(hierarchy3)
        data3 = json.loads(hierarchy3)
        nameapi = request.POST.get('nameapi')
        namewarehouse = request.POST.get('namewarehouse')
        nametable = request.POST.get('nametable')
        hierarchy1 = request.POST.get('hierarchy1')
        hierarchy2 = request.POST.get('hierarchy2')
        idapi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        for num in range(len(data3)):
            cataloguedata = data3[num]
            bianmudataway = Cataloguedatawaybm()
            bianmudataway.cataloguename = cataloguedata['cataloguename']
            bianmudataway.typeid = cataloguedata['id']
            bianmudataway.idapi = idapi
            bianmudataway.save()
            a = bianmudataway.typeid
            print(a)
            idcount = str(a)
            idcount1 = idcount[0:1]
            idcount2 = idcount[0:4]
            idcount3 = idcount[0:7]
            catalogue = Cataloguedataway.objects.get(typeid=idcount1)
            catalogue.count = catalogue.count + 1
            catalogue.save()
            if idcount2 != '' and len(idcount2) == 4:
                cl2 = Cataloguedataway.objects.get(typeid=idcount2)
                cl2.count = cl2.count + 1
                cl2.save()
                if idcount3 != '' and len(idcount3) == 7:
                    cl3 = Cataloguedataway.objects.get(typeid=idcount3)
                    cl3.count = cl3.count + 1
                    cl3.save()

        # Adminapi, Fieldapi, Conditionapi

        AdminapiData = Adminapi()
        AdminapiData.nameapi = nameapi
        AdminapiData.idapi = idapi
        AdminapiData.warehouseapi = namewarehouse
        AdminapiData.tableapi = nametable
        # AdminapiData.typeid = typeid
        AdminapiData.createtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        AdminapiData.save()

        data1 = json.loads(hierarchy1)
        for num in range(len(data1)):
            FieldapiData = Fieldapi()
            FieldapiData.fieldData = json.dumps(data1[num])
            FieldapiData.idapi = idapi
            FieldapiData.save()

        data2 = json.loads(hierarchy2)
        for num in range(len(data2)):
            ConditionapiData = Conditionapi()
            ConditionapiData.conditionname = json.dumps(data2[num])
            ConditionapiData.idapi = idapi
            ConditionapiData.save()
        return JsonResponse(result)

    elif len(idapi) > 10:
        idapi = request.POST.get('idapi11')
        print(idapi)

        cataloguecount = Cataloguedatawaybm.objects.filter(idapi=idapi)
        for num in range(len(cataloguecount)):
            count = str(cataloguecount[num].typeid)
            idcount1 = count[0:1]
            idcount2 = count[0:4]
            idcount3 = count[0:7]
            idcount4 = count[0:10]
            countdata = Cataloguedataway.objects.get(typeid=idcount1)
            countdata.count = countdata.count - 1
            countdata.save()
            if idcount2 != '' and len(idcount2) == 4:
                cl2 = Cataloguedataway.objects.get(typeid=idcount2)
                cl2.count = cl2.count - 1
                cl2.save()
                if idcount3 != '' and len(idcount3) == 7:
                    cl3 = Cataloguedataway.objects.get(typeid=idcount3)
                    cl3.count = cl3.count - 1
                    cl3.save()


        nameapi = request.POST.get('nameapi')
        namewarehouse = request.POST.get('namewarehouse')
        nametable = request.POST.get('nametable')
        hierarchy1 = request.POST.get('hierarchy1')
        print(hierarchy1)
        hierarchy2 = request.POST.get('hierarchy1')

        hierarchy3 = request.POST.get('hierarchy3')
        data3 = json.loads(hierarchy3)
        for num in range(len(data3)):
            cataloguedata = data3[num]
            bianmudataway = Cataloguedatawaybm()
            bianmudataway.cataloguename = cataloguedata['cataloguename']
            bianmudataway.typeid = cataloguedata['id']
            bianmudataway.idapi = idapi
            bianmudataway.save()
            a = bianmudataway.typeid
            print(a)
            idcount = str(a)
            idcount1 = idcount[0:1]
            idcount2 = idcount[0:4]
            idcount3 = idcount[0:7]
            catalogue = Cataloguedataway.objects.get(typeid=idcount1)
            catalogue.count = catalogue.count + 1
            catalogue.save()
            if idcount2 != '' and len(idcount2) == 4:
                cl2 = Cataloguedataway.objects.get(typeid=idcount2)
                cl2.count = cl2.count + 1
                cl2.save()
                if idcount3 != '' and len(idcount3) == 7:
                    cl3 = Cataloguedataway.objects.get(typeid=idcount3)
                    cl3.count = cl3.count + 1
                    cl3.save()

                    # Adminapi, Fieldapi, Conditionapi
                    AdminapiData = Adminapi.objects.filter(idapi=idapi)
                    AdminapiData.nameapi = nameapi
                    AdminapiData.idapi = idapi
                    print(AdminapiData.idapi)
                    AdminapiData.warehouseapi = namewarehouse
                    AdminapiData.tableapi = nametable
                    AdminapiData.createtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(AdminapiData.createtime)
                    Adminapi.objects.extra(where=['idapi IN (' + idapi + ')']).update(nameapi=nameapi,warehouseapi=namewarehouse,tableapi=nametable,createtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
                    print(111)
                    Fieldapi.objects.extra(where=['idapi IN (' + idapi + ')']).delete()
                    Conditionapi.objects.extra(where=['idapi IN (' + idapi + ')']).delete()
                    print(222)
                    data1 = json.loads(hierarchy1)
                    for num in range(len(data1)):
                        FieldapiData = Fieldapi()
                        FieldapiData.fieldData = json.dumps(data1[num])
                        FieldapiData.idapi = idapi
                        print(FieldapiData.idapi)
                        FieldapiData.save()

                    data2 = json.loads(hierarchy2)
                    for num in range(len(data2)):
                        ConditionapiData = Conditionapi()
                        ConditionapiData.conditionname = json.dumps(data2[num])
                        ConditionapiData.idapi = idapi
                        ConditionapiData.save()
                    return JsonResponse(result)
                else:
                    result.errorCode = '0x0002'
                    result.errorString = '参数错误'
                return JsonResponse(result)


#增加编目
def catalogue(request):
    result = {'errorCode': '0x0000', 'errorString': ''}
    if request.method == 'POST':
        catalogueid = request.POST.get('ids')
        catalogueidData = catalogueid.split(',')
        for num in range(len(catalogueidData)):
            catalogueData = Adminapi(typeid=request.POST.get('typeid'))
            catalogueData.typeid = catalogueidData[num]
            catalogue = Cataloguedataway.objects.get(typeid=catalogueData.typeid)
            catalogueData.cataloguename = catalogue.cataloguename
            catalogueData.save()
        return JsonResponse(result)
    else:
        result.errorCode = '0x0002'
        result.errorString = '参数错误'
    return JsonResponse(result)

# 查看详情
def datawayfield(request):
    dataidapi = request.POST.get('dataidapi', 0)
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    counts = Fieldapi.objects.filter(idapi=dataidapi).count()
    data = Fieldapi.objects.filter(idapi=dataidapi)[start:end]
    list = []
    for num in range(len(data)):
        list.append(json.loads(data[num].fieldData))
    return JsonResponse({'total':counts,'rows': list})

def datawaycondition(request):
    dataidapi = request.POST.get('dataidapi', 0)
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    counts = Conditionapi.objects.filter(idapi=dataidapi).count()
    data = Conditionapi.objects.filter(idapi=dataidapi)[start:end]
    list = []
    for num in range(len(data)):
        list.append(json.loads(data[num].conditionname))
    return JsonResponse({'total':counts,'rows': list})


# 数据比对接口
def compareData(request):
    # 来源数据库连接信息
    srcDbHost = request.GET.get('srcDbHost', '')
    srcDbPort = request.GET.get('srcDbPort', '')
    srcDbType = request.GET.get('srcDbType', '')
    srcDbUsername = request.GET.get('srcDbUsername', '')
    srcDbPassword = request.GET.get('srcDbPassword', '')
    srcDbName = request.GET.get('srcDbName', '')
    # 检测连接信息是否完整
    if srcDbHost == '' or srcDbPort == '' or srcDbType == '' or srcDbUsername == '' or srcDbPassword == '':
        result = {'errorCode':'0x0001', 'errorMessage':'来源数据库连接信息不完整'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 检测端口号
    try:
        srcDbPort = int(srcDbPort)
    except:
        result = {'errorCode':'0x0002', 'errorMessage':'来源数据库端口号必须为数字'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 检测数据库类型
    try:
        srcDbType = int(srcDbType)
    except:
        result = {'errorCode':'0x0003', 'errorMessage':'未知的数据库产品'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    if srcDbType != 1 and srcDbType != 2:
        result = {'errorCode':'0x0004', 'errorMessage':'不支持的数据产品'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 检测是否能连通来源数据库
    if srcDbName == '':
        result = {'errorCode':'0x0005', 'errorMessage':'未指定来源数据库'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    try:
        if srcDbType == 1:
            srcDbConn = cx_Oracle.connect(srcDbUsername, srcDbPassword, srcDbHost + ':' + str(srcDbPort) + '/' + srcDbName)
        elif srcDbType == 2:
            srcDbConn = pymysql.connect(host=srcDbHost, port=srcDbPort, user=srcDbUsername, passwd=srcDbPassword, db=srcDbName, charset='utf8')
    except:
        result = {'errorCode':'0x0006', 'errorMessage':'来源数据库无法连通'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 检测来源数据库有没有指定的表
    srcTable = request.GET.get('srcTable', '')
    if srcTable == '':
        result = {'errorCode':'0x0007', 'errorMessage':'未指定来源数据表'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    srcTables = []
    if srcDbType == 1:
        sql = 'select table_name from tabs'
    elif srcDbType == 2:
        sql = 'show tables'
    srcDbCur = srcDbConn.cursor()
    srcDbCur.execute(sql)
    for row in srcDbCur.fetchall():
        srcTables.append(row[0])
    if len(srcTables) == 0:
        result = {'errorCode':'0x0008', 'errorMessage':'从来源数据库中扫描不到表信息'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    tableIsExists = False
    for item in srcTables:
        if item.lower() == srcTable.lower():
            tableIsExists = True
            break
    if tableIsExists == False:
        result = {'errorCode':'0x0009', 'errorMessage':'从来源数据库中找不到指定表'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 本地数据库校验
    engineName = DATABASES[STANDARDDB]['ENGINE'].split(',')[-1]
    localDbType = 1 # 默认为Oracle
    if engineName.lower() == 'oracle':
        localDbType = 1
    elif engineName.lower() == 'mysql':
        localDbType = 2
    localDbHost = DATABASES[STANDARDDB]['HOST']
    localDbPort = DATABASES[STANDARDDB]['PORT']
    localDbUsername = DATABASES[STANDARDDB]['USER']
    localDbPASSWORD = DATABASES[STANDARDDB]['PASSWORD']
    localDbName = DATABASES[STANDARDDB]['NAME']
    try:
        if localDbType == 1:
            localDbConn = cx_Oracle.connect(localDbUsername, localDbPASSWORD, localDbHost + ':' + localDbPort + '/' + localDbName)
        elif localDbType == 2:
            localDbConn = pymysql.connect(host=localDbHost, port=int(localDbPort), user=localDbUsername, passwd=localDbPASSWORD, db=localDbName, charset='utf8')
    except:
        result = {'errorCode':'0x0011', 'errorMessage':'本地数据库无法连通'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    destTable = request.GET.get('destTable', '')
    if destTable == '':
        result = {'errorCode':'0x0012', 'errorMessage':'未指定目标表'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    destTables = []
    if localDbType == 1:
        sql = 'select table_name from tabs'
    elif localDbType == 2:
        sql = 'show tables'
    localDbCur = localDbConn.cursor()
    localDbCur.execute(sql)
    for row in localDbCur.fetchall():
        destTables.append(row[0])
    if len(destTables) == 0:
        result = {'errorCode':'0x0013', 'errorMessage':'目标数据库中扫描不到表信息'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    tableIsExists = False
    for item in destTables:
        if item.lower() == destTable.lower():
            tableIsExists = True
            break
    if tableIsExists == False:
        result = {'errorCode':'0x0014', 'errorMessage':'目标数据库中找不到指定表'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 字段检测
    fieldMaps = request.GET.getlist('fieldMap')
    if len(fieldMaps) == 0:
        result = {'errorCode':'0x0015', 'errorMessage':'必须指定比对字段映射关系'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 检测来源表结构（检测字段和本地新建临时表时需要用到）
    if srcDbType == 1:
        sql = "select column_name, data_type, data_length from user_tab_columns where table_name = '" + srcTable + "'"
    elif srcDbType == 2:
        sql = 'select column_name, data_type from information_schema.columns where table_schema = "' + srcDbName + '" and table_name = "' + srcTable + '"'
    srcDbFields = [] # 封装来源库字段信息
    srcDbCur.execute(sql)
    for row in srcDbCur.fetchall():
        temp = {}
        if srcDbType == 1:
            temp['name'] = row[0]
            temp['type'] = row[1]
            temp['length'] = row[2]
        elif srcDbType == 2:
            temp['name'] = row[0]
            temp['type'] = row[1]
        srcDbFields.append(temp)
    localDbFields = [] # 封装本地库字段信息
    if localDbType == 1:
        sql = "select column_name, data_type, data_length from user_tab_columns where table_name = '" + destTable + "'"
    elif localDbType == 2:
        sql = 'select column_name, data_type from information_schema.columns where table_schema = "' + localDbName + '" and table_name = "' + destTable + '"'
    localDbCur.execute(sql)
    for row in localDbCur.fetchall():
        temp = {}
        if srcDbType == 1:
            temp['name'] = row[0]
            temp['type'] = row[1]
            temp['length'] = row[2]
        elif srcDbType == 2:
            temp['name'] = row[0]
            temp['type'] = row[1]
        localDbFields.append(temp)
    # 判断是否有不存在的列
    for fieldMap in fieldMaps:
        fields = fieldMap.split(',')
        if len(fields) == 1: # 只写了一个的情况，检测两边
            field = fields[0]
            if field == '': # 忽略未输入项
                continue
            fieldIsExists = False
            for f in srcDbFields:
                if f['name'].lower() == field.lower():
                    fieldIsExists = True
                    break
            if fieldIsExists == False:
                result = {'errorCode':'0x0010', 'errorMessage':'来源数据表中没有指定列：' + field}
                return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
            fieldIsExists = False
            for f in localDbFields:
                if f['name'].lower() == field.lower():
                    fieldIsExists = True
                    break
            if fieldIsExists == False:
                result = {'errorCode':'0x0016', 'errorMessage':'目标数据库中没有指定列：' + field}
                return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
        elif len(fields) == 2: # 书写了两个的情况，分别检测两边
            fieldA = fields[0]
            fieldB = fields[1]
            if fieldA == '' or fieldB == '':
                result = {'errorCode':'0x0017', 'errorMessage':'正确的映射格式（A,B），但未指定列名'}
                return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
            fieldIsExists = False
            for f in srcDbFields:
                if f['name'].lower() == fieldA.lower():
                    fieldIsExists = True
                    break
            if fieldIsExists == False:
                result = {'errorCode':'0x0010', 'errorMessage':'来源数据表中没有指定列：' + fieldA}
                return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
            fieldIsExists = False
            for f in localDbFields:
                if f['name'].lower() == fieldB.lower():
                    fieldIsExists = True
                    break
            if fieldIsExists == False:
                result = {'errorCode':'0x0016', 'errorMessage':'目标数据库中没有指定列：' + fieldB}
                return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    # 数据比对类型
    compareType = request.GET.get('compareType', '')
    if compareType == '':
        result = {'errorCode':'0x0018', 'errorMessage':'未指定比对类型'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    try:
        compareType = int(compareType)
    except:
        result = {'errorCode':'0x0019', 'errorMessage':'错误的比对类型'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    if compareType != 1 and compareType != 2:
        result = {'errorCode':'0x0020', 'errorMessage':'不支持的比对类型'}
        return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
    if compareType == 1:
        # 新建临时表
        tempTableName = ''
        for i in range(15):
            tempTableName = tempTableName + chr(random.randint(65, 90))
        sql = 'create table ' + tempTableName + ' as select * from ' + destTable + ' where 1 = 0'
        try:
            localDbCur.execute(sql)
        except:
            result = {'errorCode':'0x0021', 'errorMessage':'新建临时表失败'}
            return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
        # 采集数据
        selectfields = []
        for fieldMap in fieldMaps:
            fields = fieldMap.split(',')
            if fields[0] != '':
                selectfields.append(fields[0])
        insertfields = []
        for fieldMap in fieldMaps:
            fields = fieldMap.split(',')
            if len(fields) == 1 and fields[0] != '':
                insertfields.append(fields[0])
            elif len(fields) == 2:
                insertfields.append(fields[1])
        try:
            sql = 'select distinct ' + ','.join(selectfields) + ' from ' + srcTable
            srcDbCur.execute(sql)
            if localDbType == 1:
                sql = 'insert into ' + tempTableName + '(' + ','.join(insertfields) + ') values ('
                for i in range(len(selectfields)):
                    sql = sql + ':' + str(i + 1) + ','
                sql = sql[:len(sql) - 1] + ')'
                for row in srcDbCur.fetchall():
                    localDbCur.execute(sql, row)
            elif localDbType == 2:
                sql = 'insert into ' + tempTableName + '(' + ','.join(insertfields) + ') values ('
                for i in range(len(selectfields)):
                    sql = sql + '%s,'
                sql = sql[:len(sql) - 1] + ')'
                for row in srcDbCur.fetchall():
                    localDbCur.execute(sql, row)
            localDbConn.commit()
        except:
            result = {'errorCode':'0x0022', 'errorMessage':'从来源表抓取数据失败'}
            return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
        try:
            sql = 'select ' + ','.join(insertfields) + ' from ' + tempTableName + ' where not exists ('
            sql = sql + 'select ' + ','.join(insertfields) + ' from ' + destTable + ' where '
            for field in insertfields:
                sql = sql + tempTableName + '.' + field + '=' + destTable + '.' + field + ' and '
            sql = sql[:len(sql) - 5]
            sql = sql + ')'
            localDbCur.execute(sql)
            # 将比对差异返回
            resultData = []
            columnInfo = localDbCur.description
            for row in localDbCur.fetchall():
                record = []
                for i in range(len(columnInfo)):
                    kv = {}
                    kv['name'] = columnInfo[i][0]
                    kv['value'] = row[i]
                    record.append(kv)
                resultData.append(record)
            return render_to_response('dataway/compareSuccessMessage.xml', {'data': resultData}, content_type='application/xml')
        except:
            result = {'errorCode':'0x0023', 'errorMessage':'比对数据失败'}
            localDbCur.execute('drop table ' + tempTableName) # 这里应该写日志文件，方便手动删除表
            return render_to_response('dataway/compareErrorMessage.xml', result, content_type='application/xml')
        finally:
            localDbCur.execute('drop table ' + tempTableName) # 这里应该写日志文件，方便手动删除表
            srcDbConn.close()
            localDbConn.close()
    elif compareType == 2:
        # TODO 增量比对
        pass
