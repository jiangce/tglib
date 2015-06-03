# -*- coding: utf-8 -*-
'''
Created on 2012-5-21

@author: JC
'''

import os, win32com.client
from .worksheet import ExWorksheet

class ExWorkbook(object):
    '文档类Workbook的包装'
    def __init__(self, exapp, workbook):
        self.exapp = exapp
        self._book = workbook
        
    def getname(self):
        '返回文档的名称'
        return self._book.Name

    def getfullname(self):
        '返回文档的全路径名'
        return self._book.FullName
    
    def getworksheets(self):
        '返回一个字典，每一项的键是sheet的名称，值是sheet的包装对象'
        return {s.Name:ExWorksheet(self, s) for s in self._book.Worksheets}

    def getworksheet(self, nameindex):
        '通过索引或名称返回一个sheet的包装对象'
        try:
            return ExWorksheet(self, self._book.Worksheets(nameindex))
        except:
            index = int(nameindex)
            return ExWorksheet(self, self._book.Worksheets[index])
            
    
    def containsworksheet(self, name):
        '判断当前文档是否包含指定名称的sheet'
        l = (s.Name for s in self._book.Worksheets)
        return name in l
       
    def insertworksheet(self, name):
        '''在当前文档中插入新的sheet，并返回其包装对象；
        如果有重名，将返回该名称的sheet包装对象'''
        if self.containsworksheet(name):
            return self.getworksheet(name)
        sheet = self._book.Sheets.Add()
        sheet.Name = name
        return ExWorksheet(self, sheet)
        
    def save(self):
        '保存文档'
        self._book.Save()
    
    def saveas(self, fullname):
        '文档另存为'
        ext = os.path.splitext(fullname)[1].lower()
        if ext == '.xlsx':
            self._book.SaveAs(fullname)
        elif ext == '.xlsm':
            self._book.SaveAs(fullname, win32com.client.constants.xlOpenXMLWorkbookMacroEnabled)
        elif ext == '.xlsb':
            self._book.SaveAs(fullname, win32com.client.constants.xlExcel12)
        elif ext == '.xls':
            self._book.SaveAs(fullname, win32com.client.constants.xlExcel8)
        else:
            raise NotImplementedError
        
    def close(self):
        '关闭文档'
        self._book.Close()
        if not len(self.exapp.getworkbooks()):
            self.exapp.quitapp()
            
    def __del__(self):
        del self._book
