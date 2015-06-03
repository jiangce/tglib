# -*- coding:utf-8 -*-

from ._edna import EDNA, Service, ServicePoint, Point
from datetime import datetime


class SimpleEDNA(object):
    def __init__(self):
        self.edna = EDNA()

    def getServiceList(self, sType, count=20):
        s = Service(count, sType, '', 64, 128, 32, 32)
        if self.edna.getServiceList(s) == 0:
            return [(s.szSvcName[i], s.szSvcDesc[i], s.szStatus[i])
                    for i in range(len(s.szSvcName)) if s.szSvcName[i]]

    def getPointList(self, serviceName, count=50000):
        sp = ServicePoint(count, serviceName, 0, 32, 32, 32, 128, 32)
        if self.edna.getPointsFromService(sp) == 0:
            return [(sp.dValue[i], sp.szPointId[i], sp.szTime[i], sp.szStatus[i], sp.szDesc[i], sp.szUnits[i])
                    for i in range(len(sp.szPointId)) if sp.szPointId[i]]

    def getRTAll(self, pointid):
        pt = Point(pointid, 0, 32, 32, 128, 64)
        if self.edna.getRTAll(pt) == 0:
            return self._getdictfrompoint(pt)

    def _getdictfrompoint(self, point):
        return {'id': point.szPoint,
                'value': point.pdValue,
                'unit': point.szUnits.strip(),
                'status': point.szStatus.strip(),
                'lasttime': datetime.strptime(point.szTime.strip(), '%m/%d/%y %H:%M:%S'),
                'description': point.szDesc.strip()}