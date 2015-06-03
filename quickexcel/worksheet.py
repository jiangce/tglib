# -*- coding: utf-8 -*-
'''
Created on 2012-5-21

@author: JC
'''

import re, pickle

maxcolumn = 0x4000
maxrow = 0x100000

class ExWorksheet(object):
    '''
    Worksheet的包装对象，对象中包含几个重要的字典：
    
    命名单元格定义字典：
    给指定的单元格赋予一个名称，使得用户可以通过名称查询单元格内容
    namedefinitions = {'name1':'a1','name2','b1'...}
    
    表格定义字典：
    给一个区域赋予一个表格名称，表格的第一行是列标题，第一列是行标题，可以利用行列标题定位单元格；
    表格可以分为有限表格和无限表格；
    有限表格定义左上角和右下角坐标，有限表的行列标题可以有空白；
    无限表格只定义左上角坐标，行列以空白为结束标志
    tabledefinitions = {

                            'tname1':('a1','f10'),
                            'tname2':('a12',)
                            ...
    }
    
    表格定位缓存：
    为加快访问速度，对已经定位过的行列缓存其地址
    tablecache = {
                    'tname1':(
                                {'row1':'2', 'row2':'3', ...},
                                {'column1':'B', column1':'C', ...}
                    )
                    'tname2':(
                                ...
                    )
    }
    
    表格范围缓存：
    该缓存记录所有表格的范围，减少无限表格的遍历次数
    tablescopecache = {
                        'tname1':('a1','f10'),
                        'tname2':('a12','f22')
                        ...
    }
    '''
    patten = re.compile('^\$?[a-z]+\$?\d+$', re.I)
    pattenrow = re.compile('\$?\d+$', re.I)
    pattencolumn = re.compile('^\$?[a-z]+', re.I)
    
    @staticmethod
    def verifyposition(position):
        '测试excel单元地址格式的正确性，如果错误则抛出PositionMistake异常'
        if not ExWorksheet.patten.match(position):
            raise PositionMistake
        
    @staticmethod
    def getrowinaddr(position):
        '取出地址中的行号部分'
        ExWorksheet.verifyposition(position)
        return ExWorksheet.pattenrow.findall(position)[0]
        
    @staticmethod
    def getcolumninaddr(position):
        '取出地址中的列号部分'
        ExWorksheet.verifyposition(position)
        return ExWorksheet.pattencolumn.findall(position)[0]
    
    def __init__(self, exbook, worksheet):
        self.exbook = exbook
        self._sheet = worksheet
        self.namedefinitions = {}
        self.tabledefinitions = {}
        self.tablecache = {}
        self.tablescopecache = {}
        
    @property
    def sheetname(self):
        '返回该sheet的名称'
        return self._sheet.Name
        
    def setvalue(self, position, value):
        '为指定地址单元格赋值'
        ExWorksheet.verifyposition(position) 
        self._sheet.Range(str(position)).Value = value
        
    def getvalue(self, position):
        '获取指定地址单元格的值'
        ExWorksheet.verifyposition(position) 
        return self._sheet.Range(str(position)).Value
    
    def gettext(self, position):
        '获取指定地址单元格的显示文本'
        ExWorksheet.verifyposition(position) 
        return self._sheet.Range(str(position)).Text.strip()
    
    def setnamedef(self, name, position):
        '定义一个命名单元格'
        ExWorksheet.verifyposition(position)            
        self.namedefinitions[name] = position
        
    def settabledef(self, name, ltposition, rbposition=None):
        '定义一个表格'
        ExWorksheet.verifyposition(ltposition)
        #如果指定了右下角坐标，则必须符合格式规范
        if rbposition:
            ExWorksheet.verifyposition(rbposition)
        self.tabledefinitions[name] = (ltposition, rbposition)
        
    def setnamevalue(self, name, value):
        '给一个命名单元格设置值'
        position = self.namedefinitions.get(name)
        if position:
            self.setvalue(position, value)
            
    def getnamevalue(self, name):
        '获取一个命名单元格的值'
        position = self.namedefinitions.get(name)
        if position:
            return self.getvalue(position)
        
    def getnametext(self, name):
        '获取一个命名单元格的显示文本'
        position = self.namedefinitions.get(name)
        if position:
            return self.gettext(position)

    def gettablescope(self, tablename):
        '查询并缓存表的实际范围'
        #如果找不到表定义，则返回空
        scope = self.tabledefinitions.get(tablename)
        if not scope:
            return
        #如果已有缓存，则返回缓存内容
        cachescope = self.tablescopecache.get(tablename)
        if cachescope:
            return cachescope
        #没有缓存，如果是有限表，则直接将表范围缓存
        if scope[1]:
            self.tablescopecache[tablename] = scope
            return scope
        #对于无限表，则从左上角开始分别遍历行和列，直到遇见空文本单元格，获取右下角地址后缓存并返回
        rg = self._sheet.Range(scope[0])
        row = rg.Row
        col = rg.Column
        for i in range(1 + row, maxrow + 1):
            v = self._sheet.Cells(i, col).Text.strip()
            if not v:
                break
        for j in range(1 + col, maxcolumn + 1):
            v = self._sheet.Cells(row, j).Text.strip()
            if not v:
                break
        cachescope = (scope[0], self._sheet.Cells(i - 1, j - 1).Address)
        self.tablescopecache[tablename] = cachescope
        return cachescope
    
    def cachetable(self, tablename):
        '''对一张表进行缓存，这样可以防止findtablecell方法多次反复扫描；
        该方法同时可以对地址缓存进行刷新，注意：但它不会刷新表范围缓存'''
        #返回表的范围，如果为空则返回
        scope = self.gettablescope(tablename)
        if not scope:
            return
        #将表的缓存置为空字典
        rows = {}
        columns = {}
        self.tablecache[tablename] = (rows, columns)
        #获得表范围的行列坐标
        rg1 = self._sheet.Range(scope[0])
        rg2 = self._sheet.Range(scope[1])
        row1 = rg1.Row
        col1 = rg1.Column
        row2 = rg2.Row
        col2 = rg2.Column
        #将表中每个坐标保存入缓存
        for i in range(row1 + 1, row2 + 1):
            addr = self._sheet.Cells(i , col1).Address
            rowname = self._sheet.Cells(i, col1).Text.strip()
            rows[rowname] = ExWorksheet.getrowinaddr(addr)
        for j in range(col1 + 1, col2 + 1):
            addr = self._sheet.Cells(row1 , j).Address
            columnname = self._sheet.Cells(row1, j).Text.strip()
            columns[columnname] = ExWorksheet.getcolumninaddr(addr)
                
                
    def cachealltable(self):
        '重新缓存所有表'
        for t in self.tabledefinitions:
            self.cachetable(t)
    
    def findtablecell(self, tablename, rowname, columnname):
        '通过表和行列名称返回单元格的地址，如果没有缓存则先进行缓存扫描'
        #返回表的范围，如果范围为空则返回空
        scope = self.gettablescope(tablename)
        if not scope:
            return
        #查找表格缓存，如果没有找到，则进行缓存
        if not self.tablecache.get(tablename):
            self.cachetable(tablename)
        #从缓存字典中搜索行列名称，如果存在则返回地址
        rc = self.tablecache[tablename]
        rowaddr = rc[0].get(rowname)
        columnaddr = rc[1].get(columnname)
        if rowaddr and columnaddr:
            return columnaddr+rowaddr

    
    def cleartablecache(self):
        '清除缓存'
        self.tablecache = {}
        self.tablescopecache = {}
        
    def gettablevalue(self, tablename, rowname, columnname):
        '通过表格地址获取单元格的值'
        pos = self.findtablecell(tablename, rowname, columnname)
        if pos:
            return self.getvalue(pos)
    
    def gettabletext(self, tablename, rowname, columnname):
        '通过表格地址获取单元格的文本'
        pos = self.findtablecell(tablename, rowname, columnname)
        if pos:
            return self.gettext(pos)
        
    def settablevalue(self, tablename, rowname, columnname, value):
        '通过表格地址设置单元格的值'
        pos = self.findtablecell(tablename, rowname, columnname)
        if pos:
            return self.setvalue(pos, value)
        
    def gettablerowtitles(self, tablename):
        '获取表的行标题列表'
        #返回表的范围，如果为空则返回
        scope = self.gettablescope(tablename)
        if not scope:
            return
        titles = []
        rg1 = self._sheet.Range(scope[0])
        rg2 = self._sheet.Range(scope[1])
        row1 = rg1.Row
        col1 = rg1.Column
        row2 = rg2.Row
        for i in range(row1 + 1, row2 + 1):
            titles.append(self._sheet.Cells(i, col1).Text.strip())
        return titles
            
    def gettablecolumntitles(self, tablename):
        '获取表的列标题列表'
        #返回表的范围，如果为空则返回
        scope = self.gettablescope(tablename)
        if not scope:
            return
        titles = []
        rg1 = self._sheet.Range(scope[0])
        rg2 = self._sheet.Range(scope[1])
        row1 = rg1.Row
        col1 = rg1.Column
        col2 = rg2.Column
        for j in range(col1 + 1, col2 + 1):
            titles.append(self._sheet.Cells(row1, j).Text.strip())
        return titles
        
    def savedefinitions(self, filename):
        '''保存该sheet中定义的所有命名单元格和表格；
        filename指定的文件如果存在，则会先读取该文件并替换其中的相关部分；
        其他部分会保持不变；
        文件保存的对象是一个字典：
        key：sheet名称
        value：一个元组，类似(self.namedefinitions,self.tabledefinitions)'''
        try:
            f = open(filename)
            d = pickle.load(f)
            f.close()
        except:
            d = {}
        d[self.sheetname] = (self.namedefinitions, self.tabledefinitions)
        f = open(filename, 'w')
        pickle.dump(d, f)
        f.close()
        
    def loaddefinitions(self, filename, sheetname=None):
        '''读取保存在文件中的命名单元和表格
        如果sheetname==None，则搜索和该sheet同名的字典项'''
        key = self.sheetname if (not sheetname) else sheetname
        f = open(filename)
        d = pickle.load(f)
        f.close()
        tu = d.get(key)
        self.namedefinitions = tu[0]
        self.tabledefinitions = tu[1]

    def __del__(self):
        del self._sheet
              
        
class PositionMistake(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
