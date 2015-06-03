# -*- coding: utf-8 -*-

from .jobbase import JobBase
from ._base import TYPE_JOBCRON
from .cron import Cron


class JobCron(JobBase):
    def __init__(self, name, pyfile, method, params=None, cron=None):
        super(JobCron, self).__init__(name, pyfile, method, params)
        self.param['type'] = TYPE_JOBCRON
        if cron == None:
            cron = Cron()
        if isinstance(cron, dict):
            cron = Cron(**cron)
        self.param['cron'] = cron.toDictByTime()

    @property
    def cron(self):
        return Cron(**self.param['cron'])

    def __str__(self):
        crondisc = str(self.cron)
        return '%s[执行时间]\n\t%s' % (super(JobCron, self).__str__(), '\n\t'.join(crondisc.split('\n')))

    def addToScheduler(self, sche):
        cron = Cron(**self.param['cron'])
        sche.add_cron_job(self._getMethod(), args=self.params, **cron.toDictByDateTime())
