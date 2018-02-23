from __future__ import absolute_import

from celery import task

from celery import shared_task

from . import views, sites

import time


@shared_task
def celeryRunCleanTaskById(taskId):
    """
    celery执行清洗任务
    :param taskId: 清洗任务ID
    :return:
    """
    return sites.site.runCleanTaskById(taskId)
