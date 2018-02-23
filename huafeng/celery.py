from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'huafeng.settings')
# Specifying the settings here means the celery command line program will know where your Django project is.
# This statement must always appear before the app instance is created, which is what we do next:
from django.conf import settings

app = Celery('huafeng')

app.config_from_object('django.conf:settings')
# This means that you don’t have to use multiple configuration files, and instead configure Celery directly from the Django settings.
# You can pass the object directly here, but using a string is better since then the worker doesn’t have to serialize the object.

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# With the line above Celery will automatically discover tasks in reusable apps if you define all tasks in a separate tasks.py module.
# The tasks.py should be in dir which is added to INSTALLED_APP in settings.py.
# So you do not have to manually add the individual modules to the CELERY_IMPORT in settings.py.

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # dumps its own request information

import datetime
import json
from djcelery import models as celery_models
from django.utils import timezone


def create_task(name, task, task_args, crontab_time):
    """
    创建celery定时任务
    :param name: 任务名称
    :param task: 执行的任务
    :param task_args: 任务参数
    :param crontab_time: 定时任务时间 格式：
    {
        'month_of_year': 9 # 月份
        'day_of_month': 5 # 日期
        'hour': 01 # 小时
        'minute':05 # 分钟
    }
    :return:
    """

    task, created = celery_models.PeriodicTask.objects.get_or_create(name=name, task=task)
    crontab = celery_models.CrontabSchedule.objects.filter(**crontab_time).first()

    if crontab is None:
        crontab = celery_models.CrontabSchedule.objects.create(**crontab_time)

    task.crontab = crontab
    task.enabled = True
    task.kwargs = json.dumps(task_args)
    task.save()
    return True


def disable_task(name):
    """
    关闭定时任务
    :param name: 任务名称
    :return:
    """
    try:
        task = celery_models.PeriodicTask.objects.get(name=name)
        task.enabled = False
        task.save()
        return True
    except celery_models.PeriodicTask.DoesNotExist:
        return True

