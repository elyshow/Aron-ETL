from django.contrib import admin
from .models import *

admin.site.register(Cataloguedataway,CataloguedatawayDisplay)
admin.site.register(Cataloguedatawaybm,CataloguedatawaybmDisplay)
admin.site.register(InterfacejournalProtslog,InterfacejournalProtslogDisplay)
