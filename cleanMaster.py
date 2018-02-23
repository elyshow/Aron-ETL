# -*- encoding: utf-8 -*-
from queue import Queue
from multiprocessing.managers import BaseManager
import pymysql, os, petl, cx_Oracle
import time
import re

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


class Master():
    def __init__(self, fromDBSetting, toDBSetting, toDBTableName, line, port, toFieldList, disPatchedJobListLegth = 50, getDataLength = 10000):
        # 派发出去的作业队列
        self.dispatchedJobQueue = Queue(disPatchedJobListLegth)
        # 配置作业队列
        self.config = Queue(1)
        self.FROM_DB_CON = None
        self.fromDBSetting = fromDBSetting
        self.getDataLength = getDataLength
        self.port = port
        self.line = line
        self.toFieldList = toFieldList
        self.config.put({'endFlag': False, 'line': line, 'from_db_setting': fromDBSetting, 'to_db_setting': toDBSetting, 'to_db_table': toDBTableName, 'to_field_list': toFieldList})
        self.manager = None

    def getDispatchedJobQueue(self):
        return self.dispatchedJobQueue

    def getConfigQueue(self):
        return self.config

    def start(self):
        BaseManager.register('getDispatchedJobQueue', callable=self.getDispatchedJobQueue)
        BaseManager.register('getConfigQueue', callable=self.getConfigQueue)
        self.manager = BaseManager(address=('0.0.0.0', self.port), authkey=b'huafeng@123+1s')

        self.manager.start()
        self.FROM_DB_CON = self.getDBConnection(self.fromDBSetting)

        self.selectRows(self.line)
        
        while self.manager.getDispatchedJobQueue().qsize():
            time.sleep(5)
        self.manager.shutdown()

    @staticmethod
    def getDBConnection(DB_SETTINGS):
        if DB_SETTINGS['ENGINE'].endswith('mysql'):
            connection = pymysql.connect(host=DB_SETTINGS['HOST'],
                                         user=DB_SETTINGS['USER'],
                                         password=DB_SETTINGS['PASSWORD'],
                                         database=DB_SETTINGS['NAME'],
                                         port=int(DB_SETTINGS['PORT']), )
        elif DB_SETTINGS['ENGINE'].endswith('oracle'):
            dsn = '%s:%s/%s' % (DB_SETTINGS['HOST'], DB_SETTINGS['PORT'], DB_SETTINGS['NAME'])
            connection = cx_Oracle.connect(user=DB_SETTINGS['USER'], password=DB_SETTINGS['PASSWORD'], dsn=dsn)
        else:
            connection = None
        return connection

    def selectRows(self, line):
        currentCount = 0
        listLength = 0
        list1 = []
        fromTable = petl.fromdb(self.FROM_DB_CON, line)
        it = iter(fromTable)
        hdr = next(it)
        for one in it:
            transDatas = []
            flag = True
            for i in range(len(one)):
                if CHECK_RULE[i]:
                    if not CHECK_RULE[i].startswith('def'):
                        p = re.compile(CHECK_RULE[i])
                        if isinstance(one[i], str):
                            if not p.match(one[i]):
                                flag = False
                                break
                        else:
                            flag = False
                            break
                    else:
                        method_name = re.search(r'def (\w+)\(', CHECK_RULE[i]).group(1)
                        exec(CHECK_RULE[i])
                        if not eval(method_name)(one[i]):
                            flag = False
                            break

                if CLEAN_RULE[i]:
                    afterTransData = one[i]
                    if isinstance(CLEAN_RULE[i], dict):
                        for keyStr in CLEAN_RULE[i].keys():
                            try:
                                p = re.compile(keyStr)
                                res = p.search(one[i])
                                if res:
                                    afterTransData = re.sub(keyStr, CLEAN_RULE[i].get(keyStr), one[i])
                                    break
                            except:
                                continue

                    elif isinstance(CLEAN_RULE[i], str):
                        method_name = re.search(r'def (\w+)\(', CLEAN_RULE[i]).group(1)
                        exec(CLEAN_RULE[i])
                        afterTransData = eval(method_name)(one[i])
                else:
                    afterTransData = one[i]
                transDatas.append(afterTransData)

            if flag:
                list1.append(transDatas)
                currentCount += 1
                listLength += 1

            if listLength == self.getDataLength:
                print(self.manager.getDispatchedJobQueue().qsize())
                qList = list1
                self.manager.getDispatchedJobQueue().put(qList)
                list1 = []
                listLength = 0
        
        if len(list1):
            self.manager.getDispatchedJobQueue().put(list1)
        
        data = self.manager.getConfigQueue().get(1)
        data['endFlag'] = True
        self.manager.getConfigQueue().put(data)


def initMaster(fromDBSetting, toDBSetting, toDBTableName, line, port, toFieldList):
    master = Master(fromDBSetting, toDBSetting, toDBTableName, line, port, toFieldList)
    print('start', time.strftime('%F %T', time.localtime()))
    master.start()




