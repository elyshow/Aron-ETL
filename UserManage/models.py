#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
class PermissionList(models.Model):
    name = models.CharField(max_length = 64)
    url = models.CharField(max_length = 255)

    def __str__(self):
        return '%s(%s)' % (self.name, self.url)

class GroupList(models.Model):
    name = models.CharField(max_length = 64)
    permission = models.ManyToManyField(PermissionList, blank = True)

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, email, username, department, telephone, password = None):
        if not department:
            raise ValueError('Users must have a department')
        if not telephone:
            raise ValueError('Users must have a telephone')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            department = department,
            telephone = telephone,
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, department, telephone, password):
        user = self.create_user(email,
            username = username,
            password = password,
            department = department,
            telephone = telephone,
        )

        user.is_active = True
        user.is_superuser = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length = 255, unique = True, db_index = True)
    telephone = models.CharField(max_length= 255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    group = models.ForeignKey(GroupList,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'department', 'telephone']

    def has_perm(self,perm,obj=None):
        if self.is_active and self.is_superuser:
            return True

class UserLog(models.Model):
    usernamelog = models.CharField(max_length = 64, blank = True, null = True)
    pathlog = models.CharField(max_length = 255, blank = True, null = True)
    flag = models.CharField(max_length = 1, blank = True, null = True)
    timelog = models.DateTimeField(auto_now_add=True)
    descriptions = models.CharField(max_length = 255, blank = True, null = True)

    def __str__(self):
        return self.name

