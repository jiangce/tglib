# -*- coding: utf-8 -*-

from ctypes import *
import os

DLL_PATH = os.path.dirname(__file__) + '\\'
DLL_FILE = os.path.join(DLL_PATH, 'GoldenClnt.dll')


class Golden(object):
    api = windll.LoadLibrary(DLL_FILE)

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def __enter__(self):
        self.openConnect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnect()

    def openConnect(self):
        return Golden.api.Go_Connect(c_char_p(self.ip.encode('gbk')), c_ushort(self.port)) == 0

    def closeConnect(self):
        return Golden.api.Go_Disconnect() == 0

    def getTableCount(self):
        count = pointer(c_short())
        if Golden.api.Go_TableCount(count) == 0:
            return count.contents.value

    def getPointCount(self):
        count = pointer(c_long())
        if Golden.api.Go_PointCount(count) == 0:
            return count.contents.value

    def getPointIds(self):
        count = self.getPointCount()
        tagmask = c_char_p(b'*')
        tab = c_short(0)
        source = c_char_p(b'\0')
        unit = c_char_p(b'\0')
        desc = c_char_p(b'\0')
        descex = c_char_p(b'\0')
        mode = c_short(0)
        pts = pointer((c_long * count)())
        pcount = pointer(c_long(count))
        if Golden.api.GoB_Search(tagmask, tab, source, unit, desc, descex, mode, pts, pcount) == 0:
            return list(pts.contents)

    def getPointDesc(self, id):
        Golden.api.GoV_GetPointProperty(c_long(id))
        desc = c_char_p(b'\0' * 50)
        Golden.api.GoV_GetDesc(desc)
        return id, desc.value.decode('gbk')

    def getPoints(self, ids):
        return [self.getPointDesc(id) for id in ids]

    def getPointValue(self, id):
        pt = c_long(id)
        datatime = c_long()
        value = c_float()
        status = c_long()
        if Golden.api.GoS_GetSnapshot(pt, pointer(datatime), pointer(value), pointer(status)) == 0:
            return value.value

    def getPointValueBatch(self, ids):
        count = len(ids)
        pts = pointer((c_long * count)(*ids))
        pcount = c_long(count)
        datetime = pointer((c_long * count)())
        values = pointer((c_float * count)())
        statuses = pointer((c_long * count)())
        errors = pointer((c_ulong * count)())
        if Golden.api.GoS_GetSnapshots(pts, pointer(pcount), datetime, values, statuses, errors) == 0:
            return [(ids[i], values.contents[i], datetime.contents[i], statuses.contents[i]) for i in range(count)]
