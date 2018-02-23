from django.contrib import admin
from .models import Table1,Table1Display
from .models import Table2,Table2Display
from .models import Table4,Table4Display
from .models import Table5,Table5Display
from .models import Table6,Table6Display
from .models import Parameters,ParametersDisplay
from .models import Totable,TotableDisplay
from .models import Rules,RulesDisplay
from .models import Log,LogDisplay
from .models import Base,BaseDisplay

# Register your models here.

admin.site.register(Table1,Table1Display)
admin.site.register(Table2,Table2Display)
admin.site.register(Table4,Table4Display)
admin.site.register(Table5,Table5Display)
admin.site.register(Table6,Table6Display)
admin.site.register(Parameters,ParametersDisplay)
admin.site.register(Totable,TotableDisplay)
admin.site.register(Rules,RulesDisplay)
admin.site.register(Log,LogDisplay)
admin.site.register(Base,BaseDisplay)