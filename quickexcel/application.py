# -*- coding: utf-8 -*-
'''
Created on 2012-5-21

@author: JC

实现Excel基本功能的快速控制
'''

import win32com.client, os
from .workbook import ExWorkbook

class ExApp(object):
    'Excel Application对象的包装'
    def __init__(self):
        self._app = win32com.client.Dispatch("Excel.Application")
           
    def _getvisible(self):
        return bool(self._app.Visible)
  
    def _setvisible(self, value):
        self._app.Visible = bool(value)
        
    visible = property(_getvisible, _setvisible, None, '返回或设置Excel的显示属性')
        
    def getworkbooks(self):
        '返回一个字典，每一项的键是文档的名称，值是workbook的包装对象'
        return {b.Name:ExWorkbook(self, b) for b in self._app.Workbooks}
        
    def openworkbook(self, fullname):
        '通过文件的完整路径名，打开文档'
        return ExWorkbook(self, self._app.Workbooks.Open(fullname))

    def getworkbook(self, fullname):
        '打开Excel文件或者链接到已打开的Excel文件，返回一个ExWorkbook对象'
        d = self.getworkbooks()
        name = os.path.basename(fullname)
        wb = d.get(name)
        if not wb:
            wb = self.openworkbook(fullname)
        return wb
    
    def addworkbook(self):
        '添加一个新的文档'
        return ExWorkbook(self, self._app.Workbooks.Add())

    def iffileopened(self, name):
        '根据名称判断一个文档是否打开'
        name = name.lower()
        return any(((b.Name.lower() == name) for b in self._app.Workbooks))
    
    def closeall(self):
        '关闭所有文档'
        for exwb in self.getworkbooks().values():
            exwb.close()
    
    def quitapp(self):
        '退出excel'
        self._app.Quit()
        
    def __del__(self):
        del self._app
