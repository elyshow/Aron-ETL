from django.shortcuts import render

# Create your views here.
def getDataElementsList(request):
    page = int(request.POST.get('page')) 
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows
    if 'condition' in request.POST and request.POST.get('condition') != '':
        counts = dataElements.objects.filter(cn_name = request.POST.get('condition')).count()
        data = dataElements.objects.filter(cn_name=request.POST.get('condition'))[start:end]
    else:
        counts = dataElements.objects.all().count()
        data = dataElements.objects.all()[start:end]

    nlist = []
    fields = dataElements._meta.get_all_field_names()
    print(fields)
    for num in range(len(data)):
        temp = {}
        for t in range(len(fields)):
            temp[fields[t]] = getattr(data[num], fields[t])
        nlist.append(temp)

    return JsonResponse({'total': counts, 'rows': nlist})

def addDataElements(request):
    if request.method == 'POST':
        des = dataElements()
        #内部标识符是唯一键
        if 'internalid' in request.POST and request.POST.get('internalid') != '':
            data = des.objects.all()
            for num in range(len(data)):
                if getattr(data[num], 'internalid') != request.POST.get('internalid'):
                    des.internalid = request.POST.get('internalid')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '内部标识符重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '必须输入内部标识符'
                    })
        #中文名
        if 'cn_name' in request.POST and request.POST.get('cn_name') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入中文名'
                    })
        else:
            des.cn_name = request.POST.get('cn_name')
        #英文名
        if 'en_name' in request.POST and request.POST.get('en_name') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入英文名'
                    })
        else:
            des.en_name = request.POST.get('en_name')
        #全拼
        if 'cn_fullpinyin' in request.POST and request.POST.get('cn_fullpinyin') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入中文全拼'
                    })
        elif re.match('([a-z]+-)+[a-z]+$', request.POST.get('cn_fullpinyin')) != None:
            des.en_name = request.POST.get('cn_fullpinyin')
        else:
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '中文全拼正确格式为xxx-xxx-xxx'
                    })
        #标识符
        if 'identifier' in request.POST and request.POST.get('identifier') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入标识符'
                    })
        elif re.match('[A-Z]+', request.POST.get('identifier')) != None:
            des.identifier = request.POST.get('identifier')
        else:
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '标识符应为全英文大写'
                    })
        #语境
        des.context = request.POST.get('context')
        #版本
        des.version = request.POST.get('version')
        #同义名词
        des.synonyms = request.POST.get('synonyms')
        #说明
        des.comment = request.POST.get('comment')
        #对象类词
        des.objectwords = request.POST.get('objectwords')
        #特性词
        des.characteristicwords = request.POST.get('characteristicwords')
        #应用约束
        des.appconstraint = request.POST.get('appconstraint')
        #分类方案
        des.classifyplan = request.POST.get('classifyplan')
        #分类方案值
        des.classifyplanvalues = request.POST.get('classifyplanvalues')
        #关系
        des.relationship = request.POST.get('relationship')
        #表示词
        des.expressionwords = request.POST.get('expressionwords')
        #数据类型
        des.datatype = request.POST.get('datatype')
        #表示格式
        des.displayformat = request.POST.get('displayformat')
        #计量单位
        des.unit = request.POST.get('unit')
        #值域
        des.domain = request.POST.get('domain')
        #状态
        des.status = request.POST.get('status')
        #提交机构
        des.submitdepartement = request.POST.get('submitdepartement')
        #注册机构
        des.registrationdepartement = request.POST.get('registrationdepartement')
        #主要起草人
        des.mainwriter = request.POST.get('mainwriter')
        #批准日期
        des.approvaldate = request.POST.get('approvaldate')
        #备注
        des.notes = request.POST.get('notes')
        des.save()

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

def editDataElements(request):
    ID = request.POST.get('id')
    iDataElements = dataElements.objects.get(id = ID)

    if request.method == 'POST':
        #内部标识符
        if 'internalid' in request.POST and request.POST.get('internalid') != '':
            data = iDataElements.objects.exclude(id = ID)
            for num in range(len(data)):
                if getattr(data[num], 'internalid') != request.POST.get('internalid'):
                    iDataElements.internalid = request.POST.get('internalid')
                else:
                    return JsonResponse({
                        'errorCode': '0x0010',
                        'errorString': '内部标识符重复'
                        })
        else:
            return JsonResponse({
                    'errorCode': '0x0003',
                    'errorString': '必须输入内部标识符'
                    })
         #中文名
        if 'cn_name' in request.POST and request.POST.get('cn_name') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入中文名'
                    })
        else:
            des.cn_name = request.POST.get('cn_name')
        #英文名
        if 'en_name' in request.POST and request.POST.get('en_name') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入英文名'
                    })
        else:
            des.en_name = request.POST.get('en_name')
        #全拼
        if 'cn_fullpinyin' in request.POST and request.POST.get('cn_fullpinyin') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入中文全拼'
                    })
        elif re.match('([a-z]+-)+[a-z]+$', request.POST.get('cn_fullpinyin')) != None:
            des.en_name = request.POST.get('cn_fullpinyin')
        else:
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '中文全拼正确格式为xxx-xxx-xxx'
                    })
        #标识符
        if 'identifier' in request.POST and request.POST.get('identifier') == '':
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '必须输入标识符'
                    })
        elif re.match('[A-Z]+', request.POST.get('identifier')) != None:
            des.identifier = request.POST.get('identifier')
        else:
            return JsonResponse({
                    'errorCode': '0x0006',
                    'errorString': '标识符应为全英文大写'
                    })
        #语境
        des.context = request.POST.get('context')
        #版本
        des.version = request.POST.get('version')
        #同义名词
        des.synonyms = request.POST.get('synonyms')
        #说明
        des.comment = request.POST.get('comment')
        #对象类词
        des.objectwords = request.POST.get('objectwords')
        #特性词
        des.characteristicwords = request.POST.get('characteristicwords')
        #应用约束
        des.appconstraint = request.POST.get('appconstraint')
        #分类方案
        des.classifyplan = request.POST.get('classifyplan')
        #分类方案值
        des.classifyplanvalues = request.POST.get('classifyplanvalues')
        #关系
        des.relationship = request.POST.get('relationship')
        #表示词
        des.expressionwords = request.POST.get('expressionwords')
        #数据类型
        des.datatype = request.POST.get('datatype')
        #表示格式
        des.displayformat = request.POST.get('displayformat')
        #计量单位
        des.unit = request.POST.get('unit')
        #值域
        des.domain = request.POST.get('domain')
        #状态
        des.status = request.POST.get('status')
        #提交机构
        des.submitdepartement = request.POST.get('submitdepartement')
        #注册机构
        des.registrationdepartement = request.POST.get('registrationdepartement')
        #主要起草人
        des.mainwriter = request.POST.get('mainwriter')
        #批准日期
        des.approvaldate = request.POST.get('approvaldate')
        #备注
        des.notes = request.POST.get('notes')
        des.save()
    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

def deleteDataElements(request):
    IDs = request.POST.get('ids')
    dataElements.objects.extra(where=['id in (' + IDs + ')']).delete()

    return JsonResponse({
        'errorCode': '0x0000',
        'errorString': ''
    })

def getDataElementsCodeList(request):
    page = int(request.POST.get('page'))
    rows = int(request.POST.get('rows'))
    start = (page - 1) * rows
    end = page * rows

    counts = dataElementsCode.objects.all().count()
    data = dataElementsCode.objects.all()[start:end]
    nlist = []

    for num in range(len(data)):
        temp = {
        'id': getattr(data[num], 'id'),
        'code': getattr(data[num], 'code'),
        'name': getattr(data[num], 'name'),
        'notes': getattr(data[num], 'notes'),
        'dataelement': dataElements.objects.get(id = int(getattr(data[num], 'dataelement_id'))).cn_name
        }

        nlist.append(temp)
    return JsonResponse({'total': counts, 'rows': nlist})