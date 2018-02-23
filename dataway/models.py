from django.db import models

# Create your models here.
class Conditionapi(models.Model):
    idapi = models.CharField(db_column='idAPI', max_length=24, blank=True, null=True)  # Field name made lowercase.
    conditionname = models.CharField(db_column='conditionName', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def _str_(self):
        return self.idapi


class Adminapi(models.Model):
    nameapi = models.CharField(db_column='nameAPI', max_length=12, blank=True, null=True)  # Field name made lowercase.
    idapi = models.CharField(db_column='idAPI', primary_key=True, max_length=24)  # Field name made lowercase.
    warehouseapi = models.CharField(db_column='warehouseAPI', max_length=12, blank=True, null=True)  # Field name made lowercase.
    tableapi = models.CharField(db_column='tableAPI', max_length=12, blank=True, null=True)  # Field name made lowercase.
    createtime = models.CharField(db_column='createTime', max_length=24, blank=True, null=True)  # Field name made lowercase.

    def _str_(self):
        return self.nameapi

class Fieldapi(models.Model):
    fieldData = models.CharField(db_column='fieldData', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idapi = models.CharField(db_column='idAPI', max_length=24, blank=True, null=True)  # Field name made lowercase.
    def _str_(self):
        return self.fielddata




