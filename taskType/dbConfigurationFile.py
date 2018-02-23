
# 请填写本机数据库配置信息


#填写文件上传的路径
commonFileWay='/opt/huafeng/allinweb/PythonProject/File'
sqlFileWay='/opt/huafeng/allinweb/PythonProject/SqlFile'
apiFileWay='/opt/huafeng/allinweb/PythonProject/ApiFile'
errorFileWay='/opt/huafeng/allinweb/PythonProject/erroFile'

#本机数据库连接信息
host='192.168.6.77'                                #数据库IP
port=3306                           #数据库端口
user = 'root'                          #连接数据库用户名
pwd = '123456'                         #数据库端口
db = 'configuredb'                          #配置库
collectdb='collectdb'                        #连接的数据库名(一定要填采集库)
collerrordb = 'collecterrordb'            #采集问题数据库

shellPath = '/opt/huafeng/allinweb/huafeng/scp.sh'  #脚本文件路径
savePath = '/opt/huafeng/allinweb/PythonProject/fileDownLoad/'   #下载保存路径