# -*- coding: utf-8 -*-
'''
Created on 2012-5-21

@author: JC
'''
from .application import *

if __name__ == '__main__':
    app = ExApp()
    app.visible = True

    wb = app.openworkbook(r'f:\1.xlsx')
    ws = wb.getworksheet(0)
    ws.setnamedef('test', 'g8')
    ws.setnamevalue('test', '姜策，你好')
    print(ws.getnametext('test'))

    ws.settabledef('ttest', 'a1')
    print(ws.gettablescope('ttest'))
    ws.savedefinitions(r'f:\1.config')
