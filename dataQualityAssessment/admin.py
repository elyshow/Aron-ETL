from django.contrib import admin
from .models import Assess,AssessDisplay
from .models import Logassessment,LogassessmentDisplay
from .models import Result,ResultDisplay
# Register your models here.



admin.site.register(Assess,AssessDisplay)
admin.site.register(Logassessment,LogassessmentDisplay)
admin.site.register(Result,ResultDisplay)
