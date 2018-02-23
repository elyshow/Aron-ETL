from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import urllib,urllib.request,urllib.error,sys,urllib.parse
from django.conf import settings
from .models import BaseType
from .models import DataInterface
from taskApp.models import ApiData
from .models import RunTask
from .models import FileDownload
from codeStandard.models import DataBase
from .models import InfoFile,DataIncrement
from taskApp.models import InfoSqlFile
from .models import TimeTask
from taskType import dbConfigurationFile
import random, os, json, re
from taskApp import gobal
import time, subprocess
from taskType import tableGlobal
import pymysql
import cx_Oracle
from django.db import connection
# Create your views here.


#传文件类型的数据
def taskTypeDialog(request):
    fileType = request.POST['fileType']
    taskName = request.POST['taskName']
    belongto = request.POST['belongto']
    belongtype = request.POST['belongtype']
    baseData = BaseType.objects.all()
    bt = BaseType()
    fileid = str(random.random())[2:8]+str(time.localtime()[0])+str(time.localtime()[1])+str(time.localtime()[2])+str(time.localtime()[3])+str(time.localtime()[4])+str(time.localtime()[5])   #任务id由6位随机数和时间串组成
    while 1:
        i=0
        for b in baseData:
            if b.taskid ==fileid:
                i=1
        if i==1:
            fileid = int(fileid) + random.random()[2:3]
            fileid=str(fileid)
        else:
            break
    bt.taskid=fileid
    bt.domid=gobal.dataid
    bt.filetype=fileType
    bt.taskname = taskName
    bt.belongto = belongto
    bt.belongtype = belongtype
    bt.taskstate='1'
    bt.save()
    if request.method == "POST":  # 请求方法为POST时，进行处理
        myFile = request.FILES.get("infoFileName", None)  # 获取上传的文件，如果没有文件，则默认为None
        format = myFile.name.split('.')[-1]
        if not myFile:
            return HttpResponse("no files for upload!")
        year = str(time.localtime()[0]) + '年'
        mon = str(time.localtime()[1]) + '月'
        day = str(time.localtime()[2]) + '日'
        try:
            pathFixd = os.makedirs(dbConfigurationFile.commonFileWay)
        except:
            print('communt already exist')
        commun = r""+dbConfigurationFile.commonFileWay+"" + '/' + year + '/' + mon + '/' + day + '/' + format
        if not os.path.exists(commun):
            os.makedirs(commun)  # 创建文件夹
        destination = open(os.path.join(commun, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()

    info = InfoFile()
    info.taskid = bt.taskid
    info.domid = gobal.dataid
    info.filename = myFile.name
    info.tasktype = format
    info.fileway = commun
    info.save()
    return HttpResponse(json.dumps(fileType), content_type='application/json')

# 普通文件远程下载
def taskDownloadDialog(request):
    fileType = request.GET['fileType']
    taskName = request.GET['taskName']
    belongto = request.GET['belongto']
    belongtype = request.GET['belongtype']
    ipInfo = request.GET['ipInfo']
    pwdInfo = request.GET['pwdInfo']
    pathInfo = request.GET['pathInfo']
    username = request.GET['username']
    baseData = BaseType.objects.all()
    bt = BaseType()
    downloadid = str(random.random())[2:8]+str(time.localtime()[0])+str(time.localtime()[1])+str(time.localtime()[2])+str(time.localtime()[3])+str(time.localtime()[4])+str(time.localtime()[5])  #任务id由6位随机数和时间串组成
    while 1:
        i = 0
        for b in baseData:
            if b.taskid == downloadid:
                i = 1
        if i == 1:
            downloadid = int(downloadid) + random.random()[2:3]
            downloadid = str(downloadid)
        else:
            break
    bt.taskid=downloadid
    bt.filetype=fileType
    bt.domid=gobal.dataid
    bt.taskname = taskName
    bt.belongto = belongto
    bt.belongtype = belongtype
    bt.taskstate = '1'
    bt.save()

    fd=FileDownload()
    fd.taskid=bt.taskid
    fd.domid=gobal.dataid
    fd.ipinfo=ipInfo
    fd.pwdinfo=pwdInfo
    fd.pathinfo=pathInfo
    fd.username=username
    fd.save()
    return HttpResponse(json.dumps(fileType), content_type='application/json')

# 上传数据库文件
def taskSqlDialog(request):
    fileType = request.POST['fileType']
    taskName = request.POST['taskName']
    belongto = request.POST['belongto']
    belongtype = request.POST['belongtype']
    sqlType = request.POST['sqlType']
    baseData = BaseType.objects.all()
    bt = BaseType()
    sqlFileId = str(random.random())[2:8]+str(time.localtime()[0])+str(time.localtime()[1])+str(time.localtime()[2])+str(time.localtime()[3])+str(time.localtime()[4])+str(time.localtime()[5])   #任务id由6位随机数和时间串组成
    while 1:
        i = 0
        for b in baseData:
            if b.taskid == sqlFileId:
                i = 1
        if i == 1:
            sqlFileId = int(sqlFileId) + random.random()[2:3]
            sqlFileId = str(sqlFileId)
        else:
            break
    bt.taskid=sqlFileId
    bt.domid=gobal.dataid
    bt.filetype=fileType
    bt.taskname = taskName
    bt.belongto = belongto
    bt.belongtype = belongtype
    bt.taskstate = '1'
    bt.save()

    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("infoSqlName", None)    # 获取上传的文件，如果没有文件，则默认为None
        format = myFile.name.split('.')[-1]
        if not myFile:
            return HttpResponse("no files for upload!")
        year = str(time.localtime()[0])+'年'
        mon = str(time.localtime()[1])+'月'
        day = str(time.localtime()[2])+'日'
        try:
            os.makedirs(dbConfigurationFile.sqlFileWay)
        except:
            print('communt already exist')
        commun=r""+dbConfigurationFile.sqlFileWay+""+'/'+year+'/'+mon+'/'+day+'/'+format
        if not os.path.exists(commun):
           os.makedirs(commun)  #创建文件夹
        destination = open(os.path.join(commun,myFile.name),'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        info = InfoSqlFile()
        info.taskid = bt.taskid
        info.domid = gobal.dataid
        info.filename = myFile.name
        info.tasktype = sqlType
        info.fileway = commun
        info.save()
    return HttpResponse(json.dumps(fileType), content_type='application/json')

#传数据接口类型的数据,读出表
def dataInterDialog(request):
    databasetype = request.GET['databaseType']
    databasename = request.GET['databaseName']
    fwqadress = request.GET['fwqAdress']
    username = request.GET['userName']
    pwd = request.GET['pwd']
    port = request.GET['dkName']
    if databasetype == 'mysql':
        conn = pymysql.connect(host=fwqadress, port=int(port), user=username, password=pwd,
                               db=databasename, charset='utf8')
        tableNameSQL = "show tables;"
    elif databasetype == 'oracle':
        conn = cx_Oracle.connect(username, pwd, '%s:%s/%s' % (fwqadress, port, databasename))
        tableNameSQL = "SELECT  table_name FROM user_tables"
    cur = conn.cursor()
    cur.execute(tableNameSQL)
    allTableName = []
    table_list = cur.fetchall()
    tablecount = len(table_list)
    for index in range(tablecount):
        a = table_list[index]
        temp = a[0]
        allTableName.append(temp)
    return allTableName

# 根据选中的表，读出对应的字段
def tableToDialog(request):
    databasetype = request.GET['databaseType']
    databasename = request.GET['databaseName']
    fwqadress = request.GET['fwqAdress']
    username = request.GET['userName']
    pwd = request.GET['pwd']
    tablename = request.GET['tableName']
    port = request.GET['dkName']
    allField = []
    if databasetype == 'mysql':
        conn = pymysql.connect(host=fwqadress, port=int(port), user=username, password=pwd,
                               db=databasename, charset='utf8')
        fieldNameSQL = "desc " + tablename + ""
        cur = conn.cursor()
        cur.execute(fieldNameSQL)
        tablen = cur.fetchall()
        cur.close()
        conn.close()
        zj = ''
        for type_ziduan in tablen:
            for zhujian in type_ziduan:
                if zhujian == 'PRI':
                    zj = type_ziduan[0]

        tablecount = len(tablen)

        d = []
        e = []
        for index in range(tablecount):
            a = tablen[index]
            temp = a[0]
            type = a[1]
            dd = temp + ',' + type
            if temp != zj:
                allField.append(temp)
            d.append(type)
            e.append(dd)
        tableGlobal.ziduantype = e
        allField.append(zj)
    elif databasetype == 'oracle':
        conn = cx_Oracle.connect(username, pwd, '%s:%s/%s' % (fwqadress, port, databasename))
        cur = conn.cursor()
        primaryKeySQL = """SELECT
            UCC.COLUMN_NAME
        FROM
            USER_CONSTRAINTS UC,
            USER_CONS_COLUMNS UCC
        WHERE
            UC.CONSTRAINT_NAME = UCC.CONSTRAINT_NAME
        AND UC.TABLE_NAME = '%s'
        AND CONSTRAINT_TYPE = 'P'""" % tablename
        cur.execute(primaryKeySQL)
        primaryKeyRes = cur.fetchall()
        primaryKeyName = primaryKeyRes[0][0] if primaryKeyRes else ''

        fieldNameSQL = "select COLUMN_NAME, DATA_TYPE||'('||DATA_LENGTH||')' as COLUMN_TYPE from user_tab_columns where table_name='" + tablename + "'"
        cur.execute(fieldNameSQL)
        fieldNameRes = cur.fetchall()
        d = []
        e = []
        for i in range(len(fieldNameRes)):
            row = fieldNameRes[i]
            temp = row[0]
            type = row[1]
            dd = temp + ',' + type
            if row[0] != primaryKeyName:
                allField.append(row[0])
            d.append(type)
            e.append(dd)
        tableGlobal.ziduantype = e
        allField.append(primaryKeyName)
    return allField

# 选中对应的字段，并在本机数据库有对应操作
def fieldToDialog(request):
    #保存到Datainterface
    pri = request.GET['priName']
    fileType = request.GET['fileType']
    taskname = request.GET['taskName']
    belongto = request.GET['belongto']
    belongtype = request.GET['belongtype']
    sjyname = request.GET['sjyName']
    databasetype = request.GET['databaseType']
    incrementWay = request.GET['incrementWay']
    dkname = request.GET['dkName']
    databasename = request.GET['databaseName']
    fwqadress = request.GET['fwqAdress']
    username = request.GET['userName']
    pwd = request.GET['pwd']
    tablename = request.GET['tableName']
    listdata = request.GET.getlist('fieldName')
    listdata.append(pri)
    dataInfo=DataInterface()
    dataInfo.domid = gobal.dataid
    baseData = BaseType.objects.all()
    sqlId = str(random.random())[2:8] + str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2]) + str(time.localtime()[3]) + str(time.localtime()[4]) + str(time.localtime()[5])  # 任务id由6位随机数和时间串组成
    while 1:
        i = 0
        for b in baseData:
            if b.taskid == sqlId:
                i = 1
        if i == 1:
            sqlId = int(sqlId) + random.random()[2:3]
            sqlId = str(sqlId)
        else:
            break
    dataInfo.id = sqlId
    dataInfo.sjyname = sjyname
    dataInfo.databasename = databasename
    dataInfo.databasetype = databasetype
    dataInfo.fwqadress = fwqadress
    dataInfo.incrementway = incrementWay
    dataInfo.dkname = dkname
    dataInfo.username = username
    dataInfo.pwd = pwd
    dataInfo.ziduanname = listdata
    dataInfo.tablename = tablename
    dataInfo.save()
   #保存到Basetype
    by=BaseType()
    by.taskid = dataInfo.id
    by.domid = dataInfo.domid
    by.filetype = fileType
    by.taskname = taskname
    by.belongto = belongto
    by.belongtype = belongtype
    by.taskstate='1'
    by.save()

    # 定时刷新保存到Timetask表
    FreSetting = request.GET['FreSetting']
    print(type(FreSetting))
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
            tt = TimeTask()
            tt.taskid = dataInfo.id
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
            tt = TimeTask()
            tt.taskid = dataInfo.id
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
            tt = TimeTask()
            tt.taskid = dataInfo.id
            tt.schedule = FreSetting
            tt.rate = cycle
            tt.hours = h
            tt.minutes = m
            tt.save()
    elif FreSetting == '2':
        once_time = request.GET['once_time']
        tt = TimeTask()
        tt.taskid = dataInfo.id
        tt.schedule = FreSetting
        tt.runtime = once_time
        tt.save()
    elif FreSetting == '3':
        tt = TimeTask()
        tt.taskid = dataInfo.id
        tt.schedule = FreSetting
        tt.rate = 'hand'
        tt.save()
    elif FreSetting == '4':
        cycle = 'interv'
        interval_day = request.GET['interval_day']
        i = interval_day[1:-1]
        hours = request.GET['hours']
        h = hours[1:-1]
        minutes = request.GET['minutes']
        m = minutes[1:-1]
        tt = TimeTask()
        tt.taskid = dataInfo.id
        tt.schedule = FreSetting
        tt.runtime = i
        tt.rate = cycle
        tt.hours = h
        tt.minutes = m
        tt.save()
    conn = pymysql.connect(host=fwqadress, port=int(dkname), user=username, password=pwd,
                           db=databasename, charset='utf8')
    cur = conn.cursor()
    aa = ''
    bb = 0
    a = []
    b = ''
    sqq = "desc " + tablename + ""
    cur.execute(sqq)
    tablen = cur.fetchall()
    conn.commit()
    cur.close()
    conn = pymysql.connect(host=dbConfigurationFile.host, port=dbConfigurationFile.port, user=dbConfigurationFile.user, password=dbConfigurationFile.pwd,db=dbConfigurationFile.db, charset='utf8')
    cur = conn.cursor()
    PRI=''
    for type_ziduan in tablen:
        for zhujian in type_ziduan:
            if zhujian == 'PRI':
                PRI = type_ziduan[0]
    try:
        createDb = 'create database collectdb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
        cur.execute(createDb)
    except:
        print('database already create')
    try:
        createErrorDb = 'create database collecterrordb DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
        cur.execute(createErrorDb)
    except:
        print('db collecterrordb already exist')
    conn.select_db(dbConfigurationFile.collectdb)
    createtbNew=tablename+dataInfo.id
    for list1 in listdata:
        aa = str(list1)
        if bb < len(listdata) - 1:
            aa += ","
            bb += 1
        b += aa
        for cc in tableGlobal.ziduantype:
            a = cc.split(',')  # 分割字符串
            if a[0] == list1:
                try:
                    sq2 = "create table " + createtbNew + "(" + str(a[0]) + " " + a[1] + ")"
                    cur.execute(sq2)
                except:
                    try:
                        sq3 = "alter table " + createtbNew + " add " + str(a[0]) + " " + a[1] + "  "
                        cur.execute(sq3)
                    except:
                        print('ziduan have exist')
            if list1 == PRI:
                try:
                    sqlzj = 'ALTER TABLE ' + createtbNew + '  ADD PRIMARY KEY(' + str(list1) + ')'  # 添加主键
                    cur.execute(sqlzj)
                except:
                    print('PRI have exists')
            try:
                fieldAdd = "alter table " + createtbNew + " add xxrksj varchar(255)  "
                cur.execute(fieldAdd)
            except:
                print('field is exist')
    conn.select_db(dbConfigurationFile.collerrordb)
    for list1 in listdata:
        aa = str(list1)
        if bb < len(listdata) - 1:
            aa += ","
            bb += 1
        b += aa
        for cc in tableGlobal.ziduantype:
            a = cc.split(',')  # 分割字符串
            if a[0] == list1:
                try:
                    sq2 = "create table " + createtbNew + "(" + str(a[0]) + " " + a[1] + ")"
                    cur.execute(sq2)
                except:
                    try:
                        sq3 = "alter table " + createtbNew + " add " + str(a[0]) + " " + a[1] + "  "
                        cur.execute(sq3)
                    except:
                        print('ziduan have exist')
            if list1 == PRI:
                try:
                    sqlzj = 'ALTER TABLE ' + createtbNew + '  ADD PRIMARY KEY(' + str(list1) + ')'  # 添加主键
                    cur.execute(sqlzj)
                except:
                    print('PRI have exists')
            try:
                fieldAdd = "alter table " + createtbNew + " add xxrksj varchar(255)  "
                cur.execute(fieldAdd)
            except:
                print('field is exist')

    conn.commit()
    cur.close()
    return HttpResponse(json.dumps(listdata), content_type='application/json')

# API接口类
def dataApiDialog(request):
    fileType = request.GET['fileType']
    taskName = request.GET['taskName']
    belongto = request.GET['belongto']
    belongtype = request.GET['belongtype']
    urlAdress = request.GET['urlAd']
    apiMethod = request.GET['methodApi']
    needPara = request.GET['paramApi']
    readField = request.GET['fieldApi']
    apiType = request.GET['apiType']
    baseData = BaseType.objects.all()
    bt = BaseType()
    apiId = str(random.random())[2:8] + str(time.localtime()[0]) + str(time.localtime()[1]) + str(time.localtime()[2]) + str(time.localtime()[3]) + str(time.localtime()[4]) + str(time.localtime()[5])  # 任务id由6位随机数和时间串组成
    while 1:
        i = 0
        for b in baseData:
            if b.taskid == apiId:
                i = 1
        if i == 1:
            apiId = int(apiId) + random.random()[2:3]
            apiId = str(apiId)
        else:
            break
    bt.taskid = apiId
    bt.domid = gobal.dataid
    bt.filetype = fileType
    bt.taskname = taskName
    bt.belongto = belongto
    bt.belongtype = belongtype
    bt.taskstate='1'
    bt.save()

    apDa = ApiData()
    apDa.domid=gobal.dataid
    apDa.url = urlAdress

    apDa.byteamount = readField
    apDa.apitype = apiMethod
    apDa.filetype = apiType
    apDa.paramate = needPara
    apDa.taskid = bt.taskid
    apDa.save()
    return HttpResponse(json.dumps(fileType), content_type='application/json')

def tabs(request, type):
    dict = {'type':type}
    if type == "addTable":
        dict['allTableName'] = dataInterDialog(request)
    if type == "addField":
        dict['allField'] = tableToDialog(request)
    return render(request, 'taskType/sjyglFile.html', dict)

def insertData(runNowId):
    by = DataInterface.objects.get(id=runNowId)
    username = by.username
    pwd = by.pwd
    databasetype = by.databasetype
    databasename = by.databasename
    tablename = by.tablename
    createtbNew = tablename + runNowId
    ziduanname = by.ziduanname
    format_date = time.strftime("%Y-%m-%d %X", time.localtime())
    rt = RunTask()
    rt.taskid = runNowId
    rt.starttime = format_date
    rt.domid = gobal.dataid
    rt.save()
    r = RunTask.objects.filter(taskid=runNowId)
    runRecord = r[0].lastcollecttime
    stime = ''
    try:
        for runData in r:
            if runRecord < runData.lastcollecttime:
                stime = runData.lastcollecttime
    except:
        print('task is first time collect')

    field_name = re.sub('[\'\[\]]', '', ziduanname)

    if databasetype == 'mysql':
        conn = pymysql.connect(host=by.fwqadress, port=int(by.dkname), user=username, password=pwd, db=databasename, charset='utf8')
        cur = conn.cursor()
        table = "desc " + tablename + ""
    elif databasetype == 'oracle':
        conn = cx_Oracle.connect(username, pwd, '%s:%s/%s' % (by.fwqadress, by.dkname, databasename))
        cur = conn.cursor()
        table = "select COLUMN_NAME from user_tab_columns where table_name='" + tablename + "'"
    print(table)
    cur.execute(table)
    tableList = cur.fetchall()
    for tl in tableList:
        h = 0
        if tl[0] == 'XXRKSJ' or tl[0] == 'xxrksj':
            h = 2
            break
    j = 0
    field_list = field_name
    field_list = field_list.split(',')
    for f in field_list:
        if f == 'xxrksj' or f == 'XXRKSJ':
            j = 2
    if h == 2:
        if j == 0:
            field_name += ',XXRKSJ'
        if r[0] != []:
            read_coldata = "select " + field_name + " from " + tablename + " where xxrksj>'" + stime + "' "
            cur.execute(read_coldata)
            get_coldata_list = cur.fetchall()
        else:
            read_coldata = "select " + field_name + " from " + tablename + " "
            cur.execute(read_coldata)
            get_coldata_list = cur.fetchall()
        getMaxTime = "select max(xxrksj) xxrksj from " + tablename + " "  # 获取表中时间最大的时间
        cur.execute(getMaxTime)
        getMaxSee = cur.fetchall()
        time_max = ''
        for maxx in str(getMaxSee):  # 把最大时间进行格式处理
            if maxx != '(' and maxx != "," and maxx != ')' and maxx != "'" and maxx != "'":
                time_max += maxx
    else:
        read_coldata = "select " + field_name + " from " + tablename + " "
        cur.execute(read_coldata)
        get_coldata_list = cur.fetchall()
        field_name += ',XXRKSJ'
    conn.commit()
    cur.close()
    conn = pymysql.connect(host=dbConfigurationFile.host, port=dbConfigurationFile.port, user=dbConfigurationFile.user,
                           password=dbConfigurationFile.pwd, db=dbConfigurationFile.collectdb, charset='utf8')
    cur = conn.cursor()
    for col_data in get_coldata_list:
        fielddata_list = list(col_data)
        i = 0
        for field_data in fielddata_list:
            if field_data is None:
                fielddata_list[i] = ''
            i += 1
        if h == 2:
            try:
                all_fielddata = tuple(fielddata_list)
                ss = "INSERT INTO " + createtbNew + " (" + field_name + ") VALUES " + str(all_fielddata) + ""
                cur.execute(ss)
            except:
                print('data have exist')
        else:
            try:
                time_now = time.strftime("%Y-%m-%d %X", time.localtime())
                fielddata_list.append(time_now)
                all_fielddata = tuple(fielddata_list)
                ss = "INSERT INTO " + createtbNew + " (" + field_name + ") VALUES " + str(all_fielddata) + ""
                cur.execute(ss)
                time_max = time_now
            except:
                print('data is exist')
    time_now = time.strftime("%Y-%m-%d %X", time.localtime())
    conn.select_db(dbConfigurationFile.db)
    sql_update = 'update taskType_runtask set endtime = "' + str(time_now) + '" ,state="1" ,lastcollecttime="' + str(time_max) + '" where starttime = "' + str(format_date) + '" and taskid= "' + str(runNowId) + '"'
    cur.execute(sql_update)
    conn.commit()
    cur.close()
    conn.close()
    return HttpResponse('OK')

def apiData(task_id):
    format_date = time.strftime("%Y-%m-%d %X", time.localtime())
    run_recond = RunTask()
    run_recond.domid = gobal.dataid
    run_recond.taskid = task_id
    run_recond.starttime = format_date
    t = time.strftime('%Y-%m-%d', time.localtime())
    year = str(time.localtime()[0]) + '年'
    mon = str(time.localtime()[1]) + '月'
    day = str(time.localtime()[2]) + '日'
    try:
        savePath = os.makedirs(dbConfigurationFile.apiFileWay)
    except:
        savePath =dbConfigurationFile.apiFileWay
    commun = r""+dbConfigurationFile.apiFileWay+"" + '/' + year + '/' + mon + '/' + day
    if not os.path.exists(commun):
        os.makedirs(commun)  # 创建文件夹
    api_data = ApiData.objects.get(taskid=task_id)
    path_data = os.path.dirname(commun) + '/' + day
    tt = api_data.takname + t + '-' + api_data.apitype
    suffix = ".txt"
    datas = ''
    newFileName = path_data + '/' + tt + suffix
    if api_data.apitype == 'Get':
        url = str(api_data.url)+'/?'+api_data.paramate
        req = urllib.request.Request(url)
        fd = urllib.request.urlopen(req)
        data = fd.read(api_data.byteamount)
        datas = str(data)
    print(datas)
    f = open(newFileName, 'a')
    f.write(datas)
    f.close()
    time_now = time.strftime("%Y-%m-%d %X", time.localtime())
    run_recond.endtime = time_now
    run_recond.state = '1'
    run_recond.save()
    return HttpResponse('ok')

# 停用
def stateStop(request):
    taskid = request.GET['data']
    stateStartId=BaseType.objects.get(taskid=taskid)
    stateStartId.taskstate = 1
    stateStartId.save()
    return HttpResponse('ok')

# 启用
def stateStart(request):
    taskid = request.GET['data']
    stateStartId=BaseType.objects.get(taskid=taskid)
    stateStartId.taskstate = 0
    stateStartId.save()
    return HttpResponse('ok')

# 远程下载的立即执行
def downloadFileNow(taskid):
    downData = FileDownload.objects.get(taskid=taskid)
    user = downData.username
    ip = downData.ipinfo
    pwd = downData.pwdinfo
    downPath = downData.pathinfo
    subprocess.call("sh "+dbConfigurationFile.shellPath+" "+user+" "+ip+" "+pwd+" "+downPath+" "+dbConfigurationFile.savePath+"",shell=True)
    return taskid

# 下拉列表框
def sjyglDb(request):
    s_list = DataBase.objects.all()
    list = []
    for i in s_list:
        temp = {
            'dbid': i.type,
            'dbname': i.type,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')


def dataIncrement(request):
    s_list = DataIncrement.objects.all()
    list = []
    for i in s_list:
        temp = {
            'incrementid': i.incrementid,
            'incrementWay': i.incrementWay,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')

# 立即执行
def runNow(request):
    taskid=request.GET['data']
    runNowId=BaseType.objects.get(taskid=taskid)
    runNowType = runNowId.filetype
    runNowTask=runNowId.taskid
    if runNowType=='3':
        insertData(runNowTask)
    if runNowType=='4':
        apiData(runNowTask)
    if runNowType == '5':
        downloadFileNow(runNowTask)
    runNowId.taskstate = '0'
    runNowId.save()
    return HttpResponse('ok')


def xiugai(request):
    taskid=request.GET['data']
    runNowId = BaseType.objects.get(taskid=taskid)
    runNowId.taskstate = '2'
    runNowId.save()
    return HttpResponse(json.dumps(runNowId.taskstate), content_type='application/json')

#测试
def dataTest(request):
    databasetype = request.GET.get('databaseType')
    task_ip = request.GET.get('fwqAdress')
    task_port = request.GET.get('dkName')
    user_name = request.GET.get('userName')
    pwd = request.GET.get('pwd')
    databaseN = request.GET.get('databaseName')

    if databasetype == 'mysql':
        print('mysql')
        try:
            conn = pymysql.connect(host=task_ip, port=int(task_port), user=user_name, password=pwd, db=databaseN, charset='utf8')
        except:
            return
    elif databasetype == 'oracle':
        import cx_Oracle
        try:
            conn = cx_Oracle.connect(user_name, pwd, '%s:%s/%s' % (task_ip, task_port, databaseN))
        except:
            return
    conn.close()
    return HttpResponse(json.dumps(1), content_type='application/json')

#测试任务名称
def tasknameTest(request):
    task_name = request.GET.get('taskName')
    allTask=BaseType.objects.all()
    for a in allTask:
        if task_name==a.taskname:
            return HttpResponse(json.dumps(2), content_type='application/json')
    return HttpResponse(json.dumps(1), content_type='application/json')

#定时任务
def getData(request):
    try:
        task_id = request.GET['id']
        bt = BaseType.objects.get(taskid=task_id)
        bt.taskstate = '2'
        bt.save()
        # try:
        #     conn = pymysql.connect(host=dbConfigurationFile.host, port=dbConfigurationFile.port,user=dbConfigurationFile.user, password=dbConfigurationFile.pwd,db=dbConfigurationFile.db, charset='utf8')
        #     cur = conn.cursor()
        #
        # except:
        #     connErrorTime = time.strftime("%Y-%m-%d %X", time.localtime())
        #     rt = RunTask()
        #     rt.starttime = connErrorTime
        #     rt.taskid = task_id
        #     rt.state = 'connError 程序执行连接本机数据库出错'
        #     rt.save()
        #     os._exit(0)
        #
        # format_date = time.strftime("%Y-%m-%d %X", time.localtime())
        # sql_data = "INSERT INTO taskType_runtask (taskid,starttime,domid) VALUES  ('" + task_id + "','" + format_date + "','" + bt.domid + "')"
        # cur.execute(sql_data)
        # conninfo_list = []
        # conn.commit()
        # cur.close()
        format_date = time.strftime("%Y-%m-%d %X", time.localtime())
        try:
            RunTask.objects.create(taskid=task_id, starttime=format_date, domid=bt.domid)
        except:
            connErrorTime = time.strftime("%Y-%m-%d %X", time.localtime())
            rt = RunTask()
            rt.starttime = connErrorTime
            rt.taskid = task_id
            rt.state = 'connError 程序执行连接本机数据库出错'
            rt.save()
            os._exit(0)

        conninfo_list = DataInterface.objects.get(id=task_id)
        tableWrite = conninfo_list.tablename + task_id
        try:
            r = RunTask.objects.filter(taskid=task_id)
            runRecord = r[0].lastcollecttime
        except:
            print('get all data')
        stime = ''
        try:
            for runData in r:
                if runRecord < runData.lastcollecttime:
                    stime = runData.lastcollecttime
        except:
            print('task is first time collect')
        try:
            conn = pymysql.connect(host=conninfo_list.fwqadress, port=int(conninfo_list.dkname),user=conninfo_list.username, password=conninfo_list.pwd,db=conninfo_list.databasename, charset='utf8')
            cur = conn.cursor()
        except:
            connErrorTime = time.strftime("%Y-%m-%d %X", time.localtime())
            rt = RunTask()
            rt.starttime = connErrorTime
            rt.taskid = task_id
            rt.state = 'connError 程序执行连接远程数据库出错'
            rt.save()
            os._exit(0)
        field_name = ''
        for str_field in conninfo_list.ziduanname:
            if str_field != '[' and str_field != "'" and str_field != ']':
                field_name += str_field
        field = "desc " + conninfo_list.tablename + ""
        cur.execute(field)
        fieldList = cur.fetchall()
        for tl in fieldList:
            h = 0
            if tl[0] == 'XXRKSJ' or tl[0] == 'xxrksj':
                h = 2
                break
        j = 0
        field_list = field_name
        field_list = field_list.split(',')
        for f in field_list:
            if f == 'xxrksj' or f == 'XXRKSJ' or f == ' XXRKSJ':
                j = 2
        if h == 2:
            if j == 0:
                field_name += ',XXRKSJ'
            if stime != '':
                read_coldata = "select " + field_name + " from " + conninfo_list.tablename + " where xxrksj>'" + stime + "' "
                cur.execute(read_coldata)
                get_coldata_list = cur.fetchall()
            else:
                read_coldata = "select " + field_name + " from " + conninfo_list.tablename + " "
                cur.execute(read_coldata)
                get_coldata_list = cur.fetchall()
            getMaxTime = "select max(xxrksj) xxrksj from " + conninfo_list.tablename + " "  # 获取表中时间最大的时间
            cur.execute(getMaxTime)
            getMaxSee = cur.fetchall()
            time_max = ''
            for maxx in str(getMaxSee):  # 最大时间进行格式处理
                if maxx != '(' and maxx != "," and maxx != ')' and maxx != "'" and maxx != "'":
                    time_max += maxx
        else:
            read_coldata = "select " + field_name + " from " + conninfo_list.tablename + " "
            cur.execute(read_coldata)
            get_coldata_list = cur.fetchall()
            field_name += ',XXRKSJ'
        conn.commit()
        cur.close()
        conn = pymysql.connect(host=dbConfigurationFile.host, port=dbConfigurationFile.port,user=dbConfigurationFile.user, password=dbConfigurationFile.pwd,db=dbConfigurationFile.collectdb, charset='utf8')

        cur = conn.cursor()

        for col_data in get_coldata_list:
            fielddata_list = list(col_data)

            i = 0
            for field_data in fielddata_list:
                if field_data is None:
                    fielddata_list[i] = ''
                i += 1
            if h == 2:
                try:
                    field_name = field_name.lower()
                    all_fielddata = tuple(fielddata_list)
                    ss = "INSERT INTO " + str(tableWrite) + " (" + field_name + ") VALUES " + str(
                        all_fielddata) + ""
                    cur.execute(ss)
                except:
                    print('collect error')
            else:
                try:
                    time_now = time.strftime("%Y-%m-%d %X", time.localtime())
                    fielddata_list.append(time_now)
                    all_fielddata = tuple(fielddata_list)
                    ss = "INSERT INTO " + str(tableWrite) + " (" + field_name + ") VALUES " + str(all_fielddata) + ""
                    cur.execute(ss)
                    time_max = time_now
                except:
                    print('data has exist')
        conn.select_db(dbConfigurationFile.db)
        time_now = time.strftime("%Y-%m-%d %X", time.localtime())
        sql_update = 'update taskType_runtask set endtime = "' + str(time_now) + '" ,state="1" ,lastcollecttime="' + str(time_max) + '" where starttime = "' + str(format_date) + '" and taskid= "' + str(task_id) + '"'
        cur.execute(sql_update)
        sql_tasktime_update = 'update taskType_timetask set endtime = "' + str(time_now) + '",runstate="finished",state="1" where taskid= "' + task_id + '"'
        cur.execute(sql_tasktime_update)
        sql_runstate_update = 'update taskType_basetype set taskstate = "0" where taskid= "' + task_id + '"'
        cur.execute(sql_runstate_update)
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponse('OK')
    except:
        AccidentalTerminationTime = time.strftime("%Y-%m-%d %X", time.localtime())
        rt = RunTask()
        rt.starttime = AccidentalTerminationTime
        rt.taskid = task_id
        rt.state = 'terminationError 程序意外中止'
        rt.save()
        os._exit(0)


