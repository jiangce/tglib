# -*- coding: utf-8 -*-

from datetime import datetime
from apscheduler.scheduler import Scheduler
import time


class Cron(object):
    def __init__(self, year=None, month=None, day=None, week=None,
                 day_of_week=None, hour=None, minute=None, second=None,
                 start_date=None):
        self.year = year
        self.month = month
        self.day = day
        self.week = week
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second
        if isinstance(start_date, float):
            start_date = datetime.fromtimestamp(start_date)
        self.start_date = start_date

    def toDictByDateTime(self):
        return {'year': self.year,
                'month': self.month,
                'day': self.day,
                'week': self.week,
                'day_of_week': self.day_of_week,
                'hour': self.hour,
                'minute': self.minute,
                'second': self.second,
                'start_date': self.start_date}

    def toDictByTime(self):
        result = self.toDictByDateTime()
        if result['start_date']:
            result['start_date'] = time.mktime(result['start_date'].timetuple())
        return result

    def checkCron(self):
        def fun():
            pass

        sche = Scheduler()
        try:
            sche.add_cron_job(fun, **self.toDictByDateTime())
            return True
        except:
            return False
        finally:
            del sche

    def __str__(self):
        return 'Year: %s\n' \
               'Month: %s\n' \
               'Day: %s\n' \
               'Week: %s\n' \
               'Day of week: %s\n' \
               'Hour: %s\n' \
               'Minute: %s\n' \
               'Second: %s\n' \
               'Start Date: %s' % \
               (self.year, self.month, self.day, self.week, self.day_of_week,
                self.hour, self.minute, self.second, self.start_date)