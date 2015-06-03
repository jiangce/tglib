# -*- coding: utf-8 -*-

from win32com.client import Dispatch


class PISDK(object):
    sdk = Dispatch('PISDK.PISDK')

    def __init__(self):
        self.server = PISDK.sdk.Servers.DefaultServer
        self.isOpen = False

    def __enter__(self):
        self.openConnect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnect()

    def openConnect(self):
        try:
            if not self.isOpen:
                self.server.Open()
                self.isOpen = True
        except:
            self.closeConnect()

    def closeConnect(self):
        try:
            self.server.Close()
        finally:
            self.isOpen = False

    def getPoints(self):
        result = []
        for p in self.server.PIPoints:
            result.append((p.Name,
                           p.PointAttributes.Item('Descriptor').Value,
                           p.PointAttributes.Item('EngUnits').Value))
        return result

    def getValue(self, tag):
        p = self.server.PIPoints(tag)
        return tag, p.Data().Value, p.Data().TimeStamp(), p.Data().IsGood()

    def getValues(self, tags):
        return [self.getValue(tag) for tag in tags]