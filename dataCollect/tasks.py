from __future__ import absolute_import

from celery import task

from celery import shared_task

from . import views

import time


@shared_task
def celeryRunCollectTaskById(taskId):
    """
    celery执行采集任务
    :param taskId: 采集任务ID
    :return:
    """
    print('celeryRunCollectTaskById')
    views.runCollectTaskById(taskId)