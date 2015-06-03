# -*- coding:utf-8 -*-

from ctypes import *

DLL_FILE = r'c:\dna\ezdnaapi.dll'


def trydecode(s):
    try:
        return s.decode('gbk')
    except:
        try:
            return s[:-1].decode('gbk')
        except:
            return s


class EDNA(object):
    api = windll.LoadLibrary(DLL_FILE)

    def getServiceList(self, service):
        nCount = c_ushort(service.nCount)
        szType = c_char_p(service.szType.encode('gbk'))
        szStartSvcName = c_char_p(service.szStartSvcName.encode('gbk'))

        szSvcName = (c_char_p * service.nCount)()
        nSvcName = c_short(service.nSvcName)

        szSvcDesc = (c_char_p * service.nCount)()
        nSvcDesc = c_ushort(service.nSvcDesc)

        szSvcType = (c_char_p * service.nCount)()
        nSvcType = c_ushort(service.nSvcType)

        szStatus = (c_char_p * service.nCount)()
        nStatus = c_ushort(service.nStatus)

        for i in range(service.nCount):
            szSvcName[i] = c_char_p(b'\0' * service.nSvcName)
            szSvcDesc[i] = c_char_p(b'\0' * service.nSvcDesc)
            szSvcType[i] = c_char_p(b'\0' * service.nSvcType)
            szStatus[i] = c_char_p(b'\0' * service.nStatus)

        res = self.api.DnaGetServiceList(nCount, szType, szStartSvcName, szSvcName, nSvcName,
                                         szSvcDesc, nSvcDesc, szSvcType, nSvcType, szStatus, nStatus)

        service.szSvcName = [trydecode(s.strip()) for s in szSvcName]
        service.szSvcDesc = [trydecode(s.strip()) for s in szSvcDesc]
        service.szSvcType = [trydecode(s.strip()) for s in szSvcType]
        service.szStatus = [trydecode(s.strip()) for s in szStatus]

        return res

    def getPointsFromService(self, servicePoint):
        nCount = c_ushort(servicePoint.nCount)
        szServiceName = c_char_p(servicePoint.szServiceName.encode('gbk'))
        nStarting = c_ushort(servicePoint.nStarting)

        dValue = (c_double * servicePoint.nCount)()

        szPointId = (c_char_p * servicePoint.nCount)()
        nPointIdLen = c_ushort(servicePoint.nPointIdLen)
        szTime = (c_char_p * servicePoint.nCount)()
        nTimeLen = c_ushort(servicePoint.nTimeLen)
        szStatus = (c_char_p * servicePoint.nCount)()
        nStatusLen = c_ushort(servicePoint.nStatusLen)
        szDesc = (c_char_p * servicePoint.nCount)()
        nDescLen = c_ushort(servicePoint.nDescLen)
        szUnits = (c_char_p * servicePoint.nCount)()
        nUnitsLen = c_ushort(servicePoint.nUnitsLen)

        for i in range(servicePoint.nCount):
            szPointId[i] = c_char_p(b'\0' * servicePoint.nPointIdLen)
            szTime[i] = c_char_p(b'\0' * servicePoint.nTimeLen)
            szStatus[i] = c_char_p(b'\0' * servicePoint.nStatusLen)
            szDesc[i] = c_char_p(b'\0' * servicePoint.nDescLen)
            szUnits[i] = c_char_p(b'\0' * servicePoint.nUnitsLen)

        res = self.api.DnaGetPointList(nCount, szServiceName, nStarting, szPointId, nPointIdLen, dValue,
                                       szTime, nTimeLen, szStatus, nStatusLen, szDesc, nDescLen, szUnits, nUnitsLen)

        servicePoint.szPointId = [trydecode(s.strip()) for s in szPointId]
        servicePoint.szTime = [trydecode(s.strip()) for s in szTime]
        servicePoint.szStatus = [trydecode(s.strip()) for s in szStatus]
        servicePoint.szDesc = [trydecode(s.strip()) for s in szDesc]
        servicePoint.szUnits = [trydecode(s.strip()) for s in szUnits]
        servicePoint.dValue = dValue

        return res

    def getRTAll(self, point):
        '''
        Get the specified point Real-Time all information.
        '''
        szPoint = c_char_p(point.szPoint.encode('gbk'))
        pdValue = pointer(c_double(point.pdValue))
        szTime = c_char_p(point.szTime.encode('gbk'))
        nTime = c_ushort(point.nTime)
        szStatus = c_char_p(point.szStatus.encode('gbk'))
        nStatus = c_ushort(point.nStatus)
        szDesc = c_char_p(point.szDesc.encode('gbk'))
        nDesc = c_ushort(point.nDesc)
        szUnits = c_char_p(point.szUnits.encode('gbk'))
        nUnits = c_ushort(point.nUnits)

        res = self.api.DNAGetRTAll(szPoint, pdValue, szTime, nTime, szStatus, nStatus, szDesc, nDesc, szUnits, nUnits)

        point.pdValue = pdValue.contents.value
        point.szTime = trydecode(szTime.value)
        point.szStatus = trydecode(szStatus.value)
        point.szDesc = trydecode(szDesc.value)
        point.szUnits = trydecode(szUnits.value)

        return res


class Service(object):
    def __init__(self, nCount, szType, szStartSvcName, nSvcName, nSvcDesc, nSvcType, nStatus):
        self.nCount = nCount
        self.szType = szType
        self.szStartSvcName = szStartSvcName
        self.szSvcName = None
        self.nSvcName = nSvcName
        self.szSvcDesc = None
        self.nSvcDesc = nSvcDesc
        self.szSvcType = None
        self.nSvcType = nSvcType
        self.szStatus = None
        self.nStatus = nStatus


class ServicePoint(object):
    def __init__(self, nCount, szServiceName, nStarting, nPointIdLen, nTimeLen, nStatusLen, nDescLen, nUnitsLen):
        self.nCount = nCount
        self.szServiceName = szServiceName
        self.nStarting = nStarting
        self.nPointIdLen = nPointIdLen
        self.nTimeLen = nTimeLen
        self.nStatusLen = nStatusLen
        self.nDescLen = nDescLen
        self.nUnitsLen = nUnitsLen
        self.dValue = None
        self.szPointId = None
        self.szTime = None
        self.szStatus = None
        self.szDesc = None
        self.szUnits = None


class Point(object):
    def __init__(self, szPoint, pdValue, nTime, nStatus, nDesc, nUnits):
        '''
        param szPoint the Real-Time point name. (const char *szPoint)
        param pdValue return the point value. (double *pdValue)
        param szTime return the point time. (char *szTime)
        param nTime the szTime reserved length. (unsigned short nTime)
        param szStatus return the point status. (char *szStatus)
        param nStatus the szStatus reserved length. (unsigned short nStatus)
        param szDesc return the point description. (char *szDesc)
        param nDesc the szDesc reserved length. (unsigned short nDesc)
        param szUnits return the point. (char *szUnits)
        param nUnits the szUnits reserved length. (unsigned short nUnits)
        '''
        self.szPoint = szPoint
        self.pdValue = pdValue
        self.nTime = nTime
        self.nStatus = nStatus
        self.nDesc = nDesc
        self.nUnits = nUnits
        self.szTime = "\0" * nTime
        self.szStatus = "\0" * nStatus
        self.szDesc = "\0" * nDesc
        self.szUnits = "\0" * nUnits

    def __str__(self):
        msg = "szPoint %s, pdValue %f, szTime %s, nTime %d " \
              ", szStatus %s, nStatus %d, szDesc %s, nDesc %d " \
              ", szUnits %s, nUnits %d " \
              % (self.szPoint, self.pdValue, self.szTime, self.nTime,
                 self.szStatus, self.nStatus, self.szDesc, self.nDesc,
                 self.szUnits, self.nUnits)
        return msg