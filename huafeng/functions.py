import os
import random
import datetime
import time
import uuid
import cx_Oracle



def getAvaliablePort():
    """
    获取可用端口号
    :return:
    """
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt = random.randint(15000, 20000)
    if tt not in procarr:
        return tt
    else:
        getAvaliablePort()


def dataToString(data):
    if isinstance(data, cx_Oracle.LOB):
        return data.__str__()
    elif isinstance(data, datetime.datetime):
        return data.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(data, datetime.date):
        return data.strftime('%Y-%m-%d')
    elif isinstance(data, uuid.UUID):
        return data.__str__()
    else:
        return data