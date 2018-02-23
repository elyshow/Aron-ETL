from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    # 采集节点相关
    url(r'^collectNode/$', views.collectNodeIndex, name='collectNode'),
    url(r'^getCollectNodeListData/$', views.getCollectNodeListData, name='getCollectNodeListData'),
    url(r'^saveCollectNode/$', views.saveCollectNode, name='saveCollectNode'),
    url(r'^delCollectNode/$', views.delCollectNode, name='delCollectNode'),

    # 采集任务相关
    url(r'^collectTask(/(?P<collectNodeId>\d*))?/$', views.collectTaskIndex, name='collectTask'),
    url(r'^getCollectTaskListData/$', views.getCollectTaskListData, name='getCollectTaskListData'),
    url(r'^saveCollectTask/$', views.saveCollectTask, name='saveCollectTask'),
    url(r'^delCollectTask/$', views.delCollectTask, name='delCollectTask'),

    url(r'^runCollectTask/$', views.runCollectTask, name='runCollectTask'),
    # # 测试数据库连接
    url(r'^testDataBaseConnect/$', views.testDataBaseConnect, name='testDataBaseConnect'),
    # # 获取表
    url(r'^getDataBaseTables/$', views.getDataBaseTables, name='getDataBaseTables'),
    # # 获取SQL语句
    url(r'^getSelectAllSQL/$', views.getSelectAllSQL, name='getSelectAllSQL'),
    # # 获取预览数据
    url(r'^getPreviewData/$', views.getPreviewData, name='getPreviewData'),
    # # 启用禁用
    url(r'^endisableCollectTask/$', views.endisableCollectTask, name='endisableCollectTask'),

    # 其他相关
    url(r'^getBelongInstitution/$', views.getBelongInstitution, name='getBelongInstitution'),
    url(r'^getBelongType/$', views.getBelongType, name='getBelongType'),
    url(r'^getCollectTable/$', views.getCollectTable, name='getCollectTable'),
    url(r'^testServer/$', views.testServer, name='testServer'),
    url(r'^getRootElement/$', views.getRootElement, name='getRootElement'),
    url(r'^getDataGridList/$', views.getDataGridList, name='getDataGridList'),
    url(r'^getCollectTaskLog/$', views.getCollectTaskLog, name='getCollectTaskLog'),
    url(r'^getProgressBar/$', views.getProgressBar, name='getProgressBar'),
]
