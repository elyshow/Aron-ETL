from django.shortcuts import render, render_to_response
from dataway.models import Adminapi, Conditionapi, Fieldapi
from .models import *
from cataloguedataway.models import Cataloguedataway, Cataloguedatawaybm
from django.http.response import HttpResponse
from user.models import Userpermission
import json
from django.http import JsonResponse
from InterfaceCatalogue import myGlobal
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


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


def interface(rq):
    try:
        curPage = int(rq.GET.get('curPage', '1'))
        allPage = int(rq.GET.get('allPage', '1'))
        pageType = str(rq.GET.get('pageType', ''))
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
        allPostCounts = Cataloguedataway.objects.filter(typeparentid=1).count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    data = Cataloguedataway.objects.filter(typeparentid=1)[startPos:endPos]

    middlepos = rq.POST.get('goPage')
    if middlepos is not None:
        if int(middlepos) <= int(allPage):
            startPos = (int(middlepos) - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            data = Cataloguedataway.objects.filter(typeparentid=1)[startPos:endPos]
            curPage = int(middlepos)
        else:
            startPos = (int(allPage) - 1) * ONE_PAGE_OF_DATA
            endPos = startPos + ONE_PAGE_OF_DATA
            data = Cataloguedataway.objects.filter(typeparentid=1)[startPos:endPos]
            curPage = int(allPage)

    return render_to_response('InterfaceCatalogue/interface.html',
                              {'data': data, 'allPage': allPage, 'curPage': curPage},
                              context_instance=RequestContext(rq))


def interfacecatalogue1(request, typeid):
    myGlobal.InterfaceCatalogueHierarchy_1 = typeid
    # if not request.user.is_authenticated():
    #     return render_to_response("user/login.html")
    # else:
    #     usernameGet = request.user
    #     a = Userpermission.objects.get(userid=usernameGet)
    #     perlist = dataDisplay(a)
    #     for index in perlist:
    #         if index == myGlobal.InterfaceCatalogueHierarchy_1:
    return render_to_response('InterfaceCatalogue/interfacecatalogue1.html')
    #return HttpResponse('你没有访问此资源或目录的权限')


def interfacecatalogue1_table(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    if 'condition' in request.POST:
        counts = Cataloguedataway.objects.filter(cataloguename__icontains=request.POST.get('condition'),
                                                 typeparentid=myGlobal.InterfaceCatalogueHierarchy_1).count()
        data = Cataloguedataway.objects.filter(cataloguename__icontains=request.POST.get('condition'),
                                               typeparentid=myGlobal.InterfaceCatalogueHierarchy_1)[start:end]
    else:
        counts = Cataloguedataway.objects.filter(typeparentid=myGlobal.InterfaceCatalogueHierarchy_1).count()
        data = Cataloguedataway.objects.filter(typeparentid=myGlobal.InterfaceCatalogueHierarchy_1)[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'typeid': data[num].typeid,
            'cataloguename': data[num].cataloguename,
            'typetime': data[num].typetime,
            'count': data[num].count,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


def interfacecatalogue2_request(request):
    qqq = request.GET['data']
    myGlobal.InterfaceCatalogueHierarchy_2 = qqq
    return render_to_response('InterfaceCatalogue/interfacecatalogue2.html')


def interfacecatalogue2(request):
    # if not request.user.is_authenticated():
    #     return render_to_response("user/login.html")
    # else:
    #     usernameGet = request.user
    #     a = Userpermission.objects.get(userid=usernameGet)
    #     perlist = dataDisplay(a)
    #     for index in perlist:
    #         if index == myGlobal.InterfaceCatalogueHierarchy_2:
    return render_to_response('InterfaceCatalogue/interfacecatalogue2.html')
    #return HttpResponse('你没有访问此资源或目录的权限')


def interfacecatalogue2_table(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Cataloguedataway.objects.filter(cataloguename__icontains=request.POST.get('condition'),
                                                 typeparentid=myGlobal.InterfaceCatalogueHierarchy_2).count()
        data = Cataloguedataway.objects.filter(cataloguename__icontains=request.POST.get('condition'),
                                               typeparentid=myGlobal.InterfaceCatalogueHierarchy_2)[start:end]
    else:
        counts = Cataloguedataway.objects.filter(typeparentid=myGlobal.InterfaceCatalogueHierarchy_2).count()
        data = Cataloguedataway.objects.filter(typeparentid=myGlobal.InterfaceCatalogueHierarchy_2)[start:end]
    list = []
    for num in range(len(data)):
        temp = {
            'typeid': data[num].typeid,
            'cataloguename': data[num].cataloguename,
            'typetime': data[num].typetime,
            'count': data[num].count,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


def interfacetable_request(request):
    qqq = request.GET['data']
    myGlobal.InterfaceCatalogueHierarchy_3 = qqq
    return render_to_response('InterfaceCatalogue/interfacetable.html')


def interfacetable(request):
    # if not request.user.is_authenticated():
    #     return render_to_response("user/login.html")
    # else:
    #     usernameGet = request.user
    #     a = Userpermission.objects.get(userid=usernameGet)
    #     perlist = dataDisplay(a)
    #     for index in perlist:
    #         if index == myGlobal.InterfaceCatalogueHierarchy_3:
    return render_to_response('InterfaceCatalogue/interfacetable.html')
    #return HttpResponse('你没有访问此资源或目录的权限')


def interfacetable_table(request):
    cc = Admintwo.objects.all().delete()
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    a = Cataloguedatawaybm.objects.filter(typeid=myGlobal.InterfaceCatalogueHierarchy_3)
    for num in range(len(a)):
        print(a[num].idapi)
        b = Adminapi.objects.get(idapi=a[num].idapi)
        c = Admintwo()
        c.typeid = a[num].typeid
        c.idapi = b.idapi
        c.nameapi = b.nameapi
        c.warehouseapi = b.warehouseapi
        c.tableapi = b.tableapi
        c.createtime = b.createtime
        c.weiyi = 123456
        c.save()
    if 'condition' in request.POST:
        counts = Admintwo.objects.filter(nameapi__icontains=request.POST.get('condition'),
                                         typeid=myGlobal.InterfaceCatalogueHierarchy_3).count()
        data = Admintwo.objects.filter(nameapi__icontains=request.POST.get('condition'),
                                       typeid=myGlobal.InterfaceCatalogueHierarchy_3)[start:end]
    else:
        counts = Admintwo.objects.filter(typeid=myGlobal.InterfaceCatalogueHierarchy_3).count()
        data = Admintwo.objects.filter(typeid=myGlobal.InterfaceCatalogueHierarchy_3)[start:end]

    list = []
    for num in range(len(data)):
        temp = {
            'idapi': data[num].idapi,
            'nameapi': data[num].nameapi,
            'warehouseapi': data[num].warehouseapi,
            'tableapi': data[num].tableapi,
            'createtime': data[num].createtime,
        }
        list.append(temp)

    return JsonResponse({'total': counts, 'rows': list})


def interfacedetailed_request(request):
    qqq = request.GET['data']
    myGlobal.InterfaceCatalogueHierarchy_4 = qqq

    return render_to_response('InterfaceCatalogue/interfacedetailed.html')


def interfacedetailed(request):
    return render_to_response('InterfaceCatalogue/interfacedetailed.html')


def interfacetable_index(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Fieldapi.objects.filter(idAPI__icontains=request.POST.get('condition'),
                                         idapi=myGlobal.InterfaceCatalogueHierarchy_4).count()
        data = Fieldapi.objects.filter(idAPI__icontains=request.POST.get('condition'),
                                       idapi=myGlobal.InterfaceCatalogueHierarchy_4)[start:end]
    else:
        counts = Fieldapi.objects.filter(idapi=myGlobal.InterfaceCatalogueHierarchy_4).count()
        data = Fieldapi.objects.filter(idapi=myGlobal.InterfaceCatalogueHierarchy_4)[start:end]
    list = []
    for num in range(len(data)):
        a = json.loads(data[num].fieldData)
        field_english = (a['field_english'])
        field_chinese = (a['field_chinese'])
        show_type = (a['show_type'])
        temp = {
            'idAPI': data[num].idapi,
            'field_english': field_english,
            'field_chinese': field_chinese,
            'show_type': show_type,
        }
        list.append(temp)
    return JsonResponse({'total': counts, 'rows': list})


def condition_request(request):
    qqq = request.GET['data']
    myGlobal.InterfaceCatalogueHierarchy_4 = qqq
    return render_to_response('InterfaceCatalogue/condition.html')


def condition(request):
    return render_to_response('InterfaceCatalogue/condition.html')


def condition_table(request):
    print(97687999)
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Conditionapi.objects.order_by("-id").filter(conditionname__icontains=request.POST.get('condition'),
                                                             idapi=myGlobal.InterfaceCatalogueHierarchy_4).count()
        data = Conditionapi.objects.order_by("-id").filter(conditionname__icontains=request.POST.get('condition'),
                                                           idapi=myGlobal.InterfaceCatalogueHierarchy_4)[start:end]
    else:
        counts = Conditionapi.objects.order_by("-id").filter(idapi=myGlobal.InterfaceCatalogueHierarchy_4).count()
        print(counts)
        data = Conditionapi.objects.order_by("-id").filter(idapi=myGlobal.InterfaceCatalogueHierarchy_4)[start:end]
    list = []
    for num in range(len(data)):
        b = json.loads(data[num].conditionname)
        print(111)
        field_english = (b['field_english'])
        print(222)
        field_chinese = (b['field_chinese'])
        print(333)
        show_type = (b['show_type'])
        print(444)
        temp = {
            'id': data[num].id,
            'idAPI': data[num].idapi,
            'field_english': field_english,
            'field_chinese': field_chinese,
            'show_type': show_type,
        }
        list.append(temp)
        print(list)
    print(myGlobal.InterfaceCatalogueHierarchy_4)
    print(354354)
    return JsonResponse({'total': counts, 'rows': list})