from django.contrib import admin

from .models import Problems,ProblemsDisplay
from .models import Catalogue,CatalogueDisplay
from .models import Release,ReleaseDisplay
from .models import Resourcefield,ResourcefieldDisplay
from .models import Assesstb,AssesstbDisplay



# Register your models here.
admin.site.register(Problems,ProblemsDisplay)
admin.site.register(Catalogue,CatalogueDisplay)
admin.site.register(Release,ReleaseDisplay)
admin.site.register(Resourcefield,ResourcefieldDisplay)
admin.site.register(Assesstb,AssesstbDisplay)
