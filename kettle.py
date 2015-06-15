# -*- coding: utf-8 -*-

import subprocess
import os
import time

KITCHEN = r'D:\toGeek\kettle\bin\kitchen.bat'
JOBPATH = r'D:\toGeek\kettle\kettlerep'


def _joinParams(params):
   if isinstance(params, dict) and params:
      ss = []
      for key in params.keys():
         ss.append('/param:%s="%s"' % (str(key), str(params[key])))
      return uncd.toUnicode(' '.join(ss))


def exeJobByFilename(filename, params=None, logfile=None):
   filename = uncd.toUnicode(filename)
   command = r'%s /norep /file:"%s"' % (KITCHEN, filename)
   parastr = _joinParams(params)
   if parastr:
      command += ' ' + parastr
   if logfile:
      command += r' /logfile:"%s" /level:Error' % logfile
   return not subprocess.call(uncd.toGbk(command), shell=True)


def exeJobByName(name, params=None, logfile=None):
   name = uncd.toUnicode(name)
   filename = os.path.join(JOBPATH, name + '.kjb')
   return exeJobByFilename(filename, params, logfile)


def batExeJobByName(interval, *names):
   for i in range(len(names)):
      job = names[i]
      if isinstance(job, basestring):
         exeJobByName(job)
      else:
         name, params = job
         exeJobByName(name, params)
      if i != len(names) - 1:
         time.sleep(interval)
