# -*- coding: utf-8 -*-

import os
from ctypes import *

DLL_PATH = os.path.dirname(__file__) + '\\'
DLL_FILE = os.path.join(DLL_PATH, 'RTDBInterface.dll')


class TagData(Structure):
    _fields_ = [('value', c_double), ('time', c_long), ('status', c_int)]


class VESTOR(object):
    """
    VESTOR is an adapter to access RTDBInterface DLL.
    """
    api = cdll.LoadLibrary(DLL_FILE)

    def connect(self):
        '''
        打开数据库连接
        '''
        nCount = c_long(4)
        ps = (c_char_p * 4)()
        ps[0] = c_char_p(DLL_PATH.encode())
        ps[1] = c_char_p(DLL_PATH.encode())
        return self.api.InitConnect(ps, nCount) == 0

    def close(self):
        """
        释放数据库连接
        """
        self.api.ReleaseConnect()

    def getPointValue(self, pointname):
        """
        获得单点值
        返回：(id, value, time, status)
        """
        if not pointname:
            return
        if self.connect():
            data = TagData()
            ok = self.api.GetRTDataByTagName(c_char_p(pointname.encode()), byref(data)) == 0
            self.close()
            if ok:
                return pointname, data.value, data.time, data.status

    def getPointValueBatch(self, pointnames):
        """
        批量获得值
        返回：[(id, value, time, status), ...]
        """
        if not pointnames:
            return
        pointnames = list(pointnames)
        if self.connect():
            size = len(pointnames)
            names = (c_char_p * size)()
            for i in range(size):
                names[i] = c_char_p(pointnames[i].encode())
            data = pointer((TagData * size)())
            ok = self.api.GetRTDataByBatch(names, data, c_int(size)) == 0
            self.close()
            if ok:
                result = []
                for i in range(size):
                    result.append((pointnames[i], data.contents[i].value,
                                   data.contents[i].time, data.contents[i].status))
                return result