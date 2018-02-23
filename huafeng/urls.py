"""huafeng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from dataCleaning import sites as cleanup_sites
from dataCleaningRules import sites as cleanRule_sites
from codeStandard import sites as codeStandard_sites

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'home.views.index', name="homeIndex"),

# 数据清洗
    # 数据清洗
    url(r'^dataCleaning/', include(cleanup_sites.site.urls)),
    # 数据清洗规则
    url(r'^dataCleaningRules/', include(cleanRule_sites.site.urls)),
    #数据管理
    url(r'^standardIndex/', include(codeStandard_sites.site.urls)),

# 新版数据采集
    url(r'^dataCollect/', include('dataCollect.urls')),

#数据采集
    # 采集节点相关
    url(r'^cjjdglIndex/$', 'taskApp.views.cjjdglIndex', name='cjjdglIndex'),
    url(r'^cjjdglIndex/cjjdgl/', 'taskApp.views.cjjdgl',name='getCollectNodeList'),
    url(r'^cjjdglIndex/cjjdglDel/', 'taskApp.views.cjjdglDel', name='cjjdglDel'),
    url(r'^cjjdglIndex/addjdTask/', 'taskApp.views.addjdTask', name='addjdtask'),
    url(r'^cjjdglIndex/domSearch/', 'taskApp.views.domSearch', name='domSearch'),
    url(r'^cjjdglIndex/changeDom/', 'taskApp.views.changeDom',name='changeDom'),
    # 采集任务相关
    url(r'^sjyglIndex/$', 'taskApp.views.sjyglIndex', name='sjyglIndex'),
    url(r'^sjyglIndex/newSjygl/', 'taskApp.views.newSjygl', name='newSjygl'),
    url(r'^sjyglIndex/sjygl/', 'taskApp.views.sjygl', name='sjygl'),
    url(r'^sjyglIndex/sjyglDel/', 'taskApp.views.sjyglDel', name='sjyglDel'),
    # 查看采集日志
    url(r'^collectLogIndex/$', 'taskApp.views.collectLogIndex', name='collectLogIndex'),
    url(r'^collectLogIndex/collection/', 'taskApp.views.collection', name='collection'),
    # 新加采集任务
    url(r'^taskTypeDialog/$', 'taskType.views.taskTypeDialog'),
    url(r'^taskType/getContent/(?P<type>\w+)/', 'taskType.views.tabs'),
    url(r'^taskTypeDialog/dataInterDialog/', 'taskType.views.dataInterDialog'),
    url(r'^taskTypeDialog/taskDownloadDialog/', 'taskType.views.taskDownloadDialog'),
    url(r'^taskTypeDialog/taskSqlDialog/', 'taskType.views.taskSqlDialog'),
    url(r'^taskTypeDialog/tableToDialog/', 'taskType.views.tableToDialog'),
    url(r'^taskTypeDialog/fieldToDialog/', 'taskType.views.fieldToDialog'),
    url(r'^taskTypeDialog/dataApiDialog/', 'taskType.views.dataApiDialog'),
    url(r'^taskTypeDialog/stateStop/', 'taskType.views.stateStop'),
    url(r'^taskTypeDialog/stateStart/', 'taskType.views.stateStart'),
    url(r'^taskTypeDialog/runNow/', 'taskType.views.runNow'),
    url(r'^taskTypeDialog/xiugai/', 'taskType.views.xiugai', name='xiugai'),
    url(r'^taskTypeDialog/sjyglDb/', 'taskType.views.sjyglDb', name='sjyglDb'),
    url(r'^taskTypeDialog/dataIncrement/', 'taskType.views.dataIncrement', name='dataIncrement'),
    url(r'^taskTypeDialog/tasknameTest/', 'taskType.views.tasknameTest', name='tasknameTest'),
    # 测试
    url(r'^taskTypeDialog/dataTest/', 'taskType.views.dataTest'),
    # 定时任务执行
    url(r'^getData/', 'taskType.views.getData',name='getData'),
    # 修改
    url(r'^sjyglIndex/taskInfo/', 'taskApp.views.taskInfo', name='taskInfo'),
    url(r'^sjyglIndex/updateData/', 'taskApp.views.updateData', name='updateData'),
    url(r'^sjyglIndex/testConn/', 'taskApp.views.testConn', name='testConn'),
    url(r'^sjyglIndex/sjyglBelongto/', 'taskApp.views.sjyglBelongto', name='sjyglBelongto'),
    url(r'^sjyglIndex/sjyglBelongType/', 'taskApp.views.sjyglBelongType', name='sjyglBelongType'),
    url(r'^sjyglIndex/updataRefesh/', 'taskApp.views.updataRefesh', name='updataRefesh'),
    # 查看采集日志
    url(r'^collectLogIndex/$', 'taskApp.views.collectLogIndex', name='collectLogIndex'),
    url(r'^collectLogIndex/collection/', 'taskApp.views.collection', name='collection'),


#数据标准管理
    # url(r'^standardIndex/$', 'codeStandard.views.standardIndex', name="standardIndex"),
    # url(r'^standardIndex/standardData/', 'codeStandard.views.standardData'),
    # url(r'^standardIndex/addStandardData/', 'codeStandard.views.addStandardData',name='addStandardData'),
    # url(r'^standardIndex/delData/', 'codeStandard.views.delData'),
    # url(r'^standardIndex/recognizeData/', 'codeStandard.views.recognizeData'),
    # url(r'^standardIndex/Detail/', 'codeStandard.views.Detail'),
    # url(r'^standardIndex/comboboxData/', 'codeStandard.views.comboboxData'),
    # url(r'^standardIndex/insertStandard/', 'codeStandard.views.insertStandard'),
    # #机构信息
    # url(r'^recognizeIndex/$', 'codeStandard.views.recognizeIndex', name='recognizeIndex'),
    # url(r'^recognizeIndex/recognAddData/', 'codeStandard.views.recognAddData'),
    # url(r'^recognizeIndex/recognInfo/', 'codeStandard.views.recognInfo'),
    # url(r'^recognizeIndex/recognDel/', 'codeStandard.views.recognDel'),
    # url(r'^recognizeIndex/checkData/', 'codeStandard.views.checkData'),
    # #信息类型管理
    # url(r'^dataTypeIndex/$', 'codeStandard.views.dataTypeIndex', name='dataTypeIndex'),
    # url(r'^dataTypeIndex/typeData/', 'codeStandard.views.typeData'),
    # url(r'^dataTypeIndex/addInfoData/', 'codeStandard.views.addInfoData'),
    # url(r'^dataTypeIndex/dataDel/', 'codeStandard.views.dataDel'),
    # url(r'^dataTypeIndex/dataEdit/', 'codeStandard.views.dataEdit'),
    # #业务代码管理
    # url(r'^busCodeIndex/$', 'codeStandard.views.busCodeIndex', name='busCodeIndex'),
    # url(r'^busCodeIndex/busCode/', 'codeStandard.views.busCode'),
    # url(r'^busCodeIndex/addBusCode/', 'codeStandard.views.addBusCode'),
    # url(r'^busCodeIndex/delBusCode/', 'codeStandard.views.delBusCode'),
    # #数据库类型管理
    # url(r'^databaseIndex/$', 'codeStandard.views.databaseIndex', name='databaseIndex'),
    # url(r'^databaseIndex/getList/$', 'codeStandard.views.getList', name='getList'),
    # url(r'^databaseIndex/saveList/$', 'codeStandard.views.saveList', name='saveList'),
    # url(r'^databaseIndex/savechangeList/$', 'codeStandard.views.savechangeList', name='savechangeList'),
    # url(r'^databaseIndex/delDbList/$', 'codeStandard.views.delDbList', name='delDbList'),
    # # 标准代码管理
    # url(r'^taskIndex/$', 'codeStandard.views.taskIndex', name='taskIndex'),
    # url(r'^taskIndex/sjygl/', 'codeStandard.views.sjygl', name='sjygl'),
    # url(r'^taskIndex/getDataList/', 'codeStandard.views.getDataList', name='getDataList'),
    # url(r'^taskIndex/changeList/', 'codeStandard.views.changeList', name='changeList'),
    # url(r'^taskIndex/save/', 'codeStandard.views.save', name='save'),
    # url(r'^taskIndex/delList/', 'codeStandard.views.delList', name='delList'),
    # url(r'^taskIndex/insertTable/', 'codeStandard.views.insertTable', name='insertTable'),
    # url(r'^taskIndex/DetailTask/', 'codeStandard.views.DetailTask', name='DetailTask'),
    # url(r'^taskIndex/detilList/', 'codeStandard.views.detilList', name='detilList'),
    # 可访问接口
    # url(r'^getCollectTable/', 'taskApp.views.getCollectTable', name='getCollectTable'),

# 数据监控统计
    url(r'^huafeng/shujujiankong/$', 'shujujiankong.views.dataMonitoringStatistics', name='dataMonitoringStatistics'),
    # 数据监控统计主页面获取后台数据库数据的方法的URL
    url(r'^huafeng/getData/$', 'shujujiankong.views.getData', name='getData'),
    url(r'^huafeng/getData1/$', 'shujujiankong.views.getData1', name='getData1'),
    # 数据监控统计中点击主页面后的“二级页面”后台数据库数据的URL
    url(r'^huafeng/getData5/$', 'shujujiankong.views.getData5', name='getData5'),
    # 当点击“主页面”的第一行时跳转到新页面的方法的URL
    url(r'^huafeng/secondPage/$', 'shujujiankong.views.secondPage', name='secondPage'),
    # 数据监控统计的url
    url(r'^huafeng/returnBack/(?P<tabIndex>\d+)$', 'shujujiankong.views.returnBack', name='returnBack'),
    url(r'^huafeng/biaozhunku_request/', 'shujujiankong.views.biaozhunku_request', name='biaozhunku_request'),

#数据资源管理
    #编目管理
    url(r'^catalogueManagement/index/$', 'catalogueManagement.views.index', name="catalogManagementIndex"),
    url(r'^catalogueManagement/getCatalogueManagementTree/', 'catalogueManagement.views.getData', name='getCatalogueManagementTree'),
    url(r'^catalogueManagement/saveCleaningRules/', 'catalogueManagement.views.saveCleaningRules'),
    url(r'^catalogueManagement/delCleaningRules/', 'catalogueManagement.views.delCleaningRules'),
    url(r'^catalogueManagement/allData/', 'catalogueManagement.views.allData'),
    #注册发布管理
    url(r'^releaseRegister/index/$', 'releaseRegisterManagement.views.index', name="releaseRegisterIndex"),
    url(r'^releaseRegister/getUnRegisterDataList/', 'releaseRegisterManagement.views.unregisterIndex', name="getUnRegisterDataList"),
    url(r'^releaseRegister/getResourceTreeData/', 'releaseRegisterManagement.views.getTreeData', name="getResourceTreeData"),
    url(r'^releaseRegister/getRegisterTableFieldList/', 'releaseRegisterManagement.views.dragData', name='getRegisterTableFieldList'),
    url(r'^releaseRegister/dragData2/', 'releaseRegisterManagement.views.dragData2'),
    url(r'^releaseRegisterManagement/saveRegisterResource/', 'releaseRegisterManagement.views.saveCleaningRules', name='saveRegisterResource'),
    url(r'^releaseRegister/getRegisterDataList/', 'releaseRegisterManagement.views.registerIndex', name='getRegisterDataList'),
    url(r'^releaseRegister/PublishResource/', 'releaseRegisterManagement.views.release', name='PublishResource'),
    url(r'^releaseRegister/getPublishDataList/', 'releaseRegisterManagement.views.releaseIndex', name='getPublishDataList'),
    url(r'^releaseRegister/remokeRegisterResource/', 'releaseRegisterManagement.views.registerCancel', name='remokeRegisterResource'),
    url(r'^releaseRegister/remokePublishResource/', 'releaseRegisterManagement.views.fabuCancel', name='remokePublishResource'),

# 数据概况
    url(r'^huafeng/dataprofile/$','dataProfile.views.dataprofile', name='dataprofile'),
    url(r'^catalogue1/(?P<typeid>\d+)','dataProfile.views.catalogue1', name='catalogue1'),
    url(r'^huafeng/catalogue1_table/$','dataProfile.views.catalogue1_table', name='catalogue1_table'),
    url(r'^huafeng/catalogue2_table/$','dataProfile.views.catalogue2_table', name='catalogue2_table'),
    url(r'^huafeng/catalogue2_request/','dataProfile.views.catalogue2_request', name='catalogue2_request'),
    url(r'^huafeng/catalogue2/','dataProfile.views.catalogue2', name='catalogue2'),
    url(r'^huafeng/table_request/','dataProfile.views.table_request', name='table_request'),
    url(r'^huafeng/table/','dataProfile.views.table', name='table'),
    url(r'^huafeng/table_table/$','dataProfile.views.table_table', name='table_table'),
    url(r'^huafeng/detailed_request/','dataProfile.views.detailed_request', name='detailed_request'),
    url(r'^huafeng/detailed/','dataProfile.views.detailed', name='detailed'),
    url(r'^dataProfile/getResourceAttr/','dataProfile.views.getResourceAttr', name='getResourceAttr'),
    url(r'^dataProfile/getResourceField/','dataProfile.views.getResourceField', name='getResourceField'),

# 数据质量监测管理
    url(r'^dataQualityManagement/index/', 'dataQualityManagement.views.index', name='dataQualityManagementIndex'),
    url(r'^table1/showData/$', 'dataQualityManagement.views.showData', name='showData '),
    url(r'^table1/addData/$', 'dataQualityManagement.views.addData', name='addData '),
    url(r'^table1/delData/$', 'dataQualityManagement.views.delData', name='delData '),
    url(r'^table1/changeMet/$', 'dataQualityManagement.views.changeMet', name='changeMet '),
    url(r'^parameters/loadList/$', 'dataQualityManagement.views.loadList', name='loadList '),
    url(r'^parameters/loadList2/$', 'dataQualityManagement.views.loadList2', name='loadList2 '),

    url(r'^table2/showData2/$', 'dataQualityManagement.views.showData2', name='showData2 '),
    url(r'^table2/addData2/$', 'dataQualityManagement.views.addData2', name='addData2 '),
    url(r'^table2/delData2/$', 'dataQualityManagement.views.delData2', name='delData2 '),
    url(r'^table2/changeRul/$', 'dataQualityManagement.views.changeRul', name='changeRul '),
    url(r'^parameters/loadList21/$', 'dataQualityManagement.views.loadList21', name='loadList21 '),

    url(r'^table3/showData3/$', 'dataQualityManagement.views.showData3', name='showData3 '),
    url(r'^table3/delData3/$', 'dataQualityManagement.views.delData3', name='delData3 '),
    url(r'^table3/changeBas/$', 'dataQualityManagement.views.changeBas', name='changeBas '),
    # 新增监测方案
    url(r'^baseschedum/$', 'dataQualityManagement.views.baseschedum', name='baseschedum'),
    url(r'^baseschedum/add/', 'dataQualityManagement.views.add', name='add'),
    url(r'^table5/showData5/$', 'dataQualityManagement.views.showData5', name='showData5 '),
    url(r'^table5/changeRul/$', 'dataQualityManagement.views.changeRul', name='changeRul '),
    url(r'^table5/stateStop/', 'dataQualityManagement.views.stateStop'),
    url(r'^table5/stateStart/', 'dataQualityManagement.views.stateStart'),
    url(r'^table5/runNow/', 'dataQualityManagement.views.runNow'),
    url(r'^table5/changeTas/', 'dataQualityManagement.views.changeTas', name='changeTas'),
    url(r'^table5/addData5/', 'dataQualityManagement.views.addData5', name='addData5'),
    url(r'^table5/delData5/', 'dataQualityManagement.views.delData5', name='delData5'),
    url(r'^table6/delData6/', 'dataQualityManagement.views.delData6', name='delData6'),
    url(r'^table6/deData6/', 'dataQualityManagement.views.deData6', name='deData6'),
    # 查看监测日志
    url(r'^logList/$', 'dataQualityManagement.views.logList', name='logList'),
    url(r'^logList/loadList6/', 'dataQualityManagement.views.loadList6', name='loadList6'),
    # 数据质量评估的url
    url(r'^dataQualityAssessment/index/', 'dataQualityAssessment.views.index',name='dataQualityAssessmentIndex'),
    url(r'^Assess/showData/$', 'dataQualityAssessment.views.showData', name='showData '),
    url(r'^Assess/addData/$', 'dataQualityAssessment.views.addData', name='addData '),
    url(r'^Assess/delData/$', 'dataQualityAssessment.views.delData', name='delData '),
    url(r'^Assess/changeMet/$', 'dataQualityAssessment.views.changeMet', name='changeMet '),
    url(r'^Logassessment/loadList/$', 'dataQualityAssessment.views.loadList', name='loadList '),
    url(r'^Result/loadList2/$', 'dataQualityAssessment.views.loadList2', name='loadList2 '),
    url(r'^assess/runNow3/$', 'dataQualityAssessment.views.runNow3', name='runNow3 '),
    url(r'^assess/delData02/$', 'dataQualityAssessment.views.delData02', name='delData02 '),
    # 问题数据管理
    url(r'^huafeng/question/','problemData.views.question', name='question'),
    url(r'^huafeng/question_table/$','problemData.views.question_table', name='question_table'),
    url(r'^huafeng/wrong_request/','problemData.views.wrong_request', name='wrong_request'),
    url(r'^huafeng/wrong/','problemData.views.wrong', name='wrong'),
    url(r'^huafeng/wrong_table/','problemData.views.wrong_table', name='wrong_table'),
    url(r'^huafeng/report/','problemData.views.report', name='report'),
    url(r'^huafeng/report_table/$','problemData.views.report_table', name='report_table'),
    url(r'^huafeng/journal_request/','problemData.views.journal_request', name='journal_request'),
    url(r'^huafeng/journal/','problemData.views.journal', name='journal'),
    url(r'^huafeng/journal_table/','problemData.views.journal_table', name='journal_table'),

#数据总线
    #数据目录
    url(r'^cataloguedataway/index/$', 'cataloguedataway.views.index'),
    url(r'^cataloguedataway/getData/$', 'cataloguedataway.views.getData'),
    url(r'^cataloguedataway/saveCleaningRules/$', 'cataloguedataway.views.saveCleaningRules'),
    url(r'^cataloguedataway/delCleaningRules/$', 'cataloguedataway.views.delCleaningRules'),
    url(r'^cataloguedataway/allData/$', 'cataloguedataway.views.allData'),
    #数据配置
    url(r'^dataway/index/', 'dataway.views.index', name='datawayIndex'),
    url(r'^dataway/showData/$', 'dataway.views.showData', name='showData '),
    url(r'^dataway/delData/$', 'dataway.views.delData', name='delData '),
    url(r'^dataway/datawayfield/$', 'dataway.views.datawayfield',name='datawayfield'),
    url(r'^dataway/datawaycondition/$', 'dataway.views.datawaycondition', name='datawaycondition'),
    url(r'^dataway/dragData/$', 'dataway.views.dragData', name='dragData'),
    url(r'^dataway/saveData/$', 'dataway.views.saveData', name='saveData'),
    url(r'^dataway/catalogue/$', 'dataway.views.catalogue', name='catalogue'),
    url(r'^dataway/compareData/$', 'dataway.views.compareData', name='compareData'), # 数据比对接口
    #接口测试
    url(r'^dataway/csindex/(?P<idapi>\w+)/$', 'dataway.views.csindex', name='csindex'),
    url(r'^dataway/resourceSharing/$', 'dataway.views.resourceSharing', name='resourceSharing'),
    url(r'^dataway/csdef/$', 'dataway.views.csdef', name='csdef'),
    # 数据接口浏览
    url(r'^huafeng/interface/$','InterfaceCatalogue.views.interface', name='interface'),
    url(r'^interfacecatalogue1/(?P<typeid>\d+)','InterfaceCatalogue.views.interfacecatalogue1', name='interfacecatalogue1'),
    url(r'^huafeng/interfacecatalogue1_table/$','InterfaceCatalogue.views.interfacecatalogue1_table', name='interfacecatalogue1_table'),
    url(r'^huafeng/interfacecatalogue2_table/$','InterfaceCatalogue.views.interfacecatalogue2_table', name='interfacecatalogue2_table'),
    url(r'^huafeng/interfacecatalogue2_request/','InterfaceCatalogue.views.interfacecatalogue2_request', name='interfacecatalogue2_request'),
    url(r'^huafeng/interfacecatalogue2/','InterfaceCatalogue.views.interfacecatalogue2', name='interfacecatalogue2'),
    url(r'^huafeng/interfacetable_request/','InterfaceCatalogue.views.interfacetable_request', name='interfacetable_request'),
    url(r'^huafeng/interfacetable/','InterfaceCatalogue.views.interfacetable', name='interfacetable'),
    url(r'^huafeng/interfacetable_table/$','InterfaceCatalogue.views.interfacetable_table', name='interfacetable_table'),
    url(r'^huafeng/interfacedetailed_request/','InterfaceCatalogue.views.interfacedetailed_request', name='interfacedetailed_request'),
    url(r'^huafeng/interfacedetailed/','InterfaceCatalogue.views.interfacedetailed', name='interfacedetailed'),
    url(r'^huafeng/interfacetable_index/$','InterfaceCatalogue.views.interfacetable_index', name='interfacetable_index'),
    url(r'^huafeng/condition_request/','InterfaceCatalogue.views.condition_request', name='condition_request'),
    url(r'^huafeng/condition/','InterfaceCatalogue.views.condition', name='condition'),
    url(r'^huafeng/condition_table/$','InterfaceCatalogue.views.condition_table', name='condition_table'),
    # 接口日志
    url(r'^huafeng/journallog/$','InterfaceJournal.views.journallog', name='journallog'),
    url(r'^huafeng/journal_tablelog/$','InterfaceJournal.views.journal_tablelog', name='journal_tablelog'),
    url(r'^huafeng/journal_dialog/$','InterfaceJournal.views.journal_dialog', name='journal_dialog'),


# 登录和鉴权
    # url(r'^login/', 'user.views.login', name='login'),
    # url(r'^startlogin/', 'user.views.startlogin', name='startlogin'),
    # url(r'^loginout/', 'user.views.loginout', name='loginout'),
    # url(r'^userIndex/$', 'user.views.userIndex', name='userIndex'),
    # url(r'^userIndex/getTreeData/', 'user.views.getTreeData', name='getTreeData'),
    # url(r'^userIndex/passTreeData/', 'user.views.passTreeData', name='passTreeData'),
    # url(r'^userIndex/userInfo/', 'user.views.userInfo', name='userInfo'),
    # url(r'^userIndex/userDel/', 'user.views.userDel', name='userDel'),
    # url(r'^userIndex/recognCombobox/', 'user.views.recognCombobox', name='recognCombobox'),
    # url(r'^userIndex/userInfoSave/', 'user.views.userInfoSave', name='userInfoSave'),
	url(r'^', include('UserManage.urls')),

#数据监控
    url(r'^', include('dataQualityManagement.urls')),

    
]
