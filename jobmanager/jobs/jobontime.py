# -*- coding: utf-8 -*-

from .jobbase import JobBase
from ._base import TYPE_JOBONTIME
from datetime import datetime
import time


class JobOnTime(JobBase):
    def __init__(self, name, pyfile, method, params=None, time=time.time()):
        super(JobOnTime, self).__init__(name, pyfile, method, params)
        self.param['type'] = TYPE_JOBONTIME
        self.param['time'] = time

    @property
    def time(self):
        return self.param['time']

    def __str__(self):
        t = tuple(time.localtime(self.time))[:6]
        return '%s[执行时间]\n\t%d年%d月%d日 %02d:%02d:%02d' % \
               (super(JobOnTime, self).__str__(), t[0], t[1], t[2], t[3], t[4], t[5])

    def addToScheduler(self, sche):
        sche.add_date_job(self._getMethod(), datetime.fromtimestamp(self.time), args=self.params)