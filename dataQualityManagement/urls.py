from django.conf.urls import url
from dataQualityManagement import views

urlpatterns = [

    # 检验方法管理
    url(r'^dataQualityManagement/getMethodList/$', views.getMethodList, name='getMethodList'),
    url(r'^dataQualityManagement/method_save/$', views.method_save, name='method_save'),
    url(r'^dataQualityManagement/method_delete/$', views.method_delete, name='method_delete'),
	
	#常用规则设置
	url(r'^oftenRules/getRulesList/$', views.oftenRules_getRulesList, name='RulesGetRulesList'),
    url(r'^oftenRules/save/$', views.oftenRules_save, name='RulesSave'),
    url(r'^oftenRules/delete/$', views.oftenRules_delete, name='RulesDelete'),
    
    url(r'^oftenRules/getObject/$', views.getObject, name='getObject'),
    url(r'^oftenRules/getFieldTable/$', views.getFieldTable, name='getFieldTable'),
    url(r'^oftenRules/getcnname/$', views.getcnname, name='getcnname'),

    url(r'^oftenRules/getTestMethod/$', views.getTestMethod, name='getTestMethod'),
    url(r'^oftenRules/getCheckRule/$', views.getCheckRule, name='getCheckRule'),
    url(r'^oftenRules/getFieldList/$', views.getFieldList, name='getFieldList'),

#------------------------------------方国巍----------------------------------------------------------------

    url(r'TaskMag/dataTaskMag/$',views.dataTaskMag, name='dataTaskMag'),
    url(r'TaskMag/getDataTaskMagList/$',views.getDataTaskMagList, name='getDataTaskMagList'),
    url(r'TaskMag/saveTaskMag/$',views.saveTaskMag, name='saveTaskMag'),
    url(r'TaskMag/taskMagActivation/$',views.taskMagActivation, name='taskMagActivation'),

    #------------------------------------方国巍----------------------------------------------------------------

    url(r'^Basic/getBasicTestingList/$', views.getBasicTestingList, name='getBasicTestingList'),
    url(r'^Basic/saveBasicTesting/$', views.saveBasicTesting, name='saveBasicTesting'),
    url(r'^Basic/deleteBasicTesting/$', views.deleteBasicTesting, name='deleteBasicTesting'),
    url(r'^Basic/getCheckObjectList/$', views.getCheckObjectList, name='getCheckObjectList'),
    url(r'^Basic/getNameList/$', views.getNameList, name='getNameList'),
    url(r'^Basic/getcheckmethodlist/$', views.checkMethodList, name='getcheckmethodlist'),
    url(r'^Basic/getOftenRules/$', views.getOftenRules,name='getOftenRules'),
    url(r'^Basic/getCheckFieldList/$', views.getCheckFieldList,name='getCheckFieldList'),
    url(r'^Basic/getRuleParamList/$', views.getRuleParamList,name='getRuleParamList'),

    ]
