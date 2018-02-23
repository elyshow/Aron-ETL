from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
# Create your views here.
import huafeng.settings as huafeng_settings
from .models import *
from django.db.models import Max
from django.db import connections
from codeStandard.models import DataType, RecognInfo
from django.http import JsonResponse, HttpResponse
import logging
import codecs
import json
import datetime
from subprocess import Popen, PIPE
import re
import time
import pymysql
import cx_Oracle
import petl
import socket
import os
import csv
import random
from huafeng.celery import *
from huafeng import functions as func
from . import tasks

import xlrd
import uuid
# Get an instance of a logger
logger=logging.getLogger('sourceDns.webdns.views')


# 采集节点首页
def collectNodeIndex(request):
    return render(request, 'dataCollect/collectNodeIndex.html')


# 获取采集节点列表数据
def getCollectNodeListData(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    collectTasks = CollectTask.objects.all()
    collectNodes = CollectNode.objects.all()[start:end]
    for num in range(len(collectNodes)):
        i = 0
        k = 0
        j = 0
        for td in collectTasks:
            if td.collectNodeId == collectNodes[num].id:
                if td.flag == True:
                    i += 1
                if td.flag == False:
                    k += 1
                if td.taskStatus == 1:
                    j += 1
        all_state = '启用' + str(i) + " " + '停用' + str(k) + " " + '正在采集' + str(j)
        cn = CollectNode.objects.get(id=collectNodes[num].id)
        cn.collectNodeStatus = all_state
        cn.save()
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = CollectNode.objects.filter(collectNodeName__icontains=request.POST.get('condition')).count()
        data = CollectNode.objects.filter(collectNodeName__icontains=request.POST.get('condition'))[start:end]
    else:
        counts = CollectNode.objects.all().count()
        data = CollectNode.objects.all()[start:end]
    list = []

    for num in range(len(data)):
        temp = {
            'id': data[num].id,
            'collectNodeName': data[num].collectNodeName,
            'collectNodeRegion': data[num].collectNodeRegion,
            'collectNodeStatus': data[num].collectNodeStatus,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


# 增加或修改采集节点
def saveCollectNode(request):
    postData = request.POST
    # 首先创建models对象，遍历其字段，如果post数据中有与其字段名相同的值，则直接赋值，下一步再确认其他值
    collectNode = CollectNode()
    fields = collectNode._meta.get_all_field_names()

    for field in fields:
        setattr(collectNode, field, postData.get(field))

    if collectNode.id == '':
        collectNode.id = None

    try:
        collectNode.save()
    except:
        return JsonResponse({
            'errorCode': '0x0001',
            'errorString': '数据库操作失败, 请检查采集节点名称是否重复！'
        })
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': '操作成功'
    })


# 删除采集节点
def delCollectNode(request):
    ids = request.POST.get('data')
    try:
        CollectNode.objects.extra(where=['id in (' + ids + ')']).delete()
        CollectTask.objects.extra(where=['collectNodeId in ('+ ids +')']).delete()
    except:
        return JsonResponse({
            'errorCode': '0x0001',
            'errorString': '删除失败'
        })
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': '删除成功'
    })


# 采集任务首页
def collectTaskIndex(request, collectNodeId):
    try:
        collectNode = CollectNode.objects.get(id=collectNodeId)
        collectNodeName = collectNode.collectNodeName
        return render(request, 'dataCollect/collectTaskIndex.html', {'collectNodeId': collectNodeId, 'collectNodeName': collectNodeName})
    except:
        print('节点不存在')
        return redirect(reverse('dataCollect.views.collectNodeIndex', args=[]))


# 获取采集任务列表
def getCollectTaskListData(request):
    collectNodeId = request.POST.get('collectNodeId')
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    counts = CollectTask.objects.filter(collectNodeId=collectNodeId).count()
    collectTasks = CollectTask.objects.filter(collectNodeId=collectNodeId)[start:end]
    fields = CollectTask._meta.get_all_field_names()
    list = []

    for num in range(len(collectTasks)):
        temp = {}
        for t in range(len(fields)):
            temp[fields[t]] = getattr(collectTasks[num], fields[t])
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


# 增加或修改采集任务
def saveCollectTask(request):
    postData = request.POST

    collectTask = CollectTask()
    fields = collectTask._meta.get_all_field_names()
    for field in fields:
        if field == 'createTime' or field == 'editTime':
            continue
        if field in postData:
            print(field)
            setattr(collectTask, field, postData.get(field))
        else:
            setattr(collectTask, field, '')
    collectTask.flag = 0
    collectTask.taskStatus = 0
    print('done1')
    if collectTask.id == '':
        collectTask.id = None
    if collectTask.databaseType == 'sqlserver':
        import pymssql
        con = pymssql.connect(server = collectTask.databaseHostName + ":" + collectTask.databasePort,
                                     user = collectTask.databaseUserName,
                                     password = collectTask.databasePassword,
                                     database=collectTask.databaseName)
        cur = con.cursor()
        cur.execute('''
                select s.[name] from sys.tables as t join sys.schemas as s on t.schema_id = s.schema_id where t.[name] = '%s'
                ''' % collectTask.databaseTableName)
        row = cur.fetchone()
        con.close()
        databaseCollectSQL = collectTask.databaseCollectSQL
        databaseCollectSQL = ' '.join(databaseCollectSQL.split())
        listsql = list(databaseCollectSQL)
        listsql[-len(collectTask.databaseTableName)-1] = " " + row[0] + "."
        collectTask.databaseCollectSQL = ''.join(listsql)
    # 存储数据库类型时，需要填充所选字段
    if int(postData.get('taskType')) == 2:
        allFieldsStr = re.search(r'SELECT([\s\S]*)FROM', collectTask.databaseCollectSQL).groups()[0]
        allFieldsStr = re.sub('[\s+\r\n\"]', '', allFieldsStr)
        collectTask.databaseFields = allFieldsStr
    elif int(postData.get('taskType')) == 1:
        collectTask.collectWay = 1

    # 频率设定页面内容
    timeDict = dict()
    timeType = postData.get('timeType')

    if timeType == '1':
        cycleType = postData.get('cycle')

        if cycleType == '1':
            timeDict['day_of_month'] = int(postData.get('days').strip('\''))
            timeDict['month_of_year'] = '*'
            timeDict['day_of_week'] = '*'
        elif cycleType == '2':
            timeDict['day_of_month'] = '*'
            timeDict['month_of_year'] = '*'
            # timeDict['day_of_week'] = list(map(int, postData.getlist('week_day')))
            timeDict['day_of_week'] = ','.join(postData.getlist('week_day'))
        elif cycleType == '3':
            timeDict['day_of_month'] = '*'
            timeDict['month_of_year'] = '*'
            timeDict['day_of_week'] = '*'

        timeDict['hour'] = int(postData.get('hours').strip('\''))
        timeDict['minute'] = int(postData.get('minutes').strip('\''))

    elif timeType == '2':
        timeStr = postData.get('once_time')

        timeTuple = time.strptime(timeStr, '%Y-%m-%d %H:%M')
        timeDict = {
            'minute': timeTuple[4],
            'hour': timeTuple[3],
            'day_of_month': timeTuple[2],
            'month_of_year': timeTuple[1],
            'day_of_week': '*',
            'year': timeTuple[0]
        }
    elif timeType == '3':
        pass
    elif timeType == '4':
        postMinute = postData.get('minutes').strip('\'')
        timeDict['minute'] = '*' if postMinute == '0' else '*/' + postMinute

        postHour = postData.get('hours').strip('\'')
        timeDict['hour'] = '*' if postHour == '0' else '*/' + postHour

        postDM = postData.get('intervalDay').strip('\'')
        timeDict['day_of_month'] = '*' if postDM == '0' else '*/' + postDM

        timeDict['month_of_year'] = '*'
        timeDict['day_of_week'] = '*'

    timeStr = json.dumps(timeDict)
    if postData.get('fieldSplitCode', '') == 'other':
        collectTask.fieldSplitCode = postData.get('otherSplitCcode')
    collectTask.timeStr = timeStr
    print(timeStr)
    try:
        collectTask.save()
        # 增加新建采集表的表名
        newTableName = collectTask.databaseTableName.upper() + '_' + str(collectTask.id)
        if '.' in newTableName:
            newTableName = newTableName.split('.')[1]
            if len(newTableName) >30:
                newTableName = newTableName[-30:]
        else:
            newTableName = newTableName[-30:]
        collectTask.newCollectCreateTableName = newTableName
        collectTask.save()

        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': '操作成功'
        })
    except:
        return JsonResponse({
            'errorCode': '0x0001',
            'errorString': '操作失败'
        })


# 删除采集任务
def delCollectTask(request):
    ids = request.POST.get('data')
    try:
        CollectTask.objects.extra(where=['id in (' + ids + ')']).delete()
    except:
        return JsonResponse({
            'errorCode': '0x0001',
            'errorString': '删除失败'
        })
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': '删除成功'
    })


def endisableCollectTask(request):
    '''
    启用禁用
    '''
    id = request.POST.get('data')
    try:
        collectTask = CollectTask.objects.get(id=id)
        collectTask.flag = 1 if collectTask.flag == 0 else 0

        if collectTask.flag == 1:
            # 启用任务
            enableCollectTaskById(id)
        else:
            # 禁用任务
            disableCollectTaskById(id)

        collectTask.save()
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': '操作成功'
        })
    except:
        return JsonResponse({
            'errorCode': '0x0001',
            'errorString': '操作失败'
        })


def enableCollectTaskById(id):
    """
    启用任务
    :param id: 任务ID
    :return:
    """
    collectTask = CollectTask.objects.get(id=id)
    # 创建celery task
    if int(collectTask.timeType) != 3:
        timeDict = json.loads(collectTask.timeStr)
        try:
            del(timeDict['year'])
        except:
            pass
        create_task(collectTask.taskName + '_' + str(id), "dataCollect.tasks.celeryRunCollectTaskById", {"taskId": collectTask.id}, timeDict)


def disableCollectTaskById(id):
    """
    禁用任务
    :param id: 任务ID
    :return:
    """
    collectTask = CollectTask.objects.get(id=id)
    # 停用celery task
    disable_task(collectTask.taskName + '_' + str(id))


# 获取所属机构
def getBelongInstitution(request):
    s_list = RecognInfo.objects.all()
    list = []
    for i in s_list:
        temp = {
            'recognid': i.recognname,
            'recognname': i.recognname,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')


# 获取所属类型
def getBelongType(request):
    s_list = DataType.objects.all()
    list = []
    for i in s_list:
        temp = {
            'dataid': i.dataname,
            'dataname': i.dataname,
        }
        list.append(temp)
    return HttpResponse(json.dumps(list), content_type='application/json')


# 接收前台页面请求运行采集任务
def runCollectTask(request):
    taskId = request.POST.get('data')

    collectTask = CollectTask.objects.get(id=taskId)

    if collectTask.taskStatus == 1:
        return JsonResponse({
            'errorCode': '0x0002',
            'errorString': '任务运行中'
        })
    print('taskId is %s' % taskId)
    # delay调用task
    tasks.celeryRunCollectTaskById.delay(taskId)

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': '任务开始运行'
    })


class CursorPorxy(object):
    def __init__(self, cursor):
        self._cursor = cursor

    def executemany(self, statement, parameters, **kwargs):
        print(statement)
        # fixme 此处循环遍历，将clob等转成str。效率比较低，可以考虑只对clob类型进行转换
        listp = []
        for parameter in parameters:
            listv = []
            for v in parameter:
                try:
                    strv = v.read()
                except:
                    strv = v
                listv.append(strv)
            listp.append(listv)
        return self._cursor.executemany(statement, listp, **kwargs)

    def __getattr__(self, item):
        return getattr(self._cursor, item)


def splitNum(totalNum, stepNum):
    """
    根据步长切分总长
    :param totalNum:总长度
    :param stepNum: 步长
    :return: 切分后的元组数组，相当于每一页的起始和终点
    """

    if totalNum <= stepNum:
        return [(1, totalNum)]

    pageCount = totalNum // stepNum
    leftCount = totalNum % stepNum

    splitList = []
    for i in range(pageCount):
        splitList.append((i * stepNum + 1, (i + 1) * stepNum))

    if leftCount:
        splitList.append((pageCount * stepNum + 1, totalNum))

    return splitList


def runCollectTaskById(taskId):
    """
    根据ID参数运行采集任务
    :param taskId: 采集任务ID
    :return:
    """

    collectTask = CollectTask.objects.get(id=taskId)
    if collectTask.taskStatus == 1:
        return JsonResponse({
            'errorCode': '0x0002',
            'errorString': '任务运行中'
        })


    collectTaskLog = CollectTaskLog()
    collectTaskLog.taskId = collectTask.id
    collectTaskLog.taskName = collectTask.taskName
    collectTaskLog.taskStatus = 1
    collectTaskLog.save()

    # 采集任务标志
    collectTask.taskStatus = 1
    # fixme   调试关闭正在执行状态
    collectTask.save()
    collectDatabaseName = huafeng_settings.COLLECTDB
    collectAppName = 'collectApp'

    newCollectCreateTableName = collectTask.newCollectCreateTableName

    connection = getDataBaseConnection(collectTask)

    collectDatabaseConnection = connections[collectDatabaseName]
    collectDatabaseEngine = huafeng_settings.DATABASES[collectDatabaseName].get('ENGINE')

    # 查询当前表里数据量
    # dsn = '%s:%s/%s' % (huafeng_settings.DATABASES[collectDatabaseName].get('HOST'),
    #                     huafeng_settings.DATABASES[collectDatabaseName].get('PORT') or '1521',
    #                     huafeng_settings.DATABASES[collectDatabaseName].get('NAME'))
    # collectDatabaseConnection = cx_Oracle.connect(user=huafeng_settings.DATABASES[collectDatabaseName].get('USER'),
    #                                   password=huafeng_settings.DATABASES[collectDatabaseName].get('PASSWORD'), dsn=dsn)
    # collectTask = CollectTask.objects.get(id=taskId)
    # countSql = 'SELECT COUNT(*) FROM %s ' % collectTask.databaseTableName.upper()
    # cur = collectDatabaseConnection.cursor()
    # cur.execute(countSql)
    # nowCount = cur.fetchall()[0][0]
    # cur.close()
    # collectTaskLog.nowCount = nowCount
    # collectTaskLog.save()

    if collectDatabaseEngine.endswith('mysql'):
        sql = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s' ;" % (
            collectDatabaseName, newCollectCreateTableName)
    elif collectDatabaseEngine.endswith('oracle'):
        sql = "select TABLE_NAME from user_tables where TABLE_NAME = '%s'" % (newCollectCreateTableName)
    else:
        return JsonResponse({
            'errorCode': '0x0003',
            'errorString': '任务失败'
        })

    collectDatabaseCursor = collectDatabaseConnection.cursor()
    collectDatabaseCursor.execute(sql)
    result = collectDatabaseCursor.fetchone()
    collectDatabaseCursor.close()


    # 文件方式采集
    if collectTask.taskType == 1:
        fileFields = json.loads(collectTask.fileFields)
        fields = []
        eleFieldMap = {}
        textField = []
        for field in fileFields:
            if field['fieldName'] == '':
                continue
            if isinstance(field['fieldLength'], str):
                field['fieldLength'] = int(field['fieldLength'].strip("'").strip('"'))
            temp = {
                'column_name': field['fieldName'],
                'data_length': field['fieldLength'],
                'iskey': 0 if field['preKey'] == 'NO' else 1,
                'comments': field['fieldChineseName'],
                'data_type': field['fieldType'],
                'nullable':'Y',
            }
            textField.append(field['fieldName'])
            eleFieldMap[field['elementName']] = field['fieldName']
            fields.append(temp)
        if not result:
            classModel, createSQL = creatTable(newCollectCreateTableName, fields, collectDatabaseName,
                                               collectAppName)

            cur = collectDatabaseConnection.cursor()
            # 执行建表语句

            for oneSQL in createSQL:
                if oneSQL:
                    cur.execute(oneSQL[0:-1])
            # 添加中文字段名
            for field in fields:
                if collectDatabaseEngine.endswith('mysql'):
                    sql = "select COLUMN_TYPE from information_schema.columns where table_schema ='%s' and table_name = '%s' and column_name='%s'; " % (
                        collectDatabaseName, newCollectCreateTableName, field['column_name'])
                    cur.execute(sql)
                    columnType = cur.fetchone()[0]
                    sql = "ALTER table %s MODIFY COLUMN `%s` %s COMMENT '%s'" % (
                        newCollectCreateTableName, field['column_name'], columnType, field['comments'])
                elif collectDatabaseEngine.endswith('oracle'):
                    sql = "COMMENT ON COLUMN %s.%s IS '%s'" % (
                        newCollectCreateTableName, field['column_name'], field['comments'])

                cur.execute(sql)
            cur.close()
        fileRoot = collectTask.fileRoot
        filePath = collectTask.filePath
        fileFields = collectTask.fileFields
        ip, port, filePath = analysisPath(filePath)
        username = collectTask.username
        passwd = collectTask.password
        FTP.port = port
        try:
            ftp = FTP(ip, user=username, passwd=passwd, timeout=3)
        except:
            return JsonResponse({
                'errorCode': '0x0010',
                'errorString': 'ftp服务器连接失败'
            })
        print(fileRoot, filePath, fileFields)
        if username == '':
            ftp.login()
        if filePath != '':
            ftp.cwd(filePath)
        fileList = getFileList(ftp, fileType= collectTask.fileType)
        listArray = []
        allCount = 0
        successCount = 0
        try:
            if collectDatabaseEngine.endswith('mysql'):
                cur = collectDatabaseConnection.cursor()
                cur.execute('SET SQL_MODE=ANSI_QUOTES')
            if collectDatabaseEngine.endswith('oracle'):

                # fixme 此处如果使用django自带连接会出错，有空可以再深入研究一次
                dsn = '%s:%s/%s' % (huafeng_settings.DATABASES[collectDatabaseName].get('HOST'),
                                    huafeng_settings.DATABASES[collectDatabaseName].get('PORT') or '1521',
                                    huafeng_settings.DATABASES[collectDatabaseName].get('NAME'))
                collectDatabaseConnection = cx_Oracle.connect(
                    user=huafeng_settings.DATABASES[collectDatabaseName].get('USER'),
                    password=huafeng_settings.DATABASES[collectDatabaseName].get('PASSWORD'), dsn=dsn)
                def get_cursor():
                    return CursorPorxy(petlCur)

                #cur = get_cursor
            #print(cur)
            # print(22222222)
            # print(ftp.pwd())
            # ftp.sendcmd('DELE "%s"' %(xmlList.__next__()))
            # print(ftp.pwd())
            # print(11111111111111)
            # return
            for l in fileList:
                petlCur = collectDatabaseConnection.cursor()
                cur = get_cursor
                # print(l)
                rootPath, fileName = downLoadFile(ftp, l)
                if collectTask.fileType == 'xml':
                    table = petl.xml.fromxml(fileName, collectTask.rowField, eleFieldMap)
                elif collectTask.fileType == 'csv':
                    table = petl.fromcsv(fileName, encoding='utf-8')
                    table = petl.rename(table, eleFieldMap)
                elif collectTask.fileType == 'txt':
                    limitCode = collectTask.fieldLimitCode
                    splitCode = codecs.decode( collectTask.fieldSplitCode, 'unicode_escape')
                    reg = limitCode + '(.*)' + limitCode
                    for i in range(len(textField) - 1):
                        reg += splitCode + limitCode + '(.*)' + limitCode
                    reg += '$'
                    os.system('sed -i 1d %s' % fileName)
                    table = petl.fromtext(fileName, encoding='utf-8')
                    table = table.capture('lines', reg, textField)
                elif collectTask.fileType == 'xlsx':
                    table = petl.fromxlsx(fileName)
                    table = petl.rename(table, eleFieldMap)
                #print(fileName)
                #print('aaaaaaaaaa')
                #print(table)
                #print(collectTask.fileType, (table.len() - 1))
                #return
                try:
                    petl.appenddb(table, cur, newCollectCreateTableName)

                    if collectDatabaseEngine.endswith('oracle'):
                        successCount += petlCur.rowcount
                except:
                    collectTask.taskStatus = 0
                    collectTask.save()
                    collectTaskLog.taskStatus = 2
                    collectTaskLog.save()
                    return JsonResponse({
                        'errorCode': '0x0004',
                        'errorString': '任务出错'
                    })

                if collectTask.fileType == 'xml' or collectTask.fileType == 'xlsx':
                    allCount += table.len() - 1
                elif collectTask.fileType == 'csv':
                    allCount += table.len() - 1
                elif  collectTask.fileType == 'txt':
                    allCount += table.len() - 2
                if os.path.exists(fileName):
                    os.remove(fileName)
            collectTaskLog.successCount = successCount
            collectTaskLog.collectNodeId = collectTask.collectNodeId
            collectTaskLog.taskStatus = 0
            collectTaskLog.allCount = allCount
            collectTaskLog.save()
            collectTask.taskStatus = 0
            collectTask.save()
            #if os.path.exists(huafeng_settings.DOWNLOAD_PATH + '/' + filePath):
                #os.system('rm -rf %s' % huafeng_settings.DOWNLOAD_PATH + '/' + filePath)
        except:
            return JsonResponse({
                'errorCode': '0x0011',
                'errorString': '文件下载失败'
            })

    # 数据库方式采集
    elif collectTask.taskType == 2:

        # 数据表不存在，需要创建
        fields = getTableFields(collectTask.databaseTableName, collectTask)
        prkID = False
        key = 0
        blobList = {}
        blobList['BLOB'] = []
        blobFlag = False
        for field in fields:
            if field['iskey']:
                if field['column_name'] == 'ID' or field['column_name'] == 'id':
                    prkID = True
            if field['data_type'].upper() == 'BLOB':
                blobList['BLOB'].append(key)
                blobFlag = True
            key += 1
        if not result:
            classModel, createSQL = creatTable(newCollectCreateTableName, fields, collectDatabaseName,
                                               collectAppName)
            print(createSQL)
            cur = collectDatabaseConnection.cursor()
            # 执行建表语句
            databaseFields = collectTask.databaseFields.split(',')
            for oneSQL in createSQL:
                if oneSQL:
                    if (not prkID) and oneSQL.startswith('CREATE TABLE') and ('ID' in databaseFields or 'id' in databaseFields):
                        oneSQL = re.sub('"(ID|id).*(KEY|key),\n', '', oneSQL)
                    try:
                        cur.execute(oneSQL[0:-1])
                    except Exception as e:
                        print(e)
                        return JsonResponse({
                            'errorCode': '0x0012',
                            'errorString': '建表失败'
                        })
            # 添加中文字段名
            for field in fields:
                if collectDatabaseEngine.endswith('mysql'):
                    sql = "select COLUMN_TYPE from information_schema.columns where table_schema ='%s' and table_name = '%s' and column_name='%s'; " % (
                        collectDatabaseName, newCollectCreateTableName, field['column_name'])
                    cur.execute(sql)
                    columnType = cur.fetchone()[0]
                    sql = "ALTER table %s MODIFY COLUMN `%s` %s COMMENT '%s'" % (
                        newCollectCreateTableName, field['column_name'], columnType, field['comments'] if field['comments'] is not None else '')
                elif collectDatabaseEngine.endswith('oracle'):
                    sql = "COMMENT ON COLUMN %s.%s IS '%s'" % (
                        newCollectCreateTableName, field['column_name'], field['comments'] if field['comments'] is not None else '')
                try:
                    cur.execute(sql)
                except Exception as e:
                    print(e)
                    return JsonResponse({
                        'errorCode': '0x0011',
                        'errorString': '修改注释失败'
                    })
            cur.close()
            print('建表完成')

        # 组装原始SQL语句
        sql = collectTask.databaseCollectSQL
        countSql = 'SELECT COUNT(*) FROM %s ' % collectTask.databaseTableName.upper()
        if collectTask.databaseType == 'sqlserver':
            import pymssql
            con = pymssql.connect(server = collectTask.databaseHostName + ":" + collectTask.databasePort,
                                         user = collectTask.databaseUserName,
                                         password = collectTask.databasePassword,
                                         database=collectTask.databaseName)
            cur = con.cursor()
            cur.execute('''
                    select s.[name] from sys.tables as t join sys.schemas as s on t.schema_id = s.schema_id where t.[name] = '%s'
                    ''' % collectTask.databaseTableName)
            row = cur.fetchone()
            con.close()
            tablename = row[0] + '.' + collectTask.databaseTableName
            countSql = 'SELECT COUNT(*) FROM %s ' % tablename

        # 如果为增量采集
        print('采集方式', collectTask.collectWay)
        whereSql = ' where 1=1 '
        if collectTask.collectWay:
            if not collectTask.databaseIncrementField:
                return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '增量字段为空'
                })
            maxContent = CollectTaskLog.objects.filter(taskId=collectTask.id).aggregate(Max('incrementContent'))[
                'incrementContent__max']
            print(maxContent)
            if maxContent:
                if collectTask.databaseType == 'mysql':
                    whereSql += " and `%s` > '%s' " % (collectTask.databaseIncrementField, maxContent)

                elif collectTask.databaseType == 'oracle':
                    try:
                        time.strptime(maxContent, "%Y-%m-%d %H:%M:%S")
                        whereSql += ' and "%s" > "TO_DATE"(\'%s\', \'yyyy-mm-dd hh24:mi:ss\') ' % (
                            collectTask.databaseIncrementField, maxContent)
                    except:
                        whereSql += ' and "%s" > %s ' % (collectTask.databaseIncrementField, maxContent)

                sql += whereSql
                countSql += whereSql
        else:
            cur = collectDatabaseConnection.cursor()
            try:
                cur.execute('TRUNCATE TABLE "%s"' % newCollectCreateTableName)
            except:
                return JsonResponse({
                    'errorCode': '0x0004',
                    'errorString': '增量字段为空'
                })
            cur.close()

        print(sql, countSql)
        # 获取需要采集的总行数
        try:
            cur = connection.cursor()
            cur.execute(countSql)
        except Exception as e:
            print(e)
            return JsonResponse({
                'errorCode': '0x0013',
                'errorString': '查询总条数失败'
            })
        collectTaskLog.allCount = cur.fetchall()[0][0]
        collectTaskLog.collectNodeId = collectTask.collectNodeId
        cur.close()

        # FROM_DB_SETTINGS = {
        #     'ENGINE': collectTask.databaseType,
        #     'NAME': collectTask.databaseName,
        #     'USER': collectTask.databaseUserName,
        #     'PASSWORD': collectTask.databasePassword,
        #     'HOST': collectTask.databaseHostName,
        #     'PORT': collectTask.databasePort,
        # }
        # TO_DB_SETTINGS = {
        #     'ENGINE': huafeng_settings.DATABASES[collectDatabaseName]['ENGINE'],
        #     'NAME': huafeng_settings.DATABASES[collectDatabaseName]['NAME'],
        #     'USER': huafeng_settings.DATABASES[collectDatabaseName]['USER'],
        #     'PASSWORD': huafeng_settings.DATABASES[collectDatabaseName]['PASSWORD'],
        #     'HOST': huafeng_settings.DATABASES[collectDatabaseName]['HOST'],
        #     'PORT': huafeng_settings.DATABASES[collectDatabaseName]['PORT'],
        # }
        #
        #
        #
        # collectMaster.initMaster(FROM_DB_SETTINGS, TO_DB_SETTINGS, newCollectCreateTableName, sql, collectMasterPort)


        # 生成Master参数脚本
        # 1.生成参数文件（参数包括来源数据库配置， 缓存库配置， 缓存表名称等）
        TIME_APPENDIX = str(time.time())
        collectMasterFileName = 'collectMaster%s.py' % TIME_APPENDIX
        collectMasterFilePath = os.path.join(huafeng_settings.COLLECT_CLEAN_TEMP_DIR, collectMasterFileName)
        while os.path.exists(collectMasterFilePath):
            time.sleep(0.1)
            TIME_APPENDIX = str(time.time())
            collectMasterFileName = 'collectMaster%s.py' % TIME_APPENDIX
            collectMasterFilePath = os.path.join(huafeng_settings.COLLECT_CLEAN_TEMP_DIR, collectMasterFileName)

        # 获取空闲端口
        collectMasterPort = func.getAvaliablePort()

        with open(collectMasterFilePath, 'w') as collectMasterFile:
            # 写入初始文件
            collectMasterFile.write(open(os.path.join(huafeng_settings.BASE_DIR, 'collectMaster.py')).read())

            FROM_DB_SETTINGS = {
                'ENGINE': collectTask.databaseType,
                'NAME': collectTask.databaseName,
                'USER': collectTask.databaseUserName,
                'PASSWORD': collectTask.databasePassword,
                'HOST': collectTask.databaseHostName,
                'PORT': collectTask.databasePort,
            }
            TO_DB_SETTINGS = {
                'ENGINE': huafeng_settings.DATABASES[collectDatabaseName]['ENGINE'],
                'NAME': huafeng_settings.DATABASES[collectDatabaseName]['NAME'],
                'USER': huafeng_settings.DATABASES[collectDatabaseName]['USER'],
                'PASSWORD': huafeng_settings.DATABASES[collectDatabaseName]['PASSWORD'],
                'HOST': huafeng_settings.DATABASES[collectDatabaseName]['HOST'],
                'PORT': huafeng_settings.DATABASES[collectDatabaseName]['PORT'],
            }
            # 写入数据库配置
            if blobFlag:
                collectMasterFile.write('BIG_FIELD =' + json.dumps(blobList) + '\n')
            collectMasterFile.write('FROM_DB_SETTINGS = ' + json.dumps(FROM_DB_SETTINGS) + '\n')
            collectMasterFile.write('TO_DB_SETTINGS = ' + json.dumps(TO_DB_SETTINGS) + '\n')
            # 写入缓存表名称
            collectMasterFile.write('TO_TABLE_NAME = "' + newCollectCreateTableName + '"\n')

            # 写入SQL语句
            collectMasterFile.write('LINE = """' + sql + '"""\n')

            # 写入PORT
            collectMasterFile.write('PORT = ' + str(collectMasterPort) + '\n')

            # 写入调用
            if blobFlag:
                collectMasterFile.write('BIG_FIELD =' + json.dumps(blobList) + '\n')
                collectMasterFile.write('initMaster(FROM_DB_SETTINGS, TO_DB_SETTINGS, TO_TABLE_NAME, LINE, PORT, BIG_FIELD)')
            else:
                collectMasterFile.write('initMaster(FROM_DB_SETTINGS, TO_DB_SETTINGS, TO_TABLE_NAME, LINE, PORT)')

        print('generate %s' % collectMasterFilePath)

        pMaster = Popen("%s %s" % (huafeng_settings.PYTHON3_PATH,collectMasterFilePath), shell=True,
              stdout=PIPE, stderr=PIPE)
        print("%s %s" % (huafeng_settings.PYTHON3_PATH,collectMasterFilePath))
        # # 2.生成SQL分片列表
        # # 生成分片元组数组
        # splitList = splitNum(collectTaskLog.allCount, 50000)
        # sqlListFilePath = os.path.join(huafeng_settings.COLLECT_CLEAN_TEMP_DIR, 'sqllist%s.txt' % TIME_APPENDIX)
        # originSQL = re.sub('[\r\n]', ' ', sql)
        #
        # with open(sqlListFilePath, 'w') as f:
        #     for one in splitList:
        #         if collectDatabaseEngine.endswith('mysql'):
        #             oneSQL = "%s LIMIE %s, %s \n" % (originSQL, one[0]-1, 50000)
        #         elif collectDatabaseEngine.endswith('oracle'):
        #             oneSQL = "select %s from (select A.*, ROWNUM RN FROM %s A %s and ROWNUM <= %s) WHERE RN >= %s \n" % (collectTask.databaseFields, collectTask.databaseTableName, whereSql, one[1], one[0])
        #         f.write(oneSQL)
        # # 3. 结果文件夹
        # hdfsResultDir = 'collectResult%s' % TIME_APPENDIX
        # # 4. python3 的路径
        # PYTHON3_PATH = '/usr/local/python3/bin/python3'
        #
        # # 需要使用hadoop用户执行此命令
        # cmd = 'su hadoop -c "python3 %s -r hadoop %s -o %s --python-bin=%s" ' % (collectMasterFilePath, sqlListFilePath, hdfsResultDir, PYTHON3_PATH)
        # print('cmd', cmd)
        # os.system(cmd)

        # 开启节点采集任务
        MyIP = huafeng_settings.MASTER_HOST
        print('MyIP is %s' % MyIP)
        collectNodePList = []
        for ip in huafeng_settings.COLLECT_NODE:
            p1 = Popen("scp %s root@%s:~/" % (os.path.join(huafeng_settings.BASE_DIR, 'collectSlave.py'), ip), shell=True,
                       stdout=PIPE, stderr=PIPE)
            p1.wait()
            if p1.returncode == 0:
                print("ssh root@%s '%s %s %s %s'" % (ip, huafeng_settings.PYTHON3_PATH, 'collectSlave.py', MyIP, collectMasterPort))
                p2 = Popen("ssh root@%s '%s %s %s %s'" % (ip, huafeng_settings.PYTHON3_PATH, 'collectSlave.py', MyIP, collectMasterPort),
                           shell=True, stdout=PIPE, stderr=PIPE)
                collectNodePList.append(p2)
            else:
                print('error in scp')
        successCount = 0
        # 等待采集任务完成
        for collectNodeP in collectNodePList:
            while collectNodeP.poll() == None:
                time.sleep(3)
            collectNodePOut = collectNodeP.stdout.readlines()
            print(collectTask.taskName, collectNodePOut)
            try:
                collectNodePSuccessCount = collectNodePOut[-1].decode('utf-8').strip('\n').split(' ')[-1]
                print(collectTask.taskName,collectNodePSuccessCount)
            except Exception as e:
                print(e)
                collectNodePSuccessCount = 0
            successCount += int(collectNodePSuccessCount)

        # if collectDatabaseEngine.endswith('mysql'):
        #     fromTable = petl.fromdb(connection, sql)
        #     print(fromTable)
        #     cur = collectDatabaseConnection.cursor()
        #     cur.execute('SET SQL_MODE=ANSI_QUOTES')
        #     petl.appenddb(fromTable, cur, newCollectCreateTableName)
        #     cur.close()
        # elif collectDatabaseEngine.endswith('oracle'):
        #     fromTable = petl.fromdb(connection, sql)
        #     print(fromTable)
        #
        #     # fixme 此处如果使用django自带连接会出错，有空可以再深入研究一次
        #     dsn = '%s:%s/%s' % (huafeng_settings.DATABASES[collectDatabaseName].get('HOST'),
        #                         huafeng_settings.DATABASES[collectDatabaseName].get('PORT') or '1521',
        #                         huafeng_settings.DATABASES[collectDatabaseName].get('NAME'))
        #     collectDatabaseConnection = cx_Oracle.connect(
        #         user=huafeng_settings.DATABASES[collectDatabaseName].get('USER'),
        #         password=huafeng_settings.DATABASES[collectDatabaseName].get('PASSWORD'), dsn=dsn)
        #     petlCur = collectDatabaseConnection.cursor()
        #
        #     def get_cursor():
        #         return CursorPorxy(petlCur)
        #
        #     print(collectDatabaseConnection, newCollectCreateTableName)
        #     print(fromTable)
        #
        #     try:
        #         # fixme 字段名大小写可能会有问题
        #         # fixme 此处考虑可能需要用django的save方法替换，不然就只有insert，无法更新
        #
        #         petl.appenddb(fromTable, get_cursor, newCollectCreateTableName)
        #         # 成功条数处理
        #         collectTaskLog.successCount = petlCur.rowcount
        #         collectTaskLog.taskStatus = 0
        #     except:
        #
        #         collectTask.taskStatus = 0
        #         collectTask.save()
        #         collectTaskLog.taskStatus = 2
        #         collectTaskLog.save()
        #         return JsonResponse({
        #             'errorCode': '0x0004',
        #             'errorString': '任务出错'
        #         })

        # 如果有设置增量字段，则需要更新日志中的增量字段值
        if collectTask.databaseIncrementField:
            print('begin find max')
            c = collectDatabaseConnection.cursor()
            c.execute('SELECT MAX(%s) FROM %s' % (collectTask.databaseIncrementField, newCollectCreateTableName))
            res = c.fetchall()
            print(res)
            # 存入日志
            collectTaskLog.incrementContent = res[0][0]
            c.close()
        collectTaskLog.successCount = successCount
        collectTaskLog.taskStatus = 0
        collectTaskLog.endTime = time.strftime('%F %T', time.localtime())
        collectTaskLog.save()
        collectDatabaseConnection.close()
        print('end')
        collectTask.taskStatus = 0
        collectTask.save()

    elif collectTask.taskType == 3:
        pass


# 根据参数获取数据库连接
def getDataBaseConnection(dbsettings):
    if dbsettings.databaseType == 'mysql':
        connection = pymysql.connect(host=dbsettings.databaseHostName,
                                     user=dbsettings.databaseUserName,
                                     password=dbsettings.databasePassword,
                                     database=dbsettings.databaseName,
                                     port=int(dbsettings.databasePort),
                                     charset='utf8',)
    elif dbsettings.databaseType == 'oracle':
        dsn = '%s:%s/%s' % (dbsettings.databaseHostName, dbsettings.databasePort, dbsettings.databaseName)
        connection = cx_Oracle.connect(user=dbsettings.databaseUserName, password=dbsettings.databasePassword, dsn=dsn)
    elif dbsettings.databaseType == 'sqlserver':
        import pymssql
        connection = pymssql.connect(server=dbsettings.databaseHostName + ":" + dbsettings.databasePort,
                                     user=dbsettings.databaseUserName,
                                     password=dbsettings.databasePassword,
                                     database=dbsettings.databaseName)
    else:
        connection = None
    return connection


def getTableFields(tableName, dbsettings):
    '''
    获取表结构
    '''
    fields = []
    needFileds = dbsettings.databaseFields.split(',')
    print(needFileds)
    if dbsettings.databaseType == 'mysql':
        connection = pymysql.connect(host=dbsettings.databaseHostName,
                                     user=dbsettings.databaseUserName,
                                     password=dbsettings.databasePassword,
                                     database=dbsettings.databaseName,
                                     port=int(dbsettings.databasePort),
                                     charset='utf8',)
        cur = connection.cursor()
        getFieldsSQL = "show full columns from %s ;" % tableName
        cur.execute(getFieldsSQL)
        fieldsInfo = cur.fetchall()
        for fieldInfo in fieldsInfo:
            if not fieldInfo[0] in needFileds:
                continue
            temp = {
                'column_name': fieldInfo[0],
                'nullable': 'Y' if fieldInfo[3] == 'YES' else 'NO',
                'comments': fieldInfo[8],
                'iskey': 1 if fieldInfo[4] == 'PRI' else 0,
            }
            fullType = fieldInfo[1]
            fullTypeSplit = re.findall(r'(\w+)\((\d+)\)', fullType)
            if fullTypeSplit:
                temp['data_type'] = fullTypeSplit[0][0]
                temp['data_length'] = int(fullTypeSplit[0][1])
            else:
                temp['data_type'] = fullType
                temp['data_length'] = 0
            fields.append(temp)
        cur.close()
        connection.close()
    elif dbsettings.databaseType == 'oracle':
        print('oracle')
        dsn = '%s:%s/%s' % (dbsettings.databaseHostName, dbsettings.databasePort, dbsettings.databaseName)
        connection = cx_Oracle.connect(user=dbsettings.databaseUserName, password=dbsettings.databasePassword, dsn=dsn)
        print(dsn)
        print(connection)
        cur = connection.cursor()
        tableName = tableName.upper()
        if '.' in tableName:
            owner = tableName.split('.')[0]
            tableName = tableName.split('.')[1]
        else:
            owner = dbsettings.databaseUserName
        # 第一步获取所有字段信息
        getFieldsSQL = '''
        select t.column_name,t.data_type,t.data_length,t.nullable,t.column_id,t.DATA_PRECISION,t.DATA_SCALE,c.comments,(select 0 from DUAL) iskey
           FROM all_tab_cols t, all_col_comments c
           WHERE upper(t.table_name)='%s'
                 and c.table_name=t.table_name
                 and c.column_name=t.column_name
                 and t.hidden_column='NO'
                 and t.owner='%s'
        order by t.column_id
        ''' % (tableName, owner)
        print(getFieldsSQL)
        firstcur = cur.execute(getFieldsSQL)
        fieldsInfo = firstcur.fetchall()
        for fieldInfo in fieldsInfo:
            print(fieldInfo[0])
            if not fieldInfo[0] in needFileds:
                continue
            if len(fieldInfo[0].encode('utf-8')) > 30:
                fieldInfo = list(fieldInfo)
                fieldInfo[0] = fieldInfo[0][0:10]
            temp = dict(zip(['column_name', 'data_type', 'data_length', 'nullable', 'column_id','data_precision','data_scale', 'comments', 'iskey'], fieldInfo))
            fields.append(temp)
        print('first step', fields)
        # 第二步获取主键
        getPrimarySQL = '''
        SELECT
            M .column_name
        FROM
            all_constraints s,
            all_cons_columns M
        WHERE
            UPPER (M .table_name) = '%s'
        AND M .table_name = s.table_name
        AND M .constraint_name = s.constraint_name
        AND s.constraint_type = 'P'
        and M.owner = '%s'
        ''' % (tableName,owner)

        secondcur = cur.execute(getPrimarySQL)
        primaryKey = secondcur.fetchall()
        try:
            #primaryKey = primaryKey[0][0]
            if len(primaryKey):
                for key in primaryKey:
                    for field in fields:
                        if field['column_name'] == key[0]:
                            print(key[0])
                            field['iskey'] = 1
                            break
            print('primarykey', primaryKey)
            print('second step', fields)
        except:
            pass
        cur.close()
        connection.close()

    elif dbsettings.databaseType == 'sqlserver':
        import pymssql
        connection = pymssql.connect(server = dbsettings.databaseHostName + ":" + dbsettings.databasePort,
                                     user = dbsettings.databaseUserName,
                                     password = dbsettings.databasePassword,
                                     database = dbsettings.databaseName)
        cur = connection.cursor()
        cur.execute('''
                        select s.[name] from sys.tables as t join sys.schemas as s on t.schema_id = s.schema_id where t.[name] = '%s'
                        ''' % dbsettings.databaseTableName)
        row = cur.fetchone()
        #第一步获取column_name  数据类型  数据长度 是否空键
        cur.execute('''SELECT syscolumns.name,systypes.name,syscolumns.isnullable,syscolumns.length
            FROM syscolumns, systypes
            WHERE syscolumns.xusertype = systypes.xusertype
            AND syscolumns.id = object_id('%s.%s')''' % (row[0], dbsettings.databaseTableName))
        res = cur.fetchall()
        print(res)
        logger.error(needFileds)
        logger.error(res)
        fields = []
        for reone in res:
            if not reone[0] in needFileds:
                continue
            temp = {
                'column_name': reone[0],
                'nullable': 'Y' if reone[2] == '1' else 'NO',
                'data_type': reone[1],
                'data_length': reone[3],
                'iskey': 0,
            }
            fields.append(temp)
        print(fields)
        #第二步获取字段说明
        cur.execute('''SELECT t.[name] AS 表名,c.[name] AS 字段名,cast(ep.[value]
            as varchar(100)) AS [字段说明]
            FROM sys.tables AS t
            INNER JOIN sys.columns
            AS c ON t.object_id = c.object_id
            LEFT JOIN sys.extended_properties AS ep
            ON ep.major_id = c.object_id AND ep.minor_id = c.column_id WHERE ep.class =1
            AND t.name= '%s' ''' % dbsettings.databaseTableName)
        ress = cur.fetchall()
        for (reone,field) in zip(ress,fields):
            field.update({'comments': reone[2]})
        logger.error(fields)
        #第三步获取主键
        getPrimarySQL = '''SELECT syscolumns.name
            FROM syscolumns,sysobjects,sysindexes,sysindexkeys
            WHERE syscolumns.id = object_id('%s.%s') AND sysobjects.xtype = 'PK'
            AND sysobjects.parent_obj = syscolumns.id
            AND sysindexes.id = syscolumns.id
            AND sysobjects.name = sysindexes.name AND sysindexkeys.id = syscolumns.id
            AND sysindexkeys.indid = sysindexes.indid
            AND syscolumns.colid = sysindexkeys.colid''' % (row[0], dbsettings.databaseTableName)

        cur.execute(getPrimarySQL)
        for row in cur:
            pass
        try:
            primaryKey = row[0]
            if primaryKey:
                for field in fields:
                    if field['column_name'] == primaryKey:
                        field['iskey'] = 1
            print('primarykey', primaryKey)
            print('3 step', fields)
        except:
            pass
        cur.close()
        connection.close()
    else:
        pass
    return fields

'''
动态创建model
'''

BIGINTEGER_FIELD = ['BIGINT', 'DECIMAL', 'NUMERIC', 'MONEY', 'REAL']
BINARY_FIELD = ['BLOB', 'BINARY', 'TINYBLOB', 'UNIQUEIDENTIFIER', 'IMAGE', 'VARBINARY', 'BIT', ]
CHAR_FIELD = ['CHAR', 'VARCHAR', 'NVARCHAR', 'VARCHAR2', 'NVARCHAR2', 'NVARCHAR', 'NCHAR', ]
DATETIME_FIELD = ['DATETIME', 'DATE', 'DATETIME2', 'DATETIMEOFFSET', 'SMALLDATETIME', 'TIMESTAMP', 'TIME', ]
FLOAT_FIELD = ['FLOAT', ]
INTEGER_FIELD = ['SMALLINT', 'INT', 'INTEGER', 'TINYINT', 'SMALLMONEY', '']
TEXT_FIELD = ['TEXT', 'CLOB', 'NCLOB', 'LONGTEXT', 'NTEXT', 'GEOGRAPHY', 'GEOMETRY', ]
DECIMAL_FIELD = ['NUMBER', 'DECIMAL', ]


def creatTable(tableName, fields, db, app_label=''):
    tableName = tableName.upper()

    class Meta:
        db_table = tableName
    setattr(Meta, 'app_label', app_label)
    list = []
    for field in fields:
        if field['iskey'] == 1:
            list.append(field['column_name'])
    hasSetPriKey = False
    #print(22222222222222222, list)
    if len(list) > 1:
        setattr(Meta, 'unique_together', tuple(list))
        hasSetPriKey = True
    attr = {'__module__': app_label + '.models', 'Meta': Meta}
    if len(list) > 1:
        attr['primary'] = tuple(list)
    for field in fields:
        if field['data_type'].upper() in BIGINTEGER_FIELD:
            attr[field['column_name']] = models.BigIntegerField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in BINARY_FIELD:
            attr[field['column_name']] = models.BinaryField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in CHAR_FIELD:
            if field['data_length'] <= 2000:
                attr[field['column_name']] = models.CharField(max_length=(field['data_length'] if field['data_length'] else 255),
                                                            null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
            else:
                attr[field['column_name']] = models.TextField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in DATETIME_FIELD:
            attr[field['column_name']] = models.DateTimeField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in FLOAT_FIELD:
            attr[field['column_name']] = models.FloatField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in INTEGER_FIELD:
            attr[field['column_name']] = models.IntegerField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in TEXT_FIELD:
            attr[field['column_name']] = models.TextField(null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
        elif field['data_type'].upper() in DECIMAL_FIELD:
            attr[field['column_name']] = models.DecimalField(max_length=field['data_length'] if field['data_length'] else 38,
                                                            null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            max_digits= field['data_precision'] if field['data_precision'] is not None else 0,
                                                            decimal_places= 0,
                                                            blank=True)
        else:
            attr[field['column_name']] = models.CharField(max_length=(field['data_length'] if field['data_length'] else 255),
                                                            null=(True if field['nullable'] == 'Y' else False),
                                                            primary_key=(True if field['iskey'] == 1 and (not hasSetPriKey)  else False),
                                                            verbose_name=field['comments'],
                                                            blank=True)
    classModel = type(tableName, (models.Model,), attr)
    from django.db import connections
    from django.db.backends.base.creation import BaseDatabaseCreation
    from django.core.management.color import no_style
    creation = BaseDatabaseCreation(connections[db])
    create_sql = creation.sql_create_model(classModel, no_style())[0]
    create_sql[0] = re.sub('(NUMBER|number)\(0.*?0\)',r'\1', create_sql[0])
    return classModel, create_sql

'''
获取post请求中数据库配置内容
'''
def getDBSettingFromRequest(request):
    class DBSetting():
        pass
    try:
        dbsetting = DBSetting()
        dbsetting.databaseType = request.POST.get('databaseType')
        dbsetting.databaseHostName = request.POST.get('databaseHostName')
        dbsetting.databaseName = request.POST.get('databaseName')
        dbsetting.dataTableSpace = request.POST.get('dataTableSpace')
        dbsetting.indexTableSpace = request.POST.get('indexTableSpace')
        dbsetting.databasePort = request.POST.get('databasePort')
        dbsetting.databaseUserName = request.POST.get('databaseUserName')
        dbsetting.databasePassword = request.POST.get('databasePassword')
        return dbsetting
    except:
        return JsonResponse({
            'errorCode': '0x0001',
            'errorString': '参数不完整'
        })

'''
根据参数测试数据库连接
'''
def testDataBaseConnect(request):
    dbsetting = getDBSettingFromRequest(request)
    if isinstance(dbsetting, JsonResponse):
        return dbsetting
    try:
        con = getDataBaseConnection(dbsettings=dbsetting)
        con.close()
    except:
        return JsonResponse({
            'errorCode': '0x0002',
            'errorString': '连接失败'
        })

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': '连接成功'
    })


'''
根据参数获取数据库中所有表
'''
def getDataBaseTables(request):
    dbsetting = getDBSettingFromRequest(request)
    if isinstance(dbsetting, JsonResponse):
        return dbsetting
    allTableName = []
    try:
        conn = getDataBaseConnection(dbsettings=dbsetting)
        if dbsetting.databaseType == 'mysql':
            tableNameSQL = "show tables;"
        elif dbsetting.databaseType == 'oracle':
            tableNameSQL = "SELECT table_name FROM user_tables"
        elif dbsetting.databaseType == 'sqlserver':
            tableNameSQL = "SELECT Name FROM SysObjects Where XType='U' ORDER BY Name"

        cur = conn.cursor()
        cur.execute(tableNameSQL)

        tableList = cur.fetchall()
        tableCount = len(tableList)
        for index in range(tableCount):
            temp = {
                'value': tableList[index][0],
                'text': tableList[index][0]
            }
            allTableName.append(temp)
        cur.close()
        conn.close()
    except Exception as e:
        print('获取库中表出错')
    finally:
        return HttpResponse(json.dumps(allTableName), content_type="application/json")


'''
根据参数获取选择所有字段的SQL语句
'''
def getSelectAllSQL(request):
    dbsetting = getDBSettingFromRequest(request)
    if isinstance(dbsetting, JsonResponse):
        return dbsetting
    databaseTableName = request.POST.get('databaseTableName')
    selectAllSQL = ''
    try:
        conn = getDataBaseConnection(dbsettings=dbsetting)
        cur = conn.cursor()
        if dbsetting.databaseType == 'mysql':
            fieldNameSQL = "desc " + databaseTableName + ""
        elif dbsetting.databaseType == 'oracle':
            if '.' in databaseTableName:
                fieldNameSQL = "select COLUMN_NAME from all_tab_columns where table_name='" + databaseTableName.split('.')[1].upper() + "' and owner='" + databaseTableName.split('.')[0].upper()+ "' ORDER BY COLUMN_ID"
                databaseTableName = databaseTableName.upper()
            else:
                fieldNameSQL = "select COLUMN_NAME from user_tab_columns where table_name='" + databaseTableName + "'" + " ORDER BY COLUMN_ID"
                databaseTableName = '"' + databaseTableName + '"' if re.search(r'[a-z]', databaseTableName) else databaseTableName
        elif dbsetting.databaseType == 'sqlserver':
            cur.execute('''
                select s.[name] from sys.tables as t join sys.schemas as s on t.schema_id = s.schema_id where t.[name] = '%s'
                ''' % databaseTableName)
            row = cur.fetchone()
            fieldNameSQL = "Select Name FROM SysColumns Where id=Object_Id('%s.%s')" % (row[0], databaseTableName)

        cur.execute(fieldNameSQL)
        allFields = cur.fetchall()
        cur.close()
        conn.close()

        # 如果是mysql，字段大小写都行；如果是oracle，如果字段名有小写，需要加引号
        if dbsetting.databaseType == 'mysql':
            fieldList = [x[0] for x in allFields]
        elif dbsetting.databaseType == 'oracle':
            fieldList = list(map(lambda x: '"' + x[0] + '"' if re.search(r'[a-z]', x[0]) else x[0], allFields))
        elif dbsetting.databaseType == 'sqlserver':
            fieldList = [x[0] for x in allFields]
        fieldStr = '\n' + '\n,'.join(fieldList) + '\n'
        selectAllSQL = 'SELECT ' + fieldStr + ' FROM %s' % databaseTableName

    except Exception as e:
        print('获取表中字段出错')
    finally:
        return HttpResponse(selectAllSQL)

'''
获取预览数据
'''
def getPreviewData(request):
    dbsetting = getDBSettingFromRequest(request)
    if isinstance(dbsetting, JsonResponse):
        return dbsetting
    databaseTableName = request.POST.get('databaseTableName')
    databaseCollectSQL = request.POST.get('databaseCollectSQL')
    databasePreviewNum = request.POST.get('databasePreviewNum')
    fieldStr = request.POST.get('fieldStr')
    fieldList = fieldStr.split(',')

    # 增加预览条数限制
    if dbsetting.databaseType == 'mysql':
        querySQL = databaseCollectSQL + ' LIMIT 0, %s' % databasePreviewNum
    elif dbsetting.databaseType == 'oracle':
        querySQL = databaseCollectSQL + ' where rownum<=%s' % databasePreviewNum
    elif dbsetting.databaseType == 'sqlserver':
        con = getDataBaseConnection(dbsettings=dbsetting)
        cur = con.cursor()
        cur.execute('''
                select s.[name] from sys.tables as t join sys.schemas as s on t.schema_id = s.schema_id where t.[name] = '%s'
                ''' % databaseTableName)
        row = cur.fetchone()
        con.close()
        databaseCollectSQL = ' '.join(databaseCollectSQL.split())
        listsql = list(databaseCollectSQL)
        databasePreviewNum = " TOP " + databasePreviewNum + " "
        listsql[6] = databasePreviewNum
        listsql[-len(databaseTableName)-1] = " " + row[0] + "."
        querySQL = ''.join(listsql)
    import collections
    try:
        con = getDataBaseConnection(dbsettings=dbsetting)
        cur = con.cursor()
        cur.execute(querySQL)
        print(querySQL)
        allres = cur.fetchall()

        resData = []

        # 遍历循环，如果查询的结果是LOB对象，则将其转换为str对象，这样才能进行json转换
        for oneres in allres:
            oneresTrans = []
            for one in oneres:

                if isinstance(one, cx_Oracle.LOB):
                    oneTrans = one.__str__()
                elif isinstance(one, datetime.datetime):
                    oneTrans = one.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(one, datetime.date):
                    oneTrans = one.strftime('%Y-%m-%d')
                elif isinstance(one, uuid.UUID):
                    oneTrans = one.__str__()
                else:
                    oneTrans = one
                oneresTrans.append(oneTrans)

            d = collections.OrderedDict()
            for i in range(len(fieldList)):
                d[fieldList[i]] = oneresTrans[i]
            resData.append(d)
            # resData.append(dict(zip(fieldList, oneresTrans)))
        return HttpResponse(json.dumps(resData, ensure_ascii=False), content_type='application/json')
    except:
        return JsonResponse({
            'errorCode': '0x0002',
            'errorString': '查询出错'
        })


'''
获取所有采集任务及其表名称
'''
def getCollectTable(request):
    collectTasks = CollectTask.objects.all()
    comboData = []
    for collectTask in collectTasks:
        temp = {
            'value': collectTask.newCollectCreateTableName,
            'text': collectTask.taskName
        }
        comboData.append(temp)
    return HttpResponse(json.dumps(comboData), content_type='application/json')

def analysisPath(path):
    pathList = path.split(':')
    filePath = ''
    ip = ''
    try:
        index = pathList[2].find('/')
        if index != -1:
            port = int(pathList[2][:index])
            filePath = pathList[2][index:]
        else:
            port = int(pathList[2])
            # port = pathList[2]
    except:
        port = 21
    index = pathList[1][2:].find('/')
    if index != -1:
        ip = pathList[1][2:][:index]
        filePath = pathList[1][2:][index:]
    else:
        ip = pathList[1][2:]
    #print(pathList[1][2:], port, filePath)
    return ip, port, filePath

'''
    测试ftp或者http是否可用
'''

from ftplib import FTP,error_perm
from socket import error,gaierror
def testServer(request):
    ftp = FTP()
    path = request.POST.get('filePath')
    serverType = path[:path.find(':')].lower()
    serverList = ['ftp', 'http']
    if not serverType in serverList:
        return JsonResponse({
            'errorCode': '0x0003',
            'errorString': '服务器地址不正确'
        })
    ip, port, filePath = analysisPath(path)
    username = request.POST.get('username')
    passwd = request.POST.get('password')
    try:
        if serverType == 'ftp':
            ftp.connect(ip, port, timeout=3)
    except(error, gaierror):
        return JsonResponse({
            'errorCode':'0x0001',
            'errorString':'服务器连接失败'
        })
    try:
        if serverType == 'ftp':
            ftp.login(username, passwd)
    except error_perm:
        if serverType == 'ftp':
            ftp.quit()
        return JsonResponse({
            'errorCode': '0x0002',
            'errorString': '用户名或密码错误'
        })
    if filePath != '':
        try:
            if serverType == 'ftp':
                ftp.cwd(filePath)
        except error_perm:
            if serverType == 'ftp':
                ftp.quit()
            return JsonResponse({
                'errorCode': '0x0003',
                'errorString': '目录不存在'
            })
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': 'ftp服务可用'
    })

'''
获取根节点combobox的值
'''
def getRootElement(request):
    path = request.POST.get('filePath', '')
    if path == '':
        return HttpResponse(json.dumps([]), content_type='application/json')
    ip, port, filePath = analysisPath(path)
    username = request.POST.get('username')
    passwd = request.POST.get('password')
    FTP.port = port
    print(ip, port, username, passwd)
    ftp = FTP(ip,  user = username, passwd=passwd, timeout=3)
    if username == '':
        ftp.login()
    root = getRoot(ftp, filePath=filePath, fileType=request.POST.get('fileType'))
    dictList = []
    if not 'fileRoot' in request.POST:
        path = '/' + root.tag
        list = [path]
        dictList = [{'value':root.tag, 'text':path}]
        result = getXmlElements(root, path)
        for path in result:
            if path not in list:
                list.append(path)
                temp = {
                    'value': path[path.rfind('/')+1:],
                    'text': path
                }
                dictList.append(temp)
    else:
        if request.POST.get('fileRoot') == '':
            return HttpResponse(json.dumps(dictList), content_type='application/json')
        list = []
        if root.tag == request.POST.get('fileRoot'):
            ele = getXmlElements(root)
            for tag in ele:
                if tag not in list:
                    list.append(tag)
                    temp = {
                        'value': tag[tag.rfind('/') + 1:],
                        'text':  request.POST.get('rootPath') + tag
                    }
                    dictList.append(temp)
        else:
            root = root.iterfind(request.POST.get('fileRoot'))

            for rp in root:
                result = getXmlElements(rp)
                for tag in result:
                    print(tag)
                    if tag not in list:
                        list.append(tag)
                        temp = {
                            'value': tag[tag.rfind('/') + 1:],
                            'text':  request.POST.get('rootPath') + tag
                        }
                        dictList.append(temp)
    return HttpResponse(json.dumps(dictList), content_type='application/json')

def  getRoot(ftp, filePath = '', fileType = ''):
    """
    获取xml根节点
    :param ftp: ftp连接
    :param filePath: 文件所在根目录
    :param fileType: 获取文件类型
    :return: 根节点对象
    """
    if filePath != '':
        ftp.cwd(filePath)
    xmlList = getFileList(ftp,fileType=fileType)
    file = xmlList.__next__()
    rootPath, fileName = downLoadFile(ftp, file)
    from lxml import etree
    tree = etree.ElementTree(file=fileName)
    root = tree.getroot()
    return root


'''
获取要采集的节点列表
'''
def getDataGridList(request):
    if not len(request.POST):
        return JsonResponse({'total': 0, 'rows': []})
    fileType = request.POST.get('fileType')
    if fileType == 'xml':
        if request.POST.get('rootPath'):
            path = request.POST.get('rootPath')
        else:
            return JsonResponse({'total': 0, 'rows': []})
    ip, port, filePath = analysisPath(request.POST.get('filePath'))
    username = request.POST.get('username')
    passwd = request.POST.get('password')
    FTP.port = port

    ftp = FTP(ip, user=username, passwd=passwd, timeout=3)
    if username == '':
        ftp.login()
    if fileType == 'xml':
        root = getRoot(ftp, filePath, fileType=fileType)
        list = []
        if path.split('/')[-1] == root.tag:
            ele = getXmlElements(root, isGrid= True)
            for tag in ele:
                list.append(tag)
        else:
            root = root.iterfind(path)
            for rp in root:
                ele = getXmlElements(rp, isGrid=True)
                for tag in ele:
                    list.append(tag)
        list = set(list)
    elif fileType == 'csv' or fileType == 'txt':
        if filePath != '':
            ftp.cwd(filePath)
        fileList = getFileList(ftp,dir = filePath + '/', fileType= fileType)
        file = fileList.__next__()
        rootPath, fileName = downLoadFile(ftp, file)
        csvFile = open(fileName, 'r', encoding='utf-8')
        line = csvFile.readline().strip('\n')
        if request.POST.get('fieldLimitCode') != 'no' or request.POST.get('fieldLimitCode') != '':
            line = line.replace(str(request.POST.get('fieldLimitCode')), '')
        if fileType != 'csv' :
            if request.POST.get('fieldSplitCode', '') == 'other':
                fieldSplitCode = request.POST.get('otherSplitCode')
            else:
                fieldSplitCode = request.POST.get('fieldSplitCode')
        else:
            fieldSplitCode = ','
        list = line.split(codecs.decode( fieldSplitCode, 'unicode_escape'))
    elif fileType == 'xls' or fileType == 'xlsx':
        if filePath != '':
            ftp.cwd(filePath)
        fileList = getFileList(ftp, dir=filePath + '/', fileType=fileType)
        file = fileList.__next__()
        rootPath, fileName = downLoadFile(ftp, file)

        xldwork = xlrd.open_workbook(fileName)

        tab = xldwork.sheets()[0]

        list = tab.row_values(0)
    result = []
    for l in list:
        temp = {
            'fieldName':l,
            'elementName':l,
            'fieldChineseName':'',
            'fieldType':'VARCHAR2',
            'fieldLength':255,
            'preKey':'NO',
        }
        result.append(temp)
    return JsonResponse({'total':len(list), 'rows':result})

'''
递归遍历xml的dict数据,得到根节点的下拉值
'''
def getXmlElements(element, path = '', isGrid = False):
    all = element.iterfind('./')
    for ele in all:
        if isGrid:
            yield ele.tag
            list = getXmlElements(ele, isGrid=isGrid)
        else:
            yield path + '/' + ele.tag
            list = getXmlElements(ele, path=path + '/' + ele.tag)
        for e in list:
            yield e


'''
将服务器上的xml文件下载到本地目录，以便读取内容
'''

def downLoadFile(ftp, file):
    baseName = os.path.basename(file)
    dirName = os.path.dirname(file)
    getSize = ftp.sendcmd('size ' + baseName)
    size = getSize.split(' ')[1]
    rootPath = huafeng_settings.DOWNLOAD_PATH + dirName.split('/')[0]
    localPath = huafeng_settings.DOWNLOAD_PATH +  dirName
    if not os.path.exists(localPath):
        os.makedirs(localPath, 0o755)
    fileName = localPath + '/' + baseName
    fileHandler = open(fileName, 'wb')
    ftp.retrbinary("RETR %s" %( baseName ), fileHandler.write, blocksize=int(size))
    fileHandler.close()
    return rootPath,fileName


def getCollectTaskLog(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if request.POST.get('id') != '':
        count = CollectTaskLog.objects.filter(taskId = request.POST.get('id')).count()
        getData = CollectTaskLog.objects.filter(taskId = request.POST.get('id')).order_by('-startTime')[start:end]
    elif request.POST.get('ids') != '':
        count = CollectTaskLog.objects.extra(where=['taskId in (' + request.POST.get('ids') + ')']).count()
        getData = CollectTaskLog.objects.extra(where=['taskId in (' + request.POST.get('ids') + ')']).order_by('-startTime')[start:end]
    else:
        count = CollectTaskLog.objects.filter(collectNodeId= request.POST.get('nodeId')).count()
        getData = CollectTaskLog.objects.filter(collectNodeId=request.POST.get('nodeId')).order_by('-startTime')[start:end]
    fields = CollectTaskLog._meta.get_all_field_names()
    list = []

    for num in range(len(getData)):
        temp = {}
        for t in range(len(fields)):
                temp[fields[t]] = func.dataToString(getattr(getData[num], fields[t]))
        list.append(temp)
    return JsonResponse({'total':count, 'rows':list}, content_type='application/json')

'''
    获取ftp目录下的所有文件
'''
def getFileList(ftp, lists = None,  dir = '',fileType = ''):
    if lists is None:
        lists = []
    list = ftp.nlst()
    if len(list):
        for file in list:
            try:
                dir = ftp.pwd() + '/'
                ftp.cwd(file)
                for path in getFileList(ftp, lists, dir, fileType = fileType):
                    yield path
                ftp.cwd(dir)
            except:
                if os.path.splitext(file)[1] == '.' +fileType:
                    yield dir + file


# 进度条

def getProgressBar(request):
    """
    根据ID参数获取进度条
    """

    #获取采集数据总量
    # allCount = collectTaskLog.allCount
    # #连接数据库
    # try:
    #     dsn = '%s:%s/%s' % (huafeng_settings.DATABASES[collectDatabaseName].get('HOST'),
    #                         huafeng_settings.DATABASES[collectDatabaseName].get('PORT') or '1521',
    #                         huafeng_settings.DATABASES[collectDatabaseName].get('NAME'))
    #     collectDatabaseConnection = cx_Oracle.connect(
    #         user=huafeng_settings.DATABASES[collectDatabaseName].get('USER'),
    #         password=huafeng_settings.DATABASES[collectDatabaseName].get('PASSWORD'), dsn=dsn)
    #     cur = collectDatabaseConnection.cursor()
    # except:
    #     return JsonResponse({
    #         'errorCode': '0x0010',
    #         'errorString': '数据库连接失败'
    #         })
    # #组装原生SQL语句
    # collectTask = CollectTask.objects.get(id=request.POST.get('id'))
    # countSql = 'SELECT COUNT(*) FROM %s ' % collectTask.databaseTableName.upper()
    # #获取当前采集数量
    # cur.execute(countSql)
    # nowCount1 = cur.fetchall()[0][0]
    # cur.close()
    # taskProgress ='%.2f' % (int(nowCount1)-int(collectTaskLog.nowCount))*100/(int(allCount)-int(collectTaskLog.nowCount))
    id = request.POST.get('ids')
    temp = {
        'ids': id,
        'taskProgress': 20
        }
    return HttpResponse(json.dumps(temp), content_type='application/json')