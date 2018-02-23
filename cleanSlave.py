# -*- encoding: utf-8 -*-
import pymysql, os, petl, sys, cx_Oracle
import multiprocessing
from multiprocessing import Value, Lock
from multiprocessing.managers import BaseManager
from petl.io.db_utils import _quote, _placeholders
from petl.io.db import SQL_INSERT_QUERY
import time

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.AL32UTF8'


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

lock = Lock()
insertSum = Value('i', 0)


def insertRows(to_db_setting, insertquery):
    global lock, insertSum
    TO_DB_CON = getDBConnection(to_db_setting)
    toCur = TO_DB_CON.cursor()
    setting = slave.manager.getConfigQueue().get(1)
    flag = setting['endFlag']
    slave.manager.getConfigQueue().put(setting)
    while (not flag) or slave.manager.getDispatchedJobQueue().qsize():
        data = slave.manager.getDispatchedJobQueue().get(1) if not flag else slave.manager.getDispatchedJobQueue().get(0, 30)
        try:
            toCur.executemany(insertquery, data)
            TO_DB_CON.commit()
            with lock:
                if isinstance(toCur.rowcount, int):
                    insertSum.value += toCur.rowcount
        except Exception as e:
            print(e)
            TO_DB_CON.rollback()
        setting = slave.manager.getConfigQueue().get(1)
        flag = setting['endFlag']
        slave.manager.getConfigQueue().put(setting)
    toCur.close()
    TO_DB_CON.close()

        
class Slave():
    def __init__(self, host, port, disPatchedJobListLegth = 100):
        self.host = host
        self.port = port
        self.disPatchedJobListLegth = disPatchedJobListLegth
        
    def start(self):
        BaseManager.register('getDispatchedJobQueue')
        BaseManager.register('getConfigQueue')
        self.manager = BaseManager(address=(self.host, self.port), authkey=b'huafeng@123+1s')

        try:
            self.manager.connect()
        except:
            time.sleep(3)
            self.manager.connect()

        self.dispatchJob = self.manager.getDispatchedJobQueue()
        
        self.setting = self.manager.getConfigQueue().get(1)
        self.manager.getConfigQueue().put(self.setting)
        
        TO_DB_CON = getDBConnection(self.setting['to_db_setting'])
        hdr = self.setting['to_field_list']
        flds = list(map(str, hdr))
        colnames = [_quote(n) for n in flds]
        insertcolnames = ', '.join(colnames)
        placeholders = _placeholders(TO_DB_CON, colnames)
        insertquery = SQL_INSERT_QUERY % (self.setting['to_db_table'], insertcolnames, placeholders)
        TO_DB_CON.close()
        #FROM_DB_CON.close()
        return insertquery

    def startThread(self, insertquery):
        size = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=size)
        for i in range(size - 1):
            pool.apply_async(insertRows, (self.setting['to_db_setting'], self.manager, insertquery, ))
        pool.close()
        pool.join()
        # insertRows(self.setting['to_db_setting'], self.manager, insertquery, )
    

if __name__ == '__main__':
    slave = Slave(sys.argv[1], int(sys.argv[2]))
    insertquery = slave.start()
    size = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=size)
    # print('start pool')
    #
    # print(slave.setting['to_db_setting'], slave.manager, insertquery, )
    if size >= 16:
        size = 15
    else:
        size = size - 1
    for i in range(size):
        pool.apply_async(insertRows, (slave.setting['to_db_setting'], insertquery))
    pool.close()
    pool.join()
    print('insertSum', insertSum.value)
    # print('endtime', time.strftime('%F %T', time.localtime()))
