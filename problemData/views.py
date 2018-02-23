# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings

from .models import Problems,ProblemsDisplay
from .models import Catalogue,CatalogueDisplay
from .models import Release,ReleaseDisplay
from .models import Resourcefield,ResourcefieldDisplay
from .models import Assesstb,AssesstbDisplay

from dataQualityManagement.models import Base,BaseDisplay
from dataQualityManagement.models import Table6,Table6Display


import os,time
import pymysql
import os.path
import re
from django.http.response import HttpResponse
import json
from django.http import JsonResponse
from problemData import myGlobal
from django.template import RequestContext
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger

import datetime,calendar
import time




def question(request):
    return render_to_response('problemData/question.html')
    
def question_table(request):

    # dodo = Base.objects.all()
    dd = Table6.objects.all()
    for h in dd:
        cc = Problems()
        cc.id = h.id
        cc.schemename = h.schemename
        cc.checkobject = h.card
        cc.problemrecords = h.foundproblemrecords
        cc.repairrecords =h.checkrecords
        cc.save()
    # ds = Problems.objects.all()
    # list1=[]
    # list2=[]
    # dataash=[]
    # datanr=[]
    # datafpr=[]
    # for i in dodo:
    #     card = i.card
    #     schemename = i.schemename
    #     list1.append(card)
    #     list2.append(schemename)
    # for j in dd:
    #     schemename = j.schemename
    #     print(schemename)
    #     dataash.append(schemename)
    #     newrecords = j.newrecords
    #     datanr.append(newrecords)
    #     foundproblemrecords= j.foundproblemrecords
    #     datafpr.append(foundproblemrecords)
    #
    # for num in range(len(dodo)):
    #     id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(num)
    #     pp=Problems()
    #     pp.schemetype = id
    #     pp.checkobject=list1[num]
    #     pp.schemename=list2[num]
    #     pp.save()
    # dd_list=Problems.objects.get(schemename=dataash[0])
    # id = dd_list.id
    # dd2=Problems.objects.get(id=id)
    # dd2.problemrecords=datanr[0]
    # dd2.repairrecords=datafpr[0]
    # dd2.save()


    # for k in dd:
    #       newrecords = k.newrecords
    #       foundproblemrecords = k.foundproblemrecords



    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Problems.objects.filter(scheme_name=request.POST.get('condition')).count()
        data = Problems.objects.filter(scheme_name=request.POST.get('condition'))[start:end]
    else:
        counts = Problems.objects.all().count()
        data = Problems.objects.all()[start:end]
    list=[]
    for num in range(len(data)):
        temp = {
            'schemename':data[num].schemename,
            'checkobject':data[num].checkobject,
            'problemtable':data[num].problemtable,
            'problemrecords':data[num].problemrecords,
            'repairrecords':data[num].repairrecords,
            'id':data[num].id,
        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def wrong_request(request):
    print("0000")
    qqq = request.GET['data']
    myGlobal.dataWrongHierarchy=qqq
    print(qqq)
    print(myGlobal.dataWrongHierarchy)
    return render_to_response('problemData/wrong.html')

def wrong(request):
    return render_to_response('problemData/wrong.html')

def wrong_table(request):  
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = eval(str(myGlobal.dataWrongHierarchy) + ".objects.filter(schoolname=request.POST.get('condition')).count()")
        data = eval(str(myGlobal.dataWrongHierarchy) + ".objects.filter(schoolname=request.POST.get('condition'))[start:end]")
    else:
        counts = eval(str(myGlobal.dataWrongHierarchy) + ".objects.all().count()")
        data = eval(str(myGlobal.dataWrongHierarchy) + ".objects.all()[start:end]")
    list=[]
    for num in range(len(data)):
        temp = {
            'id':data[num].id,
            'schoolname':data[num].schoolname,
            'provideunit':data[num].provideunit,
            'datasource':data[num].datasource,
            'updatetime':data[num].updatetime ,       

        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def report(request):
    return render_to_response('problemData/report.html')


def report_table(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = Problems.objects.filter(scheme_name=request.POST.get('condition')).count()
        data = Problems.objects.filter(scheme_name=request.POST.get('condition'))[start:end]
    else:
        counts = Problems.objects.all().count()
        data = Problems.objects.all()[start:end]
    list=[]
    for num in range(len(data)):
        temp = {
            'scheme_type':data[num].schemetype,
            'scheme_name':data[num].schemename,
            'check_object':data[num].checkobject,
            'problem_records':data[num].problemrecords,
            'repair_records':data[num].repairrecords,
            'id':data[num].id,
        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def journal_request(request):
    print("0000")
    qqq = request.GET['data']
    myGlobal.dataWrongHierarchy2=qqq
    print(qqq)
    print(myGlobal.dataWrongHierarchy)
    return render_to_response('problemData/journal.html')

def journal(request):
    return render_to_response('problemData/journal.html')

def journal_table(request):  
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = eval(str(myGlobal.dataWrongHierarchy2) + ".objects.filter(schoolname=request.POST.get('condition')).count()")
        data = eval(str(myGlobal.dataWrongHierarchy2) + ".objects.filter(schoolname=request.POST.get('condition'))[start:end]")
    else:
        counts = eval(str(myGlobal.dataWrongHierarchy2) + ".objects.all().count()")
        data = eval(str(myGlobal.dataWrongHierarchy2) + ".objects.all()[start:end]")
    list=[]
    for num in range(len(data)):
        temp = {
            'id':data[num].id,
            'schoolname':data[num].schoolname,
            'provideunit':data[num].provideunit,
            'datasource':data[num].datasource,
            'updatetime':data[num].updatetime ,       

        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})



