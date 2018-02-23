from django.contrib import admin
from .models import BaseType,BaseTypeDisplay
from .models import RunTask,RunTaskDisplay
from .models import FileDownload,FileDownloadDisplay
from .models import DataInterface,DataInterfaceDisplay
from .models import InfoFile,InfoFileDisplay
from .models import TimeTask,DataIncrement,dataIncrementDisplay
# Register your models here.


admin.site.register(BaseType,BaseTypeDisplay)
admin.site.register(RunTask,RunTaskDisplay)
admin.site.register(FileDownload,FileDownloadDisplay)
admin.site.register(DataInterface,DataInterfaceDisplay)
admin.site.register(InfoFile,InfoFileDisplay)
admin.site.register(TimeTask)
admin.site.register(DataIncrement,dataIncrementDisplay)