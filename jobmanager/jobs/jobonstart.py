# -*- coding: utf-8 -*-

from .jobbase import JobBase
from ._base import TYPE_JOBONSTART
from datetime import datetime, timedelta


class JobOnStart(JobBase):
    TIMEOFFSET = 1

    def __init__(self, name, pyfile, method, params=None, second=1):
        super(JobOnStart, self).__init__(name, pyfile, method, params)
        self.param['type'] = TYPE_JOBONSTART
        self.param['second'] = second

    @property
    def second(self):
        return self.param['second']

    def __str__(self):
        return '%s[执行时间]\n\t服务启动后%s秒' % (super(JobOnStart, self).__str__(), self.second)

    def addToScheduler(self, sche):
        sche.add_date_job(self._getMethod(), datetime.now() + timedelta(seconds=self.TIMEOFFSET + self.second),
                          args=self.params)
