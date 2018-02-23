from django.shortcuts import render,HttpResponse
import json
from .models import Cataloguedataway
from django.http import JsonResponse
import time

# Create your views here.

def index(request):
    return render(request, 'cataloguedataway/index.html')



#递归函数
def getTree(pid = 0,res = []):
    data = Cataloguedataway.objects.filter(typeparentid= pid)
    lens = len(data)
    for num in range(0, lens):
        num = int(num)
        temp = {
             'id':  data[num].typeid,
             'typeparentid':data[num].typeparentid,
             'cataloguename':data[num].cataloguename,
             'typetime': data[num].typetime,
        }
        # print(num)
        res.append(temp)
        if not hasattr(res[num],'children'):
            res[num]['children'] = []
        res[num]['children'] = getTree(data[num].typeid, res[num]['children'])
    return res

#发布的列表树
def getData(request):
    lists = getTree(1,[])
    return HttpResponse(json.dumps(lists), content_type="application/json")


#存
def saveCleaningRules(request):
    result = {'errorCode':'0x0000', 'errorString': ''}
    if request.method == 'POST':
        cataloguename = request.POST.get('cataloguename')
        typeparentid = request.POST.get('typeparentid')
        id = request.POST.get('id')
        # print(cataloguename)
        print(typeparentid)
        print(id)
        if request.POST.get('save_type') == 'edit':
            data = Cataloguedataway.objects.get(typeid = id)
            data.cataloguename = cataloguename
            data.typeparentid = typeparentid
        elif request.POST.get('save_type') == 'add':
            if Cataloguedataway.objects.filter(typeparentid=id):
                numdata = Cataloguedataway.objects.filter(typeparentid=id)
                listid = []
                for num in range(len(numdata)):
                    listid.append(numdata[num].typeid)
                numid = max(listid)+1
                data = Cataloguedataway(cataloguename=cataloguename, typeparentid=id,typeid=numid,count=0,
                                        typetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            elif id==0:
                numid = int(id)
                numid2 = numid+1
                data = Cataloguedataway(cataloguename = cataloguename,count = 0,  typeparentid = id,  typeid = numid2, typetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

            else:
                numid = int(id)*1000
                numid2 = numid+1
                data = Cataloguedataway(cataloguename = cataloguename,count = 0,  typeparentid = id,  typeid = numid2, typetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

        try:
            data.save()
        except:
            result.errorCode = '0x0001'
            result.errorString = '数据库操作失败'
    else:
        result.errorCode = '0x0002'
        result.errorString = '参数错误'
    return JsonResponse(result)

#删
def delCleaningRules(request):
    result = {'errorCode': '0x0000', 'errorString': ''}
    if request.method == 'POST':
        ids = request.POST.get('data')
        # print(ids)
        try:
            Cataloguedataway.objects.extra(where=['typeid in ('+ ids + ')']).delete()
        except:
            result.errorCode = '0x0001'
            result.errorString = '数据库操作失败'
    else:
        result.errorCode = '0x0002'
        result.errorString = '参数错误'
    return JsonResponse(result)

def allData(request):
    print("nihao")
    a = request.POST.get('dataid', 0)
    print(a)
    b = str(a)
    # b = int(a)
    # print(222)
    # print(b)
    if len(b)>2:
        print(9292)
        data = Cataloguedataway.objects.all()
        print(data)
        print("hello")
        lens = len(data)
        list = []
        for num in range(0, lens):
            num = int(num)
            temp = {
                'id': data[num].typeid,
                'typeparentid': data[num].typeparentid,
                'cataloguename': data[num].cataloguename,
                'typetime': data[num].typetime,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type="application/json")
    elif len(b)<2:
        print(82910)
        data = Cataloguedataway.objects.filter(typeid=911)
        print(data)
        print("hello")
        lens = len(data)
        list = []
        for num in range(0, lens):
            num = int(num)
            temp = {
                'id': data[num].typeid,
                'typeparentid': data[num].typeparentid,
                'cataloguename': data[num].cataloguename,
                'typetime': data[num].typetime,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type="application/json")