from django.shortcuts import render, render_to_response
from .models import ReleaseCatalogue,ResourceField
from catalogueManagement.models import Catalogue
from standardApp.models import *
# from user.models import Userpermission
from django.contrib import auth
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseRedirect
import json
from django.http import JsonResponse
from dataProfile import myGlobal
from django.template import RequestContext
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

def dataDisplay(par):
    b = par.permissionway
    c = b.split(',')
    list = []
    for i in c:
        cansee = []
        i1 = i[0:1]
        cansee.append(i1)
        i2 = i[0:4]
        cansee.append(i2)
        i3 = i[0:7]
        cansee.append(i3)
        list += cansee
    return list

ONE_PAGE_OF_DATA = 9
def dataprofile(rq):
    try:
        curPage = int(rq.GET.get('curPage', '1'))
        allPage = int(rq.GET.get('allPage', '1'))
        pageType = str(rq.GET.get('pageType',''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
        # 判断点击了【下一页】还是【上一页】
    if pageType == 'pageDown':
        curPage += 1
    elif pageType == 'pageUp':
        curPage -= 1

    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = Catalogue.objects.filter(typeparentid=1).count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    data = Catalogue.objects.filter(typeparentid=1)[startPos:endPos]

    middlepos = rq.POST.get('goPage')
    if middlepos is not None:
        if int(middlepos) <= int(allPage):
            startPos = (int(middlepos) - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            data = Catalogue.objects.filter(typeparentid=1)[startPos:endPos]
            curPage = int(middlepos)
        else:
            startPos = (int(allPage) - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            data = Catalogue.objects.filter(typeparentid=1)[startPos:endPos]
            curPage = int(allPage)
    return render_to_response('dataProfile/dataprofile.html',
                              {'data': data,'allPage': allPage,'curPage': curPage},
                              context_instance=RequestContext(rq))

def catalogue1(request,typeid):
    myGlobal.dataProfileHierarchy_1=typeid
    #if not request.user.is_authenticated():
    #   return render_to_response("user/login.html")
    #else:
     #   usernameGet = request.user
    #    a = Userpermission.objects.get(userid=usernameGet)
    #    perlist=dataDisplay(a)
    #    for index in perlist:
    #        if index == myGlobal.dataProfileHierarchy_1:
    return render_to_response('dataProfile/catalogue1.html')
    # return HttpResponse('你没有访问此资源或目录的权限')

def catalogue1_table(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Catalogue.objects.filter(cataloguename__icontains=request.POST.get('condition'),typeparentid=myGlobal.dataProfileHierarchy_1).count()
        data = Catalogue.objects.filter(cataloguename__icontains=request.POST.get('condition'),typeparentid=myGlobal.dataProfileHierarchy_1)[start:end]
    else:
        counts = Catalogue.objects.filter(typeparentid=myGlobal.dataProfileHierarchy_1).count()
        data = Catalogue.objects.filter(typeparentid=myGlobal.dataProfileHierarchy_1)[start:end]
    list=[]
    for num in range(len(data)):
        temp = {
            'typeid':data[num].typeid,
            'cataloguename':data[num].cataloguename,
            'typetime':data[num].typetime,
            'count':data[num].count,
        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def catalogue2_request(request):
    qqq = request.GET['data']
    myGlobal.dataProfileHierarchy_2=qqq
    return render_to_response('dataProfile/catalogue2.html')

def catalogue2(request):
    # if not request.user.is_authenticated():
    #     return render_to_response("user/login.html")
    # else:
    #     usernameGet = request.user
    #     a = Userpermission.objects.get(userid=usernameGet)
    #     perlist = dataDisplay(a)
    #     for index in perlist:
    #         if index == myGlobal.dataProfileHierarchy_2:
    return render_to_response('dataProfile/catalogue2.html')
    # return HttpResponse('你没有访问此资源或目录的权限')

def catalogue2_table(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Catalogue.objects.filter(cataloguename__icontains=request.POST.get('condition'),typeparentid=myGlobal.dataProfileHierarchy_2).count()
        data = Catalogue.objects.filter(cataloguename__icontains=request.POST.get('condition'),typeparentid=myGlobal.dataProfileHierarchy_2)[start:end]
    else:
        counts = Catalogue.objects.filter(typeparentid=myGlobal.dataProfileHierarchy_2).count()
        data = Catalogue.objects.filter(typeparentid=myGlobal.dataProfileHierarchy_2)[start:end]
    list=[]
    for num in range(len(data)):
        temp = {
            'typeid':data[num].typeid,
            'cataloguename':data[num].cataloguename,
            'typetime':data[num].typetime,
            'count':data[num].count,
        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def table_request(request):
    qqq = request.GET['data']
    myGlobal.dataProfileHierarchy_3=qqq
    return render_to_response('dataProfile/table.html')

def table(request):
    # if not request.user.is_authenticated():
    #     return render_to_response("user/login.html")
    # else:
    #     usernameGet = request.user
    #     a = Userpermission.objects.get(userid=usernameGet)
    #     perlist = dataDisplay(a)
    #     for index in perlist:
    #         if index == myGlobal.dataProfileHierarchy_3:
    return render_to_response('dataProfile/table.html')
    # return HttpResponse('你没有访问此资源或目录的权限')

def table_table(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = ReleaseCatalogue.objects.filter(resourcename__icontains=request.POST.get('condition'),typeid=myGlobal.dataProfileHierarchy_3).count()
        data = ReleaseCatalogue.objects.filter(resourcename__icontains=request.POST.get('condition'),typeid=myGlobal.dataProfileHierarchy_3)[start:end]
    else:
        counts = ReleaseCatalogue.objects.filter(typeid=myGlobal.dataProfileHierarchy_3).count()
        data = ReleaseCatalogue.objects.filter(typeid=myGlobal.dataProfileHierarchy_3)[start:end]
    list=[]
    for num in range(len(data)):
        temp = {
            'typeid':data[num].typeid,
            'resourcename':data[num].resourcename,
            'releasetime':data[num].releasetime,
            'resourceid':data[num].resourceid,
        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def detailed_request(request):
    data1 = request.GET['data1']
    data2 = request.GET['data2']
    print(data1, data2)
    print(111111111111111111)
    myGlobal.dataProfileHierarchy_4=data1
    myGlobal.dataProfileHierarchy_5=data2
    return render_to_response('dataProfile/detailed.html')

def getResourceAttr(request):
    id = request.POST.get('resourceid','')
    obj = ReleaseCatalogue.objects.get(resourceid= id)
    list = [{
        'name':'资源名称',
        'value':obj.resourcename
    },{
        'name': '行业信息',
        'value': obj.industryInfo
    },{
        'name': '要素分类',
        'value': obj.cadastre
    },{
        'name': '资源属性分类',
        'value': obj.resourceAttrCatalog
    },{
        'name': '共享范围',
        'value': obj.sharedScope
    },{
        'name': '共享地区',
        'value': obj.sharedArea
    },{
        'name': '共享部门',
        'value': obj.sharedDepartment
    },{
        'name': '共享方式',
        'value': obj.sharedMode
    },{
        'name': '资源事权单位',
        'value': obj.sourceUnit
    },{
        'name': '公安业务分类',
        'value': obj.businessCatalog
    },{
        'name': '资源提供单位',
        'value': obj.resourceProUnit
    },{
        'name': '更新方式',
        'value': obj.updateMode
    },{
        'name': '更新周期和资源描述信息',
        'value': obj.updateCycleAndDes
    },
    ]
    return HttpResponse(json.dumps(list), content_type='application/json')


def getResourceField(request):
    page = int(request.POST.get('page', 1))
    rows = int(request.POST.get('rows', 10))
    start = (page - 1) * rows
    end = page * rows
    resourceid = request.POST.get('resourceid', '')
    data = ResourceField.objects.filter(resourceid=resourceid)[start:end]
    total = ResourceField.objects.filter(resourceid=resourceid).count()
    list = []
    for num in range(len(data)):
        list.append(json.loads(data[num].fieldenglish))
    return JsonResponse({'total':total, 'rows': list})



def detailed(request):
    print(myGlobal.dataProfileHierarchy_4)
    data = ResourceField.objects.filter(resourceid=myGlobal.dataProfileHierarchy_4)
    title=[]
    ctitle=[]
    print(data)
    for num in range(len(data)):
        a = json.loads(data[num].fieldenglish)
        field_english = (a['field_english'])
        print(field_english)
        field_chinese = (a['field_chinese'])
        print(field_chinese)
        if field_chinese =='':
            field_chinese='字段中文名'
        tableenglish = data[num].tableenglish
        title.append(field_english)
        ctitle.append(field_chinese)
    tlen=len(title)
    #print(tableenglish.)
    detailed =eval(str(tableenglish.upper() + '_standardApp'.upper())+'.objects.all()')
    content=[]
    for n in detailed:
        for m in range(len(title)):
            nn = eval('n.'+str(title[m]))
            content.append(nn)
    clen=len(content)
    rowRange = range(int(clen/tlen))
    tRange = range(tlen)

    print({'title':title,'content':content,'tlen':tlen,'clen':clen, 'rowRange': rowRange, 'tRange': tRange,'ctitle':ctitle})
    return render_to_response('dataProfile/detailed.html',{'title':title,'content':content,'tlen':tlen,'clen':clen, 'rowRange': rowRange, 'tRange': tRange,'ctitle':ctitle})