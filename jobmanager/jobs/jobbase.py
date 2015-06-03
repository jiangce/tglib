# -*- coding: utf-8 -*-

import abc
import json
import os
import sys


class JobBase(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, pyfile, method, params=None):
        if params == None:
            params = []
        self.param = {'name': name,
                      'pyfile': pyfile,
                      'method': method,
                      'params': params,
                      'type': -1}

    @property
    def type(self):
        return self.param['type']

    @property
    def name(self):
        return self.param['name']

    @property
    def pyfile(self):
        return self.param['pyfile']

    @property
    def method(self):
        return self.param['method']

    @property
    def params(self):
        return self.param['params']

    def saveToString(self):
        return json.dumps(self.param, ensure_ascii=False)

    def loadFromString(self, s):
        self.param = json.loads(s)
        return self.param

    def __str__(self):
        ps = ''
        for p in self.params:
            ps += '\n\t' + str(p)
        return '[作业名称]\n\t%s\n' \
               '[脚本文件]\n\t%s\n' \
               '[脚本方法]\n\t%s\n' \
               '[脚本参数]\n\t%s\n' \
               % (self.name, self.pyfile, self.method, ps.strip())

    @abc.abstractmethod
    def addToScheduler(self, sche):
        pass

    def _getMethod(self):
        path = os.path.dirname(self.pyfile)
        fileName, fileExt = os.path.splitext(os.path.basename(self.pyfile))
        if not path in sys.path:
            sys.path.insert(0, path)
        module = __import__(fileName)
        return eval('module.%s' % self.method)
