# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
import UserManage.views.user as user
import UserManage.views.group as group
import UserManage.views.permission as permission

urlpatterns = [
    url(r'login/$', user.LoginUser, name = 'loginurl'),
    url(r'logout/$', user.LogoutUser, name = 'logouturl'),


    url(r'^user/add/$', user.AddUser, name = 'adduserurl'),
    url(r'^user/list/$', user.ListUser, name = 'listuserurl'),
    url(r'^user/edit/$', user.EditUser, name = 'edituserurl'),
    url(r'^user/delete/$', user.DeleteUser, name = 'deleteuserurl'),


    url(r'^user/changepwd/$', user.ChangePassword, name = 'changepasswordurl'),
    url(r'^user/resetpwd/$', user.ResetPassword, name = 'resetpasswordurl'),


    url(r'^group/add/$', group.AddGroup, name = 'addgroupurl'),
    url(r'^group/list/$', group.ListGroup, name = 'listgroupurl'),
    url(r'^group/edit/$', group.EditGroup, name = 'editgroupurl'),
    url(r'^group/delete/$', group.DeleteGroup, name = 'deletegroupurl'),


    url(r'^permission/deny/$', permission.NoPermission, name = 'permissiondenyurl'),

    url(r'^permission/add/$', permission.AddPermission, name = 'addpermissionurl'),
    url(r'^permission/list/$', permission.ListPermission, name = 'listpermissionurl'),
    url(r'^permission/edit/$', permission.EditPermission, name = 'editpermissionurl'),
    url(r'^permission/delete/$', permission.DeletePermission, name = 'deletepermissionurl'),

    url(r'^user/getlist/$', user.getList, name = 'getlisturl'),
    url(r'^group/getGroupList/$', group.getGroupList, name = 'getgrouplisturl'),
    url(r'^permission/getPermissionlist/$', permission.getPerList, name = 'getpermissionlisturl'),
    url(r'^group/getGroupName/$', group.getGroupName, name = 'getgroupnameurl'),
    url(r'^permission/getName/$', permission.getName, name = 'getnameurl'),

]