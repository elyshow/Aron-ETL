from django.contrib import admin
from .models import ApiData,ApiDataDisplay
from .models import Dommana
from .models import InfoSqlFile,InfoSqlFileDisplay
# Register your models here.


admin.site.register(ApiData,ApiDataDisplay)
admin.site.register(Dommana)
admin.site.register(InfoSqlFile,InfoSqlFileDisplay)
