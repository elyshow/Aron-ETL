import huafeng.settings as huafeng_settings
from django.apps import apps
import json
from django.http import Http404, HttpResponseRedirect, JsonResponse, HttpResponse
from .models import *
from dataCleaningRules.models import *
from releaseRegisterManagement.models import MasterdataTable,FieldTable
from standardApp.models import  *
from collectApp.models import *
from codeStandard.models import StandardDataInfo
from django.shortcuts import render, render_to_response, redirect
from django.conf import settings
from django.db import connection
from django.db.models import Max
from . import tasks
from huafeng.celery import *
from huafeng import functions as func
import os
import csv
import time
import re
import pymysql
from subprocess import Popen, PIPE
import socket


class CleanSite(object):
    def __init__(self, name='dataCleaning'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name

    def hasPermission(self, request):
        return True

    def get_urls(self):
        from django.conf.urls import url, include

        urlpatterns = [
            url(r'^$', self.index, name='index'),
            url(r'^getList/$', self.getList, name='getList'),
            url(r'^enable/$', self.enable, name='enable'),
            url(r'^disable/$', self.disable, name='disable'),
            url(r'^start/$', self.start, name='start'),
            url(r'^delete/$', self.delete, name='delete'),
            url(r'^save/$', self.save, name='save'),
            url(r'^receiveCleanResult/$', self.receiveCleanResult, name='receiveCleanResult'),
            url(r'^getFieldsByTable/$', self.getFieldsByTable, name='getFieldsByTable'),
            url(r'^getStandardTable/$', self.getStandardTable, name='getStandardTable'),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'dataCleaning', self.name

    def index(self, request):
        collectdb = huafeng_settings.COLLECTDB
        standarddb = huafeng_settings.STANDARDDB

        return render(request, 'dataCleaning/index.html', {'collectdb': collectdb, 'standarddb': standarddb})

    def getList(self, request):

        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = CleanWork.objects.filter(name=request.POST.get('condition')).count()
            data = CleanWork.objects.filter(name=request.POST.get('condition'))[start:end]
        else:
            counts = CleanWork.objects.all().count()
            data = CleanWork.objects.all()[start:end]

        fields = CleanWork._meta.get_all_field_names()

        list = []
        for num in range(len(data)):
            temp = {}
            for t in range(len(fields)):
                temp[fields[t]] = getattr(data[num], fields[t])
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def list(self, request):
        lists = CleanWork.objects.all()
        return HttpResponse(lists)

    def enable(self, request):
        """
        启用任务
        :param id: 任务ID
        :return:
        """
        workid = request.POST.get('id')

        try:
            cleanWork = CleanWork.objects.get(id=workid)
        except:
            print('get work error!')
            return JsonResponse({
                'errorCode': 1,
                'errorString': 'get cleanwork error!'
            })
        # 创建celery task
        try:
            cleanWork.flag = True
            cleanWork.save()

            timeDict = json.loads(cleanWork.timeStr)
            try:
                del (timeDict['year'])
            except:
                pass

            create_task(cleanWork.name + '_' + str(workid), "dataCleaning.tasks.celeryRunCleanTaskById",
                        {"taskId": cleanWork.id}, timeDict)
        except:
            return JsonResponse({
                'errorCode': 2,
                'errorString': '启用失败'
            })

        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': '启用成功'
        })


    @staticmethod
    def getDBSettings(db):
        return {
            'ENGINE': huafeng_settings.DATABASES[db].get('ENGINE', 'mysql'),
            'HOST': huafeng_settings.DATABASES[db].get('HOST', 'localhost'),
            'PORT': huafeng_settings.DATABASES[db].get('PORT', '3306'),
            'USER': huafeng_settings.DATABASES[db].get('USER', 'root'),
            'PASSWORD': huafeng_settings.DATABASES[db].get('PASSWORD', '123456'),
            'NAME': huafeng_settings.DATABASES[db].get('NAME', 'collectdb'),
        }

    @staticmethod
    def getDBType(db):
        engine = huafeng_settings.DATABASES[db].get('ENGINE', 'mysql')
        return engine.split('.')[-1]

    @staticmethod
    def getConnection(db):
        DBType = CleanSite.getDBType(db)
        DBSetting = CleanSite.getDBSettings(db)
        import cx_Oracle
        if DBType == 'mysql':
            conn = pymysql.connect(**DBSetting)
        elif DBType == 'oracle':
            conn = cx_Oracle.connect(DBSetting['USER'], DBSetting['PASSWORD'],'%s:%s/%s' % (DBSetting['HOST'], DBSetting['PORT'], DBSetting['NAME']))
        return conn, DBType

    def disable(self, request):
        """
        禁用任务
        :param id: 任务ID
        :return:
        """
        workid = request.POST.get('id')
        try:
            cleanWork = CleanWork.objects.get(id=workid)
        except:
            print('get work error!')
            return JsonResponse({
                'errorCode': 1,
                'errorString': 'get cleanwork error!'
            })
        try:
            # 停用celery task
            cleanWork.flag = False
            cleanWork.save()
            disable_task(cleanWork.name + '_' + str(workid))
        except:
            return JsonResponse({
                'errorCode': 2,
                'errorString': '禁用失败'
            })

        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': '禁用成功'
        })

    def start(self, request):
        workid = request.POST.get('id')
        cleanWork = CleanWork.objects.get(id=workid)

        if cleanWork.status == 1:
            return JsonResponse({
                'errorCode': '1',
                'errorString': "执行中"
            })

        tasks.celeryRunCleanTaskById.delay(workid)

        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': "任务开始执行"
        })

    @staticmethod
    def runCleanTaskById(taskId):
        cleanWork = CleanWork.objects.get(id=taskId)
        if cleanWork.status == 1:
            return JsonResponse({
                'errorCode': '1',
                'errorString': "执行中"
            })

        cleanWorkLog = CleanWorkLog()
        cleanWorkLog.workid = taskId
        cleanWorkLog.fromtable = cleanWork.fromTable
        cleanWorkLog.totable = cleanWork.toTable
        cleanWorkLog.save()

        cleanWork.status = 1
        cleanWork.save()
        fromTable = cleanWork.fromTable
        toTable = cleanWork.toTable

        # 采集表与标准表字段映射
        fromFieldAndToField = json.loads(cleanWork.fromFieldAndToField)
        # 标准表字段顺序
        toFieldList = []
        for fromField in sorted(fromFieldAndToField.keys()):
            toField = fromFieldAndToField[fromField]
            toFieldList.append(toField)

        # 1.生成清洗Master文件
        TIME_APPENDIX = str(time.time())
        cleanMasterFileName = 'cleanMaster%s.py' % TIME_APPENDIX
        cleanMasterFilePath = os.path.join(huafeng_settings.COLLECT_CLEAN_TEMP_DIR, cleanMasterFileName)
        while os.path.exists(cleanMasterFilePath):
            time.sleep(0.1)
            TIME_APPENDIX = str(time.time())
            cleanMasterFileName = 'cleanMaster%s.py' % TIME_APPENDIX
            cleanMasterFilePath = os.path.join(huafeng_settings.COLLECT_CLEAN_TEMP_DIR, cleanMasterFileName)
        cleanMaster = open(cleanMasterFilePath, 'w')
        cleanMaster.write(open(os.path.join(huafeng_settings.BASE_DIR, 'cleanMaster.py')).read())

        # 采集表字段校验规则
        cleanMaster.write('CHECK_RULE = [\n')
        fromFieldAndCheckRule = json.loads(cleanWork.fromFieldAndCheckRule)
        checkRuleList = []
        for fromField in sorted(fromFieldAndToField.keys()):
            checkRuleId = fromFieldAndCheckRule.get(fromField, '')
            if checkRuleId:
                temp = {
                    'type': CheckRule.objects.get(id=checkRuleId).type,
                    'content': CheckRule.objects.get(id=checkRuleId).content
                }
            else:
                temp = {
                    'type': 0,
                    'content': ''
                }
            if temp['type'] == 3:
                cleanMaster.write("'''" + temp['content'] + "''',\n")
            else:
                cleanMaster.write('"' + temp['content'] + '",\n')
            checkRuleList.append(temp)
        cleanMaster.write(']\n')

        # 采集表字段清洗规则(内容转换)
        cleanMaster.write('CLEAN_RULE = [\n')
        fromFieldAndCleanRule = json.loads(cleanWork.fromFieldAndCleanRule)
        cleanRuleList = []
        for fromField in sorted(fromFieldAndToField.keys()):
            cleanRuleId = fromFieldAndCleanRule.get(fromField, '')
            if cleanRuleId:
                temp = {
                    'type': CleanRule.objects.get(id=cleanRuleId).type,
                    'content': CleanRule.objects.get(id=cleanRuleId).content
                }
            else:
                temp = {
                    'type': 0,
                    'content': '{}'
                }
            if temp['type'] == 1:
                cleanMaster.write("'''" + temp['content'] + "''',\n")
            else:
                cleanMaster.write(temp['content'] + ',\n')
            cleanRuleList.append(temp)
        cleanMaster.write(']\n')

        FROM_DB_SETTINGS = CleanSite.getDBSettings(huafeng_settings.COLLECTDB)
        TO_DB_SETTINGS = CleanSite.getDBSettings(huafeng_settings.STANDARDDB)
        # 写入数据库配置
        cleanMaster.write('FROM_DB_SETTINGS = ' + json.dumps(FROM_DB_SETTINGS) + '\n')
        cleanMaster.write('TO_DB_SETTINGS = ' + json.dumps(TO_DB_SETTINGS) + '\n')
        # 写入标准名称
        cleanMaster.write('TO_TABLE_NAME = "' + toTable.upper() + '_STANDARDAPP' + '"\n')

        # 写入标准表字段顺序
        toFieldList = []
        for fromField in sorted(fromFieldAndToField.keys()):
            toField = fromFieldAndToField[fromField]
            toFieldList.append(toField)
        cleanMaster.write('TO_FIELD_LIST = ["%s"]\n' % '","'.join(toFieldList))

        # 写入SQL语句
        DBType = CleanSite.getDBType(huafeng_settings.COLLECTDB)
        joinTableFields = cleanWork.joinTableFields
        sql = "SELECT %s FROM %s where 1=1" % (",".join(sorted(fromFieldAndToField.keys())), fromTable)
        # print(",".join(fromFieldAndToField.keys()))
        # return
        if cleanWork.cleanWay == 1:
            nowMax = ''
            try:
                fromDBCon = CleanSite.getConnection(huafeng_settings.COLLECTDB)
                c = fromDBCon.cursor()
                c.execute('SELECT MAX(%s) FROM %s' % (cleanWork.databaseIncrementField, fromTable))
                res = c.fetchall()
                if res[0][0]:
                    if isinstance(res[0][0], datetime):
                        nowMax = time.strftime('%Y-%m-%d %H:%M:%S', res[0][0])
                    else:
                        nowMax = res[0][0]
                c.close()
                fromDBCon.close()
            except Exception as e:
                print('get before max error')
                print(e)

            print('nowMax', nowMax)

        if joinTableFields:
            joinFields = joinTableFields.split(',')
            for joinField in joinFields:
                sql += ' and ' + joinField
        if DBType == 'mysql':
            # 如果是增量方式1
            if cleanWork.cleanWay == 1:
                sql += " and %s <= '%s'" % (cleanWork.databaseIncrementField, nowMax)
                res = CleanWorkLog.objects.filter(workid=taskId).filter(status=0).aggregate(Max('incrementContent'))
                if res.get('incrementContent__max'):
                    lastMaxContent = res.get('incrementContent__max')
                    sql += " and %s > '%s'" % (cleanWork.databaseIncrementField, lastMaxContent)
        elif DBType == 'oracle':
            if cleanWork.cleanWay == 1:
                try:
                    # 如果是时间字符串
                    time.strptime(nowMax, "%Y-%m-%d %H:%M:%S")
                    sql += " \"%s\" <= \"TO_DATE\"('%s', 'yyyy-mm-dd hh24:mi:ss')" % (
                        cleanWork.databaseIncrementField, nowMax)
                except:
                    sql += " and %s <= '%s'" % (cleanWork.databaseIncrementField, nowMax)

                res = CleanWorkLog.objects.filter(workid=taskId).filter(status=0).aggregate(Max('incrementContent'))
                if res.get('incrementContent__max'):
                    lastMaxContent = res.get('incrementContent__max')
                    try:
                        # 如果是时间字符串
                        time.strptime(lastMaxContent, "%Y-%m-%d %H:%M:%S")
                        sql += " \"%s\" > \"TO_DATE\"('%s', 'yyyy-mm-dd hh24:mi:ss')" % (cleanWork.databaseIncrementField, lastMaxContent)
                    except:
                        sql += " and %s > '%s'" % (cleanWork.databaseIncrementField, lastMaxContent)
        print(sql)
        cleanMaster.write('LINE = """' + sql + '"""\n')

        # 获取空闲端口
        cleanMasterPort = func.getAvaliablePort()
        cleanMaster.write('PORT = ' + str(cleanMasterPort) + '\n')
        cleanMaster.write('initMaster(FROM_DB_SETTINGS, TO_DB_SETTINGS, TO_TABLE_NAME, LINE, PORT, TO_FIELD_LIST)')
        cleanMaster.close()

        print(cleanMasterFilePath + 'write over')
        pMaster = Popen("%s %s" % (settings.PYTHON3_PATH, cleanMasterFilePath), shell=True,
                        stdout=PIPE, stderr=PIPE)

        # 创建清洗成功数据库
        Successmodel = CleanSite.checkAndCreateTable(toTable, huafeng_settings.STANDARDDB, 'standardApp')
        if cleanWork.cleanWay == 0:
            Successmodel.objects.all().delete()
            print('cleanWay = 1,  delete all')
        standardDBSetting = CleanSite.getDBSettings(huafeng_settings.STANDARDDB)
        table, conn = CleanSite.checkTable(toTable, 'errordb', 'errorAppp')
        print(table, conn)
        conn, DBType = CleanSite.getConnection('standarddb')
        fieldTable = FieldTable.objects.filter(tableenglish=toTable)
        print(toTable, conn, DBType)
        print(fieldTable)
        cur = conn.cursor()
        for num in range(len(fieldTable)):
            if DBType == 'mysql':
                sql = "ALTER table %s MODIFY COLUMN %s  COMMENT '%s'" % (
                    toTable.upper() + '_STANDARDAPP', fieldTable[num].fieldenglish, fieldTable[num].fieldchinese)
            elif DBType == 'oracle':
                sql = "COMMENT ON COLUMN %s.%s IS '%s'" % (
                    toTable.upper() + '_STANDARDAPP', fieldTable[num].fieldenglish, fieldTable[num].fieldchinese)
            # print(sql)
            cur.execute(sql)
        cur.close()
        conn.close()

        # 开启节点采集任务
        MyIP = settings.MASTER_HOST
        cleanNodePlist = []
        for ip in settings.COLLECT_NODE:
            print("scp %s root@%s:~/" % (os.path.join(huafeng_settings.BASE_DIR, 'cleanSlave.py'), ip))
            p1 = Popen("scp %s root@%s:~/" % (os.path.join(huafeng_settings.BASE_DIR, 'cleanSlave.py'), ip),
                       shell=True,
                       stdout=PIPE, stderr=PIPE)
            p1.wait()
            if p1.returncode == 0:
                p2 = Popen("ssh root@%s '%s %s %s %s'" % (
                    ip, huafeng_settings.PYTHON3_PATH, 'cleanSlave.py', MyIP, cleanMasterPort),
                           shell=True, stdout=PIPE, stderr=PIPE)
                cleanNodePlist.append(p2)
            else:
                print('error in scp')

        successCount = 0
        # 等待清洗任务完成
        for cleanNodeP in cleanNodePlist:
            while cleanNodeP.poll() == None:
                time.sleep(3)
            cleanNodePOut = cleanNodeP.stdout.readlines()
            print(cleanWork.name, cleanNodePOut)
            try:
                cleanNodePSuccessCount = cleanNodePOut[-1].decode('utf-8').strip('\n').split(' ')[-1]
                print(cleanWork.name, cleanNodePSuccessCount)
            except Exception as e:
                print(e)
                cleanNodePSuccessCount = '0'
            successCount += int(cleanNodePSuccessCount)        

        # 如果有设置增量字段，则需要更新日志中的增量字段值
        try:
            if cleanWork.cleanWay:
                cleanWorkLog.incrementContent = nowMax
                cleanWorkLog.save()
                # print('begin find max')
                # print('successmodel', Successmodel)
                # if Successmodel:
                #     res = Successmodel.objects.all().aggregate(Max(cleanWork.databaseIncrementField))
                #     print('res', res)
                #     if res.get('%s__max' % cleanWork.databaseIncrementField):
                #         cleanWorkLog.incrementContent = res.get('%s__max' % cleanWork.databaseIncrementField)
                #         cleanWorkLog.save()
                #         print('end')
        except:
            print('get max %s error' % cleanWork.databaseIncrementField)

        cleanWork.status = 0
        cleanWork.save()
        # # 2.导出csv
        # importCsvFileName = 'dataImport%s.csv' % TIME_APPENDIX
        # importCsvFilePath = os.path.join(huafeng_settings.COLLECT_CLEAN_TEMP_DIR, importCsvFileName)
        # csvFile = open(importCsvFilePath, 'w')
        # writer = csv.writer(csvFile)
        #
        # dbsettings = CleanSite.getDBSettings(huafeng_settings.COLLECTDB)
        #
        # conn, DBType = CleanSite.getConnection(huafeng_settings.COLLECTDB)
        # cur = conn.cursor()
        #
        # joinTableFields = cleanWork.joinTableFields
        # sql = "SELECT %s FROM %s where 1=1" % (",".join(sorted(fromFieldAndToField.keys())), fromTable)
        # # print(",".join(fromFieldAndToField.keys()))
        # # return
        # if joinTableFields:
        #     joinFields = joinTableFields.split(',')
        #     for joinField in joinFields:
        #         sql += ' and ' + joinField
        # if DBType == 'mysql':
        #     # 如果是增量方式
        #     if cleanWork.cleanWay == 1:
        #         res = CleanWorkLog.objects.filter(workid=taskId).filter(status=0).aggregate(Max('maxtime'))
        #         if res.get('maxtime__max'):
        #             lastMaxTime = res.get('maxtime__max')
        #             sql += " and xxrksj > '%s'" % lastMaxTime.strftime('%Y-%m-%d %H:%M:%S')
        # elif DBType == 'oracle':
        #     if cleanWork.cleanWay == 1:
        #         res = CleanWorkLog.objects.filter(workid=taskId).filter(status=0).aggregate(Max('maxtime'))
        #         if res.get('maxtime__max'):
        #             lastMaxTime = res.get('maxtime__max')
        #             sql += " \"xxrksj\" > \"TO_DATE\"('%s', 'yyyy-mm-dd hh24:mi:ss')" % lastMaxTime.strftime(
        #                 '%Y-%m-%d %H:%M:%S')
        # print(sql)
        # # return
        # cur.execute(sql)
        #
        # fromTableContent = cur.fetchall()
        # for fromContent in fromTableContent:
        #     writer.writerow(fromContent)
        # csvFile.close()
        # # 3. 结果文件夹
        # hdfsResultDir = 'cleanResult%s' % TIME_APPENDIX
        # 4. python3 的路径


        # try:
        #     cmd = "python3 %s -r hadoop %s -o %s --python-bin=%s " % (cleanMasterFilePath, importCsvFilePath, hdfsResultDir, PYTHON3_PATH)
        #     print(cmd)
        #     res = os.system("su - hadoop -c '%s'" % cmd)
        #     if res:
        #         cleanWork.status = 0
        #         cleanWork.save()
        #         return JsonResponse({
        #             'errorCode': '0x0000',
        #             'errorString': "任务执行出错"
        #         })
        # except:
        #     cleanWork.status = 0
        #     cleanWork.save()
        #     return JsonResponse({
        #         'errorCode': '0x0000',
        #         'errorString': "任务执行出错"
        #     })

    @staticmethod
    def createTable(toTable, db, app_label = '', fields = None):
        """
        :param toTable:  表名
        :param db: 数据库名
        :param app_label: model所属app
        :param fields: [{field：字段名，cnname:字段注释,length：字段长度},{}]
        :return:
        """
        getAllToTableField = FieldTable.objects.filter(tableenglish=toTable)
        toTable = toTable.upper()
        class Meta:
           # print(app_label)
            #db_table = toTable
            pass
            #db_tablespace =
        if app_label:
            setattr(Meta, 'app_label', app_label)
            setattr(Meta, 'db_table', toTable+ '_' + app_label)
            # setattr(Meta, 'db_tablespace', app_label)
        else:
            print('app_label is not exits')
            return

        attr = {'__module__' : app_label + '.models', 'Meta': Meta}
        for num in range(len(getAllToTableField)):
            #if getAllToTableField[num].isPreKey == 1:
              #  attr[getAllToTableField[num].fieldenglish] = models.CharField(max_length=getAllToTableField[num].fieldlength,
               #                                                             primary_key=True, verbose_name = getAllToTableField[num].cnname)
                #attr['primary'] = (getAllToTableField[num].identifier)
            #else:
            if getAllToTableField[num].showtype == 'string' or getAllToTableField[num].showtype == 'date' or \
                            getAllToTableField[num].showtype == 'datetime':
                attr[getAllToTableField[num].fieldenglish] = models.CharField(
                    max_length=getAllToTableField[num].fieldlength, blank=True, null=True, verbose_name = getAllToTableField[num].fieldchinese)
            elif getAllToTableField[num].showtype == 'numeric':
                attr[getAllToTableField[num].fieldenglish] = models.IntegerField(blank=True, null=True, verbose_name = getAllToTableField[num].fieldchinese)
            elif getAllToTableField[num].showtype == 'binary':
                attr[getAllToTableField[num].fieldenglish] = models.BinaryField(blank=True, null=True, verbose_name = getAllToTableField[num].fieldchinese)
        if not fields is None:
            fields = json.loads(fields)
            for i in range(len(fields)):
                attr[fields[i]['field']] = models.CharField(max_length= fields[i]['length'] , blank= True, null= True, verbose_name= fields[i]['cnname'])
        classModel = type(toTable, (models.Model, ), attr)
        #classObject = type(classModel)
        from django.db import connections
        from django.db.backends.base.creation import BaseDatabaseCreation
        from django.core.management.color import no_style
        creation = BaseDatabaseCreation(connections[db])
        # print(creation)
        create_sql = creation.sql_create_model(classModel, no_style())[0]
        # print(create_sql)
        return classModel, create_sql

    @staticmethod
    def checkTable(table, db, app_label=''):
        dbsettings = CleanSite.getDBSettings(db)
        conn, DBType = CleanSite.getConnection(db)
        cur = conn.cursor()
        table = table.upper() + '_' + app_label.upper()
        if DBType == 'mysql':
            sql = "select TABLE_NAME from INFORMATION_SCHEMA.TABLES where TABLE_SCHEMA='%s' and TABLE_NAME='%s' ;" % (
                dbsettings['NAME'], table)
        elif DBType == 'oracle':
            sql = "select TABLE_NAME from all_tables where TABLE_NAME = '%s' and OWNER='%s'" % (
            table, dbsettings['USER'].upper())
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result, conn

    @staticmethod
    def checkAndCreateTable(table, db, app_label = '', fields = None):
        result, conn = CleanSite.checkTable(table, db, app_label)
        tableModel, creatTableSQL = CleanSite.createTable(table, db, app_label, fields)
        cur = conn.cursor()
        if result is None:
            for sql in creatTableSQL:
                print(sql)
                cur.execute(sql[0:-1])
            #cur.execute(creatTableSQL)
        cur.close()
        conn.close()
        return tableModel

    def receiveCleanResult(self, request):
        successFilePath = request.POST.get('successFilePath', '')
        errorFilePath = request.POST.get('errorFilePath', '')
        workid = request.POST.get('workid', '')

        cleanWork = CleanWork.objects.get(id=workid)
        # 记录日志
        cleanWorkLog = CleanWorkLog()
        cleanWorkLog.workid = workid
        cleanWorkLog.fromtable = cleanWork.fromTable
        cleanWorkLog.totable = cleanWork.toTable
        errorFlag = request.POST.get('error', '')
        if errorFlag:
            cleanWork.status = 0
            cleanWorkLog.status = 1
            cleanWork.save()
            cleanWorkLog.save()

            return JsonResponse({
                'errorCode': '0x0001',
                'errorString': "任务失败"
            })

        toTable = cleanWork.toTable
        # 采集表与标准表字段映射
        fromFieldAndToField = json.loads(cleanWork.fromFieldAndToField)
        # 标准表字段顺序
        toFieldList = []
        for fromField in sorted(fromFieldAndToField.keys()):
            toField = fromFieldAndToField[fromField]
            toFieldList.append(toField)
        successCount = 0
        errorCount = 0
        # 将结果csv导入数据库
        #standard = type()
        #创建清洗成功数据库

        Successmodel = self.checkAndCreateTable(toTable, 'standarddb', 'standardApp')
        #print(Successmodel)
        standardDBSetting = self.getDBSettings('standarddb')
        # standardDBType = self.getDBType('standarddb')
        table, conn = self.checkTable(toTable, 'errordb', 'errorAppp')
        print(table, conn)
        conn, DBType = self.getConnection('standarddb')
        fieldTable = FieldTable.objects.filter(tableenglish=toTable)
        print(toTable,conn, DBType)
        print(fieldTable)
        cur = conn.cursor()
        for num in range(len(fieldTable)):
            if DBType == 'mysql':
                sql = "ALTER table %s MODIFY COLUMN %s  COMMENT '%s'" % (
                    toTable.upper() + '_STANDARDAPP', fieldTable[num].fieldenglish, fieldTable[num].fieldchinese)
            elif DBType == 'oracle':
                sql = "COMMENT ON COLUMN %s.%s IS '%s'" % (
                    toTable.upper() + '_STANDARDAPP', fieldTable[num].fieldenglish, fieldTable[num].fieldchinese)
            print(sql)
            cur.execute(sql)
        cur.close()
        if os.path.exists(successFilePath) and os.path.exists(errorFilePath):
            errorCount = len(open(errorFilePath, 'rU').readlines())
            successFile = open(successFilePath, 'r', encoding='utf-8')
            reader = csv.reader(successFile)
            print(toFieldList)
            for line in reader:
                successCount += 1
                dicts = dict(zip(toFieldList, line))
                Successmodel.objects.create(**dicts)
            successFile.close()
            errorDBSetting = self.getDBSettings('errordb')

            if not table is None and errorCount:
                if DBType == 'mysql':
                    cur = conn.cursor(pymysql.cursors.DictCursor)
                    sql = "SELECT greatest (A.XXRKSJ,B.XXRKSJ) as T FROM %s.%s A , %s.%s B  ORDER BY  t DESC LIMIT 0,1" % (
                        standardDBSetting['NAME'], toTable.upper() + '_STANDARDAPP', errorDBSetting['NAME'], toTable.upper() + '_ERRORAPP')
                elif DBType == 'oracle':
                    cur = conn.cursor()
                    sql = "SELECT * FROM (select greatest(A.XXRKSJ,B.XXRKSJ) T FROM %s.%s A, %s.%s B ORDER BY  T DESC) WHERE ROWNUM <= 1" %(standardDBSetting['USER'].upper(), toTable.upper() + '_STANDARDAPP', errorDBSetting['USER'].upper(), toTable.upper() + '_ERRORAPP')
            else:
                cur = conn.cursor()
                sql = "select MAX(%s) T FROM %s " % ('XXRKSJ', toTable.upper() + '_STANDARDAPP')

            print(sql)
            cur.execute(sql)
            result = cur.fetchone()
            cur.close()
            conn.close()
            if successCount + errorCount != 0:
                successRate = successCount / (successCount + errorCount)
            else:
                successRate = 0
            print('result' , result)
            if not result is None and DBType == 'mysql':
                cleanWorkLog.maxtime = result['T']
            if not result[0] is None and DBType == 'oracle':
                cleanWorkLog.maxtime = result[0]
            cleanWorkLog.successrate = successRate
            cleanWorkLog.datacounts = successCount + errorCount
            cleanWork.status = 0
            print('errorCount:', errorCount)
            if errorCount:
                print(errorCount, '大于0')
                errorFields = [{'field':'WORKID', 'cnname':'任务ID', 'length': 20}]
                Errormodel = self.checkAndCreateTable(toTable, 'errordb', 'errorApp',json.dumps(errorFields))
                errorFile = open(errorFilePath, 'r', encoding='utf-8')
                reader = csv.reader(errorFile)
                for line in reader:
                    dicts = dict(zip(toFieldList, line))
                    dicts['WORKID'] = workid
                    print(dicts)
                    Errormodel.objects.create(**dicts)
                errorFile.close()
        else:
            print('success file not exists, please check it!')
            cleanWork.status = 2
            cleanWorkLog.status = 1
        print('success')
        cleanWork.save()
        cleanWorkLog.save()
        print(111111)
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': "任务完成"
        })

    def delete(self, request):
        ids = request.POST.get('data')
        try:
            CleanWork.objects.extra(where=['id in (' + ids + ')']).delete()
        except:
            return JsonResponse({
                'errorCode': '1',
                'errorString': '删除失败'
            })
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': '删除成功'
        })

    def save(self, request):
        postData = request.POST
        print(postData)
        print(request.get_host())
        # 首先创建models对象，遍历其字段，如果post数据中有与其字段名相同的值，则直接赋值，下一步再确认其他值
        newWork = CleanWork()
        fields = newWork._meta.get_all_field_names()
        for field in fields:
            setattr(newWork, field, postData.get(field))
        newWork.flag = 0
        newWork.status = 0
        if newWork.id == '':
            newWork.id = None

        # 第二个TAB页的数据
        timeDict= dict()
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
            timeDict={
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
        newWork.timeStr = timeStr
        print(timeStr)

        try:
            from dataCollect.models import CollectTask
            collectTask = CollectTask.objects.filter(newCollectCreateTableName=newWork.fromTable)
            newWork.cleanWay = collectTask[0].collectWay
            newWork.databaseIncrementField = collectTask[0].databaseIncrementField
        except:
            print('获取对应collectTask出错')

        newWork.save()

        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': '新增成功'
        })

    def getFieldsByTable(self, request):
        tableName = request.POST.get('tableName')
        dbName = request.POST.get('dbName')
        reTableName = request.POST.get('reTableName','no')
        collectdb = huafeng_settings.COLLECTDB
        standarddb = huafeng_settings.STANDARDDB
        list = []
        if dbName == standarddb:
            reg = '[a-zA-Z]+'
            re.compile(reg)
            res = re.match(reg, tableName)
            print(res.group())
            list_obj = FieldTable.objects.filter(tableenglish = res.group())
            print(list_obj)
            for num in range(len(list_obj)):
                temp = {
                    'value': list_obj[num].fieldenglish,
                    'text': list_obj[num].fieldenglish,
                    'name': list_obj[num].fieldchinese,
                    'identFieldName': list_obj[num].elementidentifier
                }
                list.append(temp)
        elif dbName == collectdb:
            dbsettings = self.getDBSettings(dbName)
            print(dbsettings)
            conn, DBType = self.getConnection(dbName)
            print(conn, DBType)
            tableNameArray = tableName.split(',')
            print(tableNameArray)
            for table in tableNameArray:
                if DBType == 'mysql':
                    cur  = conn.cursor()
                    sql = "SELECT column_name as Name,column_comment as Comment from information_schema.columns WHERE table_name = '%s' and table_schema='%s'" % (table, dbName)
                elif DBType == 'oracle':
                    cur = conn.cursor()
                    sql ="select A.COLUMN_NAME \"Name\",B.COMMENTS \"Comment\" from user_tab_columns \"A\",user_col_comments \"B\" where A.table_name='%s' and A.COLUMN_NAME = B.COLUMN_NAME and B.TABLE_NAME='%s' ORDER BY A.COLUMN_ID" % (table, table)
                cur.execute(sql)
                print(sql)
                list_obj = cur.fetchall()
                print(list_obj)

                for obj in list_obj:
                    if reTableName == 'yes':
                        value = table + '.' + obj[0]
                    else:
                        value = obj[0]
                    temp = {
                        'value': value,
                        'text': obj[0],
                        'name': obj[1],
                        'tableName':table,
                    }
                    list.append(temp)
            cur.close()
            conn.close()
        return HttpResponse(json.dumps(list), content_type='application/json')


    def getStandardTable(self, request):
        standardTables = MasterdataTable.objects.all()#only('table_english', 'table_chinese')

        tableList = []
        for standardTable in standardTables:
            tmp = {
                'value': standardTable.tableenglish,
                'text': standardTable.tablechinese,
            }
            tableList.append(tmp)
        return HttpResponse(json.dumps(tableList), content_type='application/json')

    # @staticmethod
    # def getEnabledWork():
    #     enabledCronJobs = CleanWork.objects.filter(flag=True).exclude(timeType=3)
    #     CRONJOBS = []
    #
    #     for enabledCronjob in enabledCronJobs:
    #         if enabledCronjob.crontabStr:
    #             crontabjob = eval(enabledCronjob.crontabStr)
    #             # return HttpResponse(crontabjob)
    #             CRONJOBS.append(crontabjob)
    #     setattr(settings, 'CRONJOBS', CRONJOBS)
    #     return settings
    #
    # @staticmethod
    # def refreshCleanWork():
    #
    #     settings = CleanSite.getEnabledWork()
    #     with CleanupCrontab(settings=settings) as crontab:
    #         try:
    #             crontab.remove_jobs()
    #             crontab.add_jobs()
    #         except:
    #             crontab.add_jobs()
    #
    # @staticmethod
    # def setCrontab(cleanwork, host):
    #
    #     funcStr = 'dataCleaning.views.sendBeginClean'
    #     id = cleanwork.id
    #     timeType = str(cleanwork.timeType)
    #     if timeType == '3':
    #         return JsonResponse({
    #             'errorCode': '0x0000',
    #             'errorString': '启用成功'
    #         })
    #
    #     else:
    #         timeStr = cleanwork.timeStr
    #         cronStr = ''
    #         if timeType == '1':
    #             timeObj = json.loads(timeStr)
    #
    #             if 'day' not in timeObj.keys() or timeObj['day'] == '':
    #                 timeObj['day'] = '*'
    #             if 'week' not in timeObj.keys() or timeObj['week'] == '':
    #                 timeObj['week'] = '*'
    #
    #             if isinstance(timeObj['week'], list):
    #                 timeObj['week'] = ','.join(timeObj['week'])
    #
    #             cronStr = "('%s %s %s * %s', '%s', [], {'workid': '%s', 'HOST': '%s'})" % (timeObj['min'], timeObj['hour'], timeObj['day'], timeObj['week'], funcStr, id, host)
    #         elif timeType == '2':
    #             timeObj = json.loads(timeStr)
    #             cronStr = "('%s %s %s %s *', '%s', [], {'workid': '%s', 'HOST': '%s'})" % (timeObj['min'], timeObj['hour'], timeObj['day'], timeObj['month'], funcStr, id, host)
    #
    #         elif timeType == '4':
    #             timeObj = json.loads(timeStr)
    #
    #             timeObj['min'] = '*/' + timeObj['min'] if timeObj['min'] and timeObj['min'] != '0' else '*'
    #             timeObj['hour'] = '*/' + timeObj['hour'] if timeObj['hour'] and timeObj['hour'] != '0' else '*'
    #             timeObj['day'] = '*/' + timeObj['day'] if timeObj['day'] and timeObj['day'] != '0' else '*'
    #
    #             cronStr = "('%s %s %s * *', '%s', [], {'workid': '%s', 'HOST': '%s'})" % (timeObj['min'], timeObj['hour'], timeObj['day'], funcStr, id, host)
    #
    #
    #     cleanwork.crontabStr = cronStr
    #     cleanwork.save()
    #
    #     CleanSite.refreshCleanWork()
    #
    #     return JsonResponse({
    #         'errorCode': '0x0000',
    #         'errorString': '启用成功'
    #     })


site = CleanSite()
