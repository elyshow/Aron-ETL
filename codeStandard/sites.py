from django.shortcuts import render
import random,time
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from .models import DataStandard,StandardData,ComboBoxData,DataType
from releaseRegisterManagement.models import MasterdataTable,FieldTable
from .models import BusCode,StandardDataInfo,RecognInfo,DataBase
import json,pymysql
# Create your views here.


class codeStandardSite(object):
    def __init__(self, name='codeStandard'):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name

    def get_urls(self):
        from django.conf.urls import url, include

        urlpatterns = [
            url(r'^$', self.standardIndex, name="standardIndex"),
            url(r'^standardData/', self.standardData),
            url(r'^addStandardData/', self.addStandardData, name='addStandardData'),
            url(r'^delData/', self.delData),
            url(r'^recognizeData/', self.recognizeData),
            url(r'^Detail/', self.Detail),
            url(r'^comboboxData/', self.comboboxData),
            url(r'^insertStandard/', self.insertStandard),
            # 机构信息
            url(r'^recognizeIndex/$', self.recognizeIndex, name='recognizeIndex'),
            url(r'^recognizeIndex/recognAddData/', self.recognAddData),
            url(r'^recognizeIndex/recognInfo/', self.recognInfo),
            url(r'^recognizeIndex/recognDel/', self.recognDel),
            url(r'^recognizeIndex/checkData/', self.checkData),
            # 信息类型管理
            url(r'^dataTypeIndex/$', self.dataTypeIndex, name='dataTypeIndex'),
            url(r'^dataTypeIndex/typeData/', self.typeData),
            url(r'^dataTypeIndex/addInfoData/', self.addInfoData),
            url(r'^dataTypeIndex/dataDel/', self.dataDel),
            url(r'^dataTypeIndex/dataEdit/', self.dataEdit),
            # 业务代码管理
            url(r'^busCodeIndex/$', self.busCodeIndex, name='busCodeIndex'),
            url(r'^busCodeIndex/busCode/', self.busCode),
            url(r'^busCodeIndex/addBusCode/', self.addBusCode),
            url(r'^busCodeIndex/delBusCode/', self.delBusCode),
            # 数据库类型管理
            url(r'^databaseIndex/$', self.databaseIndex, name='databaseIndex'),
            url(r'^databaseIndex/getList/$', self.getList, name='getList'),
            url(r'^databaseIndex/saveList/$', self.saveList, name='saveList'),
            url(r'^databaseIndex/savechangeList/$', self.savechangeList, name='savechangeList'),
            url(r'^databaseIndex/delDbList/$', self.delDbList, name='delDbList'),
            # 标准代码管理
            url(r'^taskIndex/$', self.taskIndex, name='taskIndex'),
            url(r'^taskIndex/sjygl/', self.sjygl, name='sjygl'),
            url(r'^taskIndex/getDataList/', self.getDataList, name='getDataList'),
            url(r'^taskIndex/changeList/', self.changeList, name='changeList'),
            url(r'^taskIndex/save/', self.save, name='save'),
            url(r'^taskIndex/delList/', self.delList, name='delList'),
            url(r'^taskIndex/insertTable/', self.insertTable, name='insertTable'),
            url(r'^taskIndex/DetailTask/', self.DetailTask, name='DetailTask'),
            url(r'^taskIndex/detilList/', self.detilList, name='detilList'),

        ]

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), 'codeStandard', self.name

    def standardIndex(self, request):
        return render(request, 'codeStandard/standardIndex.html')

    #================================标准数据元管理================================

    def standardData(self, request):
        if not 'type' in request.POST:
            return JsonResponse({'errorCode': '0x0000', 'errorString': '参数错误'})
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            print(222222222222222222)
            counts = FieldTable.objects.filter(tabtype=request.POST.get('type'),
                                               identifier=request.POST.get('condition')).count()
            data = FieldTable.objects.filter(tabtype=request.POST.get('type'),
                                             identifier=request.POST.get('condition'))[start:end]
        else:
            counts = FieldTable.objects.filter(tabtype=request.POST.get('type')).count()
            data = FieldTable.objects.filter(tabtype=request.POST.get('type'))[start:end]
        list = []
        for num in range(len(data)):
            temp = {
                'cnname': data[num].cnname,
                'identifier': data[num].identifier,
                'object': data[num].object,
                'datatype': data[num].datatype,
                'standardsou': data[num].datafrom,
                'state': data[num].state,
                'id': data[num].id,
                'rule': data[num].rule,
            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def addStandardData(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        if request.POST.get('save_type') == 'add':
            rule = request.POST.get('Rule')
            insideIdenti = request.POST.get('insideIdentifier')
            cnName = request.POST.get('chineseName')
            cnSpell = request.POST.get('cn_spell')
            enName = request.POST.get('enName')
            identi = request.POST.get('identifier')
            language = request.POST.get('language')
            version = request.POST.get('version')
            samilarName = request.POST.get('samilarName')
            definIntro = request.POST.get('definedIntro')
            objBelong = request.POST.get('object')
            featureWord = request.POST.get('featureWord')
            constraint = request.POST.get('constraint')
            scheme = request.POST.get('scheme')
            schemeword = request.POST.get('schemeword')
            relation = request.POST.get('relation')
            meanWord = request.POST.get('showWord')
            dataType = request.POST.get('datatype')
            dataFormat = request.POST.get('dataFormat')
            valueRange = request.POST.get('valueRange')
            measUnit = request.POST.get('measurementUnit')
            subOrg = request.POST.get('subOrganization')
            regOrg = request.POST.get('regOrganization')
            writer = request.POST.get('draftsman')
            approvedDate = request.POST.get('approvedDate')
            quotdStandard = request.POST.get('quotdStandard')
            remark = request.POST.get('remark')
            state = rule
            if identi[0] >= 'A' and identi[0] <= 'D':  # 判断标识符所属分类
                type = '0'
            if identi[0] >= 'E' and identi[0] <= 'H':
                type = '1'
            if identi[0] >= 'I' and identi[0] <= 'L':
                type = '2'
            if identi[0] >= 'M' and identi[0] <= 'P':
                type = '3'
            if identi[0] >= 'Q' and identi[0] <= 'T':
                type = '4'
            if identi[0] >= 'U' and identi[0] <= 'Z':
                type = '5'
            sdi = FieldTable(rule=rule, identifier=identi,enname=enName,language=language,
                            inseridentifier=insideIdenti, samilarname=samilarName,
                            object=objBelong, feature=featureWord, relation=relation, impressword=meanWord,
                            datatype=dataType,constraint=constraint,dataformat=dataFormat,
                            valuerange=valueRange, measunit=measUnit, suborg=subOrg, mainwriter=writer,
                            introduce=definIntro,scheme=scheme,schemeword=schemeword,
                            approvedate=approvedDate, datafrom=quotdStandard, version=version, cnspell=cnSpell,
                            remark=remark, cnname=cnName,regorg=regOrg,
                            tabtype=type, state=rule)
            sdi.save()
        elif request.POST.get('save_type') == 'edit':
            id = request.POST.get('id')
            rule = request.POST.get('Rule')
            insideIdenti = request.POST.get('insideIdentifier')
            cnName = request.POST.get('chineseName')
            cnSpell = request.POST.get('cn_spell')
            enName = request.POST.get('enName')
            identi = request.POST.get('identifier')
            language = request.POST.get('language')
            version = request.POST.get('version')
            samilarName = request.POST.get('samilarName')
            definIntro = request.POST.get('definedIntro')
            objBelong = request.POST.get('object')
            featureWord = request.POST.get('featureWord')
            constraint = request.POST.get('constraint')
            scheme = request.POST.get('scheme')
            schemeword = request.POST.get('schemeword')
            relation = request.POST.get('relation')
            meanWord = request.POST.get('showWord')
            dataType = request.POST.get('datatype')
            dataFormat = request.POST.get('dataFormat')
            valueRange = request.POST.get('valueRange')
            measUnit = request.POST.get('measurementUnit')
            subOrg = request.POST.get('subOrganization')
            regOrg = request.POST.get('regOrganization')
            writer = request.POST.get('draftsman')
            approvedDate = request.POST.get('approvedDate')
            quotdStandard = request.POST.get('quotdStandard')
            remark = request.POST.get('remark')
            state = rule
            if identi[0] >= 'A' and identi[0] <= 'D':  # 判断标识符所属分类
                type = '0'
            if identi[0] >= 'E' and identi[0] <= 'H':
                type = '1'
            if identi[0] >= 'I' and identi[0] <= 'L':
                type = '2'
            if identi[0] >= 'M' and identi[0] <= 'P':
                type = '3'
            if identi[0] >= 'Q' and identi[0] <= 'T':
                type = '4'
            if identi[0] >= 'U' and identi[0] <= 'Z':
                type = '5'
            sdi = FieldTable(id=id,rule=rule, identifier=identi,enname=enName,language=language,
                            inseridentifier=insideIdenti, samilarname=samilarName,
                            object=objBelong, feature=featureWord, relation=relation, impressword=meanWord,
                            datatype=dataType,constraint=constraint,
                            valuerange=valueRange, measunit=measUnit, suborg=subOrg, mainwriter=writer,
                            introduce=definIntro,scheme=scheme,schemeword=schemeword,
                            approvedate=approvedDate, datafrom=dataFormat, version=version, cnspell=cnSpell,
                            remark=remark, cnname=cnName,regorg=regOrg,
                            tabtype=type, state=rule)
            sdi.save()
        return JsonResponse(result)

    # 删除数据
    def delData(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        cancel = request.POST.get('data')
        try:
            FieldTable.objects.extra(where=['id IN (' + cancel + ')']).delete()
        except:
            result['errorCode'] = '0x0001'
            result['errorString'] = '数据库操作失败'
        return JsonResponse(result)

    def recognizeData(self, request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = DataStandard.objects.filter(codetable=request.POST.get('condition')).count()
            data = DataStandard.objects.filter(codetable=request.POST.get('condition'))[start:end]
        else:
            counts = DataStandard.objects.all().count()
            data = DataStandard.objects.all()[start:end]
        list = []
        for num in range(len(data)):
            temp = {
                'codename': data[num].codename,
                'codetable': data[num].codetable,
                'datasource': data[num].datasource,

            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    #标准数据元管理详细信息
    def Detail(self, request):
        id = request.POST.get('data')
        detail_list = FieldTable.objects.filter(identifier=id)
        list = []
        for i in detail_list:
            temp = {
                'id': i.id,
                'rule': i.rule,
                'insertIdenti': i.inseridentifier,
                'identi': i.identifier,
                'samilarname': i.samilarname,
                'object': i.object,
                'feature': i.feature,
                'impressword': i.impressword,
                'datatype': i.datatype,
                'valuerange': i.valuerange,
                'meas_unit': i.measunit,
                'sub_recogn': i.suborg,
                'main_writer': i.mainwriter,
                'introduce': i.introduce,
                'approve_date': i.approvedate,
                'datafrom': i.dataformat,
                'version': i.version,
                'cn_spell': i.cnspell,
                'remark': i.remark,
                'cn_name': i.cnname,
                'state': i.state,
                'relation': i.relation,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

    def comboboxData(self, request):
        type = request.POST.get('type')
        list = []
        if type == '1':
            meanWord = ComboBoxData.objects.filter(type='1')
            for m in meanWord:
                temp = {
                    'value': m.value,
                    'cn_name': m.cnname,
                }
                list.append(temp)
        if type == '2':
            meanWord = ComboBoxData.objects.filter(type='2')
            for m in meanWord:
                temp = {
                    'value': m.value,
                    'cn_name': m.cnname,
                }
                list.append(temp)
        if type == '3':
            meanWord = ComboBoxData.objects.filter(type='3')
            for m in meanWord:
                temp = {
                    'value': m.value,
                    'cn_name': m.cnname,
                }
                list.append(temp)
        if type == '4':
            re_info = RecognInfo.objects.all()
            list = []
            for i in re_info:
                temp = {
                    'recognid': i.recognid,
                    'recognname': i.recognname,
                }
                list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

#=====================================机构信息===================================

    def recognize(self, request):
        re_info = RecognInfo.objects.all()
        list = []
        for i in re_info:
            temp = {
                'recognid': i.recognid,
                'recognname': i.recognname,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

    def recognizeIndex(self, request):
        return render(request, 'codeStandard/recognizeIndex.html')

    def recognAddData(self, request):
        # a = request.POST.get('save_type')
        result = {'errorCode': '0x0000', 'errorString': ''}
        if request.POST.get('save_type') == 'add':
            name = request.POST.get('recognName')
            number = request.POST.get('recognNumber')
            simpleName = request.POST.get('recognSimple')
            nature = request.POST.get('nature')
            re = RecognInfo(rid=str(random.random())[2:7], recognname=name, recognid=simpleName, recogntype=nature,
                            recognnumber=number)
            re.save()
        elif request.POST.get('save_type') == 'edit':
            id = request.POST.get('id')
            name = request.POST.get('recognName')
            number = request.POST.get('recognNumber')
            simpleName = request.POST.get('recognSimple')
            nature = request.POST.get('nature')
            re = RecognInfo(rid=id, recognname=name, recognid=simpleName, recogntype=nature, recognnumber=number)
            re.save()
        return JsonResponse(result)

    def recognInfo(self, request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = RecognInfo.objects.filter(recognname=request.POST.get('condition')).count()
            data = RecognInfo.objects.filter(recognname=request.POST.get('condition'))[start:end]
        else:
            counts = RecognInfo.objects.all().count()
            data = RecognInfo.objects.all()[start:end]
        list = []
        for num in range(len(data)):
            temp = {
                'simplename': data[num].recognid,
                'name': data[num].recognname,
                'nature': data[num].recogntype,
                'number': data[num].recognnumber,
                'id': data[num].rid,
            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def recognDel(self, request):
        result = {'errorCode': '0x0000', 'errorString': ''}
        cancel = request.POST.get('data')
        RecognInfo.objects.extra(where=['rid in (' + cancel + ')']).delete()
        return JsonResponse(result)

    def checkData(self, request):
        id = request.POST.get('data')
        recond = RecognInfo.objects.filter(rid=id)
        list = []
        for r in recond:
            temp = {
                'id': r.rid,
                'name': r.recognname,
                'recognid': r.recognid,
                'recogntype': r.recogntype,
                'recognNumber': r.recognnumber,

            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

#=================================信息类型管理=======================================

    def dataTypeIndex(self, request):
        return render(request, 'codeStandard/dataTypeIndex.html')

    def typeData(self, request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = DataType.objects.filter(dataname=request.POST.get('condition')).count()
            data = DataType.objects.filter(dataname=request.POST.get('condition'))[start:end]
        else:
            counts = DataType.objects.all().count()
            data = DataType.objects.all()[start:end]
        list = []
        for num in range(len(data)):
            temp = {
                'dataname': data[num].dataname,
                'mainword': data[num].mainword,
                'standardcode': data[num].standardcode,
                'classify': data[num].classify,
                'userecognize': data[num].userecognize,
                'id': data[num].dataid,

            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def addInfoData(self, request):
        if request.POST.get('save_type') == 'add':
            dataname = request.POST.get('dataname')
            mainWord = request.POST.get('mainWord')
            standardCode = request.POST.get('standardCode')
            classify = request.POST.get('classify')
            useRcognize = request.POST.get('useRcognize')
            dt = DataType()
            dt.dataid = str(random.random())[2:7]
            dt.dataname = dataname
            dt.mainword = mainWord
            dt.standardcode = standardCode
            dt.classify = classify
            dt.userecognize = useRcognize
            dt.save()
        elif request.POST.get('save_type') == 'edit':
            dataid = request.POST.get('dataid')
            dataname = request.POST.get('dataname')
            mainWord = request.POST.get('mainWord')
            standardCode = request.POST.get('standardCode')
            classify = request.POST.get('classify')
            useRcognize = request.POST.get('useRcognize')
            dt = DataType()
            dt.dataid = dataid
            dt.dataname = dataname
            dt.mainword = mainWord
            dt.standardcode = standardCode
            dt.classify = classify
            dt.userecognize = useRcognize
            dt.save()
        return JsonResponse({
                'errorCode': '0x0000',
                'errorString': ''
            })

    def dataDel(self, request):
        cancel = request.POST.get('data')
        DataType.objects.extra(where=['dataid in (' + cancel + ')']).delete()
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': ''
        })

    def dataEdit(self, request):
        id = request.POST.get('data')
        recond = DataType.objects.filter(dataid=id)
        list = []
        for r in recond:
            temp = {
                'dataname': r.dataname,
                'mainword': r.mainword,
                'standardcode': r.standardcode,
                'classify': r.classify,
                'userecognize': r.userecognize,
                'id': r.dataid,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

#===================================业务代码管理==================================

    def busCodeIndex(self, request):
        return render(request, 'codeStandard/busCodeIndex.html')

    def busCode(self, request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = BusCode.objects.filter(codetable=request.POST.get('condition')).count()
            data = BusCode.objects.filter(codetable=request.POST.get('condition'))[start:end]
        else:
            counts = BusCode.objects.all().count()
            data = BusCode.objects.all()[start:end]
        list = []
        for num in range(len(data)):
            temp = {
                'codeid': data[num].codeid,
                'codename': data[num].codename,
                'codetable': data[num].codetable,
                'busclass': data[num].busclass,
                'registertime': data[num].registertime,
            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def addBusCode(self, request):
        busCodename = request.POST['busCodeName']
        busCodetable = request.POST['busCodeTable']
        bu = BusCode()
        bu.registertime = time.strftime("%Y-%m-%d %X", time.localtime())
        bu.codename = busCodename
        bu.codetable = busCodetable
        bu.save()
        return HttpResponseRedirect('/standardIndex/busCodeIndex/')

    def delBusCode(self, request):
        stp = request.POST.get('data')
        BusCode.objects.extra(where=['codeid IN (' + stp + ')']).delete()
        return HttpResponseRedirect('/standardIndex/busCodeIndex/')

#==========================数据库类型管理==========================================

    def databaseIndex(self, request):
        return render(request, 'codeStandard/databaseIndex.html')

    def getList(self, request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = DataBase.objects.filter(type=request.POST.get('condition')).count()
            d_list = DataBase.objects.filter(type=request.POST.get('condition'))[start:end]
        else:
            d_list = DataBase.objects.all()[start:end]
            counts = DataBase.objects.all().count()
        list = []
        for i in range(len(d_list)):
            temp = {
                'id': d_list[i].id,
                'name': d_list[i].name,
                'type': d_list[i].type,
            }
            list.append(temp)
        return JsonResponse({'rows': list, 'total': counts})

    def saveList(self, request):
        name = request.POST.get('name')
        type = request.POST.get('type')
        st = DataBase()
        st.name = name
        st.type = type
        st.save()
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': ''
        })

    def savechangeList(self, request):
        id = request.POST.get('id')
        name = request.POST.get('name')
        type = request.POST.get('type')
        st = DataBase()
        st.id = id
        st.name = name
        st.type = type
        st.save()
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': ''
        })

    def delDbList(self, request):
        stp = request.POST.get('data')
        DataBase.objects.extra(where=['id IN (' + stp + ')']).delete()
        return HttpResponseRedirect('/standardIndex/databaseIndex/')

#===============================标准代码管理=================================

    def taskIndex(self, request):
        return render(request, 'codeStandard/taskIndex.html')


    # 下拉框读取数据库
    def sjygl(self, request):
        s_list = BusCode.objects.all()
        list = []
        for i in s_list:
            temp = {
                'codeid': i.codeid,
                'codename': i.codename,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

    def deleteTask(self, request):
        stp = request.POST.get('data')
        MasterdataTable.objects.extra(where=['id IN (' + stp + ')']).delete()
        return HttpResponseRedirect('/standardIndex/taskIndex/')

    def getDataList(self, request):
        if not 'type' in request.POST:
            return JsonResponse({'errorCode': '0x0000', 'errorString': '参数错误'})
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        b = request.POST.get('type')
        if 'condition' in request.POST and request.POST.get('condition') != '':
            counts = MasterdataTable.objects.filter(codestandardclass=request.POST.get('type'),
                                                 codename=request.POST.get('condition')).count()
            data = MasterdataTable.objects.filter(codestandardclass=request.POST.get('type'),
                                               codename=request.POST.get('condition'))[start:end]
        else:
            counts = MasterdataTable.objects.filter(codestandardclass=request.POST.get('type')).count()
            data = MasterdataTable.objects.filter(codestandardclass=request.POST.get('type'))[start:end]
        list = []
        for i in range(len(data)):
            temp = {
                'id': data[i].id,
                'codename': data[i].codename,
                'standardnum': data[i].standardnum,
                'codetable': data[i].codetable,
                'datasource': data[i].datasource,
                'registertime': data[i].registertime,
            }
            list.append(temp)
        if b == '0':
            if 'condition' in request.POST and request.POST.get('condition') != '':
                counts = MasterdataTable.objects.filter(codename=request.POST.get('condition')).count()
                data = MasterdataTable.objects.filter(codename=request.POST.get('condition'))[start:end]
            else:
                data = MasterdataTable.objects.all()[start:end]
                counts = MasterdataTable.objects.all().count()
            for i in range(len(data)):
                temp = {
                    'id': data[i].id,
                    'codename': data[i].codename,
                    'standardnum': data[i].standardnum,
                    'codetable': data[i].codetable,
                    'datasource': data[i].datasource,
                    'registertime': data[i].registertime,
                }
                list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

    def changeList(self, request):
        id = request.POST.get('data')
        s_list = MasterdataTable.objects.filter(id=id)
        list = []
        for i in s_list:
            temp = {
                'id': i.id,
                'codename': i.codename,
                'standardnum': i.standardnum,
                'codetable': i.codetable,
                'datasource': i.datasource,
                'structuretype': i.structuretype,
                'businessclass': i.businessclass,
                'codestandardclass': i.codestandardclass,
                'resourceproperty': i.resourceproperty,
                'other': i.other,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

    def save(self, request):
        if request.POST.get('save_type') == 'add':
            codename = request.POST.get('codename')
            standardnum = request.POST.get('standardnum')
            codetable = request.POST.get('codetable')
            datasource = request.POST.get('datasource')
            registertime = time.strftime("%Y-%m-%d %X", time.localtime())
            structuretype = request.POST.get('structuretype')
            businessclass = request.POST.get('businessclass')
            resourceproperty = request.POST.get('resourceproperty')
            codestandardclass = request.POST.get('codestandardclass')
            other = request.POST.get('other')
            st = MasterdataTable()
            st.id = str(random.random())[2:7]
            st.codename = codename
            st.standardnum = standardnum
            st.codetable = codetable
            st.datasource = datasource
            st.registertime = registertime
            st.structuretype = structuretype
            st.businessclass = businessclass
            st.resourceproperty = resourceproperty
            st.codestandardclass = codestandardclass
            st.other = other
            st.save()
        elif request.POST.get('save_type') == 'edit':
            id = request.POST.get('id')
            codename = request.POST.get('codename')
            standardnum = request.POST.get('standardnum')
            codetable = request.POST.get('codetable')
            datasource = request.POST.get('datasource')
            registertime = time.strftime("%Y-%m-%d %X", time.localtime())
            structuretype = request.POST.get('structuretype')
            businessclass = request.POST.get('businessclass')
            resourceproperty = request.POST.get('resourceproperty')
            codestandardclass = request.POST.get('codestandardclass')
            other = request.POST.get('other')
            st = MasterdataTable()
            st.id = id
            st.codename = codename
            st.standardnum = standardnum
            st.codetable = codetable
            st.datasource = datasource
            st.registertime = registertime
            st.structuretype = structuretype
            st.businessclass = businessclass
            st.resourceproperty = resourceproperty
            st.codestandardclass = codestandardclass
            st.other = other
            st.save()
        return JsonResponse({
            'errorCode': '0x0000',
            'errorString': ''
        })

    def delList(self, request):
        stp = request.POST.get('data')
        MasterdataTable.objects.extra(where=['id IN (' + stp + ')']).delete()
        return HttpResponseRedirect("/standardIndex/taskIndex/")

    def insertTable(self, request):
        dodo = MasterdataTable.objects.all()
        ds = DataStandard.objects.all()
        for i in dodo:
            a = 0
            for j in ds:
                if i.tablechinese == j.codename:
                    a = 1
                    break
            if a == 0:
                tableenglish = i.tableenglish,
                tablechinese = i.tablechinese,
                tableid = i.tableid,
                source = i.source,
                remark = i.remark
                stt = DataStandard()
                stt.id = str(random.random())[2:7]
                stt.codename = tablechinese[0]
                stt.codetable = tableenglish[0]
                stt.standardnum = tableid[0]
                stt.datasource = source[0]
                stt.type = remark[0]
                stt.registertime = time.strftime("%Y-%m-%d %X", time.localtime())
                stt.codestandardclass = 2
                stt.save()
        return HttpResponseRedirect("/standardIndex/taskIndex/")

    def insertStandard(self, request):
        com = FieldTable.objects.all()
        dy = StandardDataInfo.objects.all()
        for i in com:
            a = 0
            for j in dy:
                if i.fieldchinese == j.cnname:
                    a = 1
                    break
            if a == 0:
                tablechinese = i.tablechinese,
                showtype = i.showtype,
                source = i.source,
                remark = i.remark,
                fieldenglish0 = i.fieldenglish[0]
                fieldenglish = i.fieldenglish
                fieldchinese = i.fieldchinese
                tableenglish = i.tableenglish
                stt = StandardDataInfo()
                stt.cnname = fieldchinese
                stt.identifier = fieldenglish
                stt.object = tablechinese[0]
                stt.datatype = showtype[0]
                stt.datafrom = source[0]
                stt.remark = remark[0]
                stt.rule = '2'
                stt.inseridentifier = tableenglish
                stt.state = '标准'
                if fieldenglish0 >= 'A' and fieldenglish0 <= 'D':  # 判断标识符所属分类
                    stt.tabtype = '0'
                if fieldenglish0 >= 'E' and fieldenglish0 <= 'H':
                    stt.tabtype = '1'
                if fieldenglish0 >= 'I' and fieldenglish0 <= 'L':
                    stt.tabtype = '2'
                if fieldenglish0 >= 'M' and fieldenglish0 <= 'P':
                    stt.tabtype = '3'
                if fieldenglish0 >= 'Q' and fieldenglish0 <= 'T':
                    stt.tabtype = '4'
                if fieldenglish0 >= 'U' and fieldenglish0 <= 'Z':
                    stt.tabtype = '5'
                stt.save()
        return HttpResponseRedirect("/standardIndex/")

    def DetailTask(self, request):
        id = request.POST.get('datas')
        ds = MasterdataTable.objects.get(id=id)
        dsbus = ds.businessclass
        b_list = BusCode.objects.all()
        for i in b_list:
            if i.codeid == int(dsbus):
                codename = i.codename
                print(i.codename)
        bs = MasterdataTable.objects.filter(id=id)
        list = []
        for b in bs:
            temp = {
                'codenameDetail': b.codename,
                'standardnumDetail': b.standardnum,
                'codetableDetail': b.codetable,
                'datasourceDetail': b.datasource,
                'registertimeDetail': b.registertime,
                'businessclassDetail':codename,
                'codestandardclassDetail': b.codestandardclass,
                'structuretypeDetail': b.structuretype,
            }
            list.append(temp)
        return HttpResponse(json.dumps(list), content_type='application/json')

    def detilList(self, request):
        page = int(request.POST.get('page'))
        rows = int(request.POST.get('rows'))
        start = (page - 1) * rows
        end = page * rows
        counts = FieldTable.objects.filter(inseridentifier=request.POST.get('data')).count()
        data = FieldTable.objects.filter(inseridentifier=request.POST.get('data'))[start:end]
        list = []
        print(1111111111)
        print(data)
        for i in range(len(data)):
            temp = {
                'rule': data[i].rule,
                'identifier': data[i].identifier,
                'inseridentifier': data[i].inseridentifier,
                'object': data[i].object,
                'datatype': data[i].datatype,
                'datafrom': data[i].datafrom,
                'remark': data[i].remark,
                'cnname': data[i].cnname,
                'state': data[i].state,
                'tabtype': data[i].tabtype
            }
            list.append(temp)
        return JsonResponse({'total': counts, 'rows': list})

site = codeStandardSite()