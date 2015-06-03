# -*- coding: utf-8 -*-

from ctypes import *


def trydecode(s):
    try:
        return s.decode('gbk')
    except:
        try:
            return s[:-1].decode('gbk')
        except:
            return s


class PIAPI(object):
    DLL_FILE = r'piapi32.dll'

    def __init__(self, servername):
        self.api = windll.LoadLibrary(PIAPI.DLL_FILE)
        self.servername = servername
        self.isOpen = False

    def __enter__(self):
        self.openConnect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeConnect()

    def openConnect(self):
        try:
            if not self.isOpen:
                self.isOpen = self.api.piut_connect(c_char_p(self.servername.encode('gbk'))) == 0
        except:
            self.isOpen = False

    def closeConnect(self):
        try:
            self.api.piut_disconnect()
        finally:
            self.isOpen = False

    def getPoints(self):
        result = []
        tagmask = c_char_p(b'*')
        found = pointer(c_int(0))
        tagname = c_char_p(b'\0' * 40)
        pt = pointer(c_int(0))
        numfound = pointer(c_int(0))
        success = self.api.pipt_wildcardsearch(tagmask, 0, found, tagname, 40, pt, numfound) == 0
        while success:
            r_pt = pt.contents.value
            r_tagname = trydecode(tagname.value).strip()
            descriptor = c_char_p(b'\0' * 40)
            r_desc = trydecode(descriptor.value).strip() if self.api.pipt_descriptor(r_pt, descriptor, 40) == 0 else ''
            engunitstring = c_char_p(b'\0' * 10)
            r_unit = trydecode(engunitstring.value).strip() \
                if self.api.pipt_engunitstring(pt.contents, engunitstring, 10) == 0 else ''
            result.append((r_pt, r_tagname, r_desc, r_unit))
            success = self.api.pipt_wildcardsearch(tagmask, 1, found, tagname, 40, pt, numfound) == 0
        return result

    def getValue(self, tag):
        tagname = c_char_p(tag.encode('gbk'))
        pt = pointer(c_int(0))
        if self.api.pipt_findpoint(tagname, pt) == 0:
            rval = pointer(c_float(0))
            istat = pointer(c_int(0))
            timedate = pointer(c_int(0))
            if self.api.pisn_getsnapshot(pt.contents.value, rval, istat, timedate) == 0:
                return pt.contents.value, tag, rval.contents.value, timedate.contents.value, istat.contents.value

    def getValues(self, tags):
        return [self.getValue(tag) for tag in tags]