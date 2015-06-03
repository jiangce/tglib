# -*- coding: utf-8 -*-

from .jobs import *
from apscheduler.scheduler import Scheduler
import json
import os


def createJobByString(s):
   param = json.loads(s)
   job = None
   if param['type'] == TYPE_JOBONSTART:
      job = JobOnStart(None, None, None, None, None)
   elif param['type'] == TYPE_JOBONTIME:
      job = JobOnTime(None, None, None, None, None)
   elif param['type'] == TYPE_JOBPERTIME:
      job = JobPerTime(None, None, None, None, None)
   elif param['type'] == TYPE_JOBCRON:
      job = JobCron(None, None, None, None, None)
   if job:
      job.loadFromString(s)
      return job


def loadJobs(jobStoreFile):
   if not os.path.exists(jobStoreFile):
      return []
   with open(jobStoreFile, 'r') as f:
      return [createJobByString(s) for s in f.readlines() if s.strip()]


def saveJobs(jobs, jobStoreFile):
   with open(jobStoreFile, 'w') as f:
      f.writelines([job.saveToString() + '\n' for job in jobs])


def getScheduler(jobs):
   sche = Scheduler()
   for job in jobs:
      job.addToScheduler(sche)
   return sche
