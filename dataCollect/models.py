from django.db import models

# Create your models here.


# 采集节点model
class CollectNode(models.Model):
    collectNodeName = models.CharField(u'采集节点名称', max_length=255, unique=True)
    collectNodeRegion = models.CharField(u'所属区域', max_length=255)
    collectNodeStatus = models.CharField(u'节点状态', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.collectNodeName


# 采集任务model
class CollectTask(models.Model):
    taskName = models.CharField(u'采集任务名称', max_length=255)
    # 1: 文件，2: 数据库接口， 3: WebService接口
    taskType = models.IntegerField(u'采集任务类型')
    collectNodeId = models.IntegerField(u'采集任务所属采集节点ID')
    belongInstitution = models.CharField(u'所属机构', max_length=1000)
    belongType = models.CharField(u'所属类型', max_length=25)

    # 0: 全量清洗 1: 增量清洗
    collectWay = models.IntegerField(u'采集方式', default=0)

    # 详细参数

    # 文件部分
    fileType = models.CharField(u'文件类型', max_length=255, blank=True, null=True)
    filePath = models.CharField(u'文件路径', max_length=255, blank=True, null=True)
    username = models.CharField(u'用户名', max_length=50, blank=True, null=True)
    password = models.CharField(u'密码', max_length=128, blank=True, null=True)
    fileRoot = models.CharField(u'采集根目录', max_length=150, blank=True, null=True)
    fileFields = models.TextField(u'采集字段', blank=True, null=True)
    rowField = models.CharField(u'采集行', max_length=150, blank=True, null=True)

    #文件内容解析需要部分
    fieldLimitCode = models.CharField(u'文本限定符',max_length=3, blank= True, null= True)
    fieldSplitCode = models.CharField(u'字段分隔符',max_length=3, blank= True, null= True)

    # 数据库部分

    databaseType = models.CharField(u'数据库类型', max_length=255, blank=True, null=True)
    databaseHostName = models.CharField(u'主机名称', max_length=255, blank=True, null=True)
    databaseName = models.CharField(u'主机名称', max_length=255, blank=True, null=True)
    dataTableSpace = models.CharField(u'数据表空间', max_length=255, blank=True, null=True)
    indexTableSpace = models.CharField(u'索引表空间', max_length=255, blank=True, null=True)
    databasePort = models.CharField(u'端口号', max_length=255, blank=True, null=True)
    databaseUserName = models.CharField(u'用户名', max_length=255, blank=True, null=True)
    databasePassword = models.CharField(u'密码', max_length=255, blank=True, null=True)

    databaseTableName = models.CharField(u'所选表', max_length=255, blank=True, null=True)
    databaseCollectSQL = models.TextField(u'获取SQL查询语句', blank=True, null=True)
    databaseFields = models.TextField(u'所选字段', blank=True, null=True)
    databaseIncrementField = models.CharField(u'增量字段', max_length=255, blank=True, null=True)

    # WebService接口部分

    ##
    ##

    # 采集本地生成的表名称
    newCollectCreateTableName = models.CharField(u'本地生成的表名', max_length=255, blank=True, null=True)

    # 0: 停用 1: 启用
    flag = models.BooleanField(u'是否启用标志')
    # 0: 未运行状态 1: 运行中 2: 运行出错
    taskStatus = models.IntegerField(u'采集任务状态')

    # 1: 固定时间, 2: 一次性 , 3: 手动 4: 间隔
    timeType = models.IntegerField(u'执行时间分类')
    # example
    # 1: {"day": "2,10,13", "week": "1,5", "hour": "0,4,13", "min": "1,53"}
    # 2: {"year": "2016", "month": "12", "day": "30", "hour": "12", "min": "59"}
    # 3: NULL
    # 4: {"day": 30, "hour": 4, "min": 30}
    timeStr = models.TextField(u'执行时间字符串')

    createTime = models.DateTimeField(u'创建时间', auto_now_add=True, editable=True, null=True)
    editTime = models.DateTimeField(u'修改时间', auto_now=True, null=True)

    def __str__(self):
        return self.taskName


# 采集日志model
class CollectTaskLog(models.Model):
    collectNodeId = models.IntegerField(u'采集节点ID', default=0)
    taskId = models.IntegerField(u'采集任务ID')
    taskName = models.CharField(u'采集任务名称', max_length=255)
    startTime = models.DateTimeField(u'任务开始时间', auto_now_add=True, editable=True, null=True)
    endTime = models.DateTimeField(u'任务结束时间', auto_now=True, editable=True, null=True)
    # 0: 未运行状态 1: 运行中 2: 运行出错
    taskStatus = models.IntegerField(u'采集任务状态', null=True, default=0)
    allCount = models.IntegerField(u'成功数量', null=True, default=0)
    successCount = models.IntegerField(u'成功数量', null=True, default=0)
    errorCount = models.IntegerField(u'失败数量', null=True, default=0)
    incrementContent = models.CharField(u'增量字段内容记录', max_length=255, blank=True, null=True)
    nowCount = models.CharField(u'当前数量',max_length=255, default=0, null = True)


# 自定义oracle的varchar2字段
class varchar2Field(models.Model):
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super(varchar2Field, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'VARCHAR2(%s)' % self.max_length