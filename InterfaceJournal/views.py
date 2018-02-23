from django.shortcuts import render, render_to_response
from django.http.response import HttpResponse
from cataloguedataway.models import InterfacejournalProtslog
import json
from django.http import JsonResponse

def journallog(request):
    return render_to_response('InterfaceJournal/journal.html')

def journal_tablelog(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST:
        counts = InterfacejournalProtslog.objects.order_by('-id').filter(apiID__icontains=request.POST.get('condition')).count()
        data = InterfacejournalProtslog.objects.order_by('-id').filter(apiID__icontains=request.POST.get('condition'))[start:end]
    else:
        counts = InterfacejournalProtslog.objects.order_by('-id').all().count()
        data = InterfacejournalProtslog.objects.order_by('-id').all()[start:end]
    list=[]
    for num in range(len(data)):
        temp = {
            'id':data[num].id,
            'username':data[num].username,
            'apiID':data[num].apiid,
            'data':data[num].data,
            'requesttime':data[num].requesttime,
            'returnvalue':data[num].returnvalue,
            'returntime':data[num].returntime,
        }
        list.append(temp)
    return JsonResponse({'total':counts,'rows':list})

def journal_dialog(request):
    print(111)
    id = request.GET['datas']
    print (id)
    ds = InterfacejournalProtslog.objects.get(id=id)
    print(ds)
    list = []

    temp = {
        'id':ds.id,
        'username':ds.username,
        'password':ds.password,
        'apiID':ds.apiID,
        'data':ds.data,
        'requesttime':ds.requesttime,
        'returnvalue':ds.returnvalue,
        'returntime':ds.returntime,
    }
    list.append(temp)
    print(list)
    return HttpResponse(json.dumps(list), content_type='application/json')





