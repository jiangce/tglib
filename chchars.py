# -*- coding: utf-8 -*-
'''
汉字集
Created on 2012-7-2
@author: 姜策
'''

import sqlite3, os, copy


def zidict(*ziinfo):
    '''
    将一条汉字信息记录包装为字典
    顺序是'zi','py','py2','wb','bs','bh','jj','xj'
    '''
    return {'zi': ziinfo[0], 'py': ziinfo[1], 'py2': ziinfo[2],
            'wb': ziinfo[3], 'bs': ziinfo[4],
            'bh': ziinfo[5], 'jj': ziinfo[6], 'xj': ziinfo[7]}


_dbname = os.path.join(os.path.dirname(__file__), 'chchars.db')
_detailsql = 'select zi,py,py2,wb,bs,bh,jj,xj from chs where zi=:zi'
_pysql = 'select zi,py,py2 from chs where zi=:zi'
_insert = 'insert into chs (zi,py,py2,wb,bs,bh,jj,xj) values (:zi,:py,:py2,:wb,:bs,:bh,:jj,:xj)'
_update = 'update chs set py=:py,py2=:py2,wb=:wb,bs=:bs,bh=:bh,jj=:jj,xj=:xj where zi=:zi'


class ChChars(object):
    '''
    汉字拼音转换类
    '''

    def __init__(self):
        self._connect = sqlite3.connect(_dbname)
        self._cursor = self._connect.cursor()

    def _getzidata(self, zi, sql):
        if not zi: return None
        self._cursor.execute(sql, {'zi': zi})
        lt = self._cursor.fetchall()
        try:
            return lt[0]
        except:
            return None

    def getdetail(self, zi):
        '''
        获取汉字的详细信息
        '''
        ziinfo = self._getzidata(zi, _detailsql)
        if ziinfo:
            return zidict(*ziinfo)

    def getpy(self, zi):
        '''
        获取汉字的拼音信息
        '''
        ziinfo = self._getzidata(zi, _pysql)
        if ziinfo:
            return {'zi': ziinfo[0], 'py': ziinfo[1], 'py2': ziinfo[2]}

    def update(self, **ziinfo):
        '''
        更新汉字信息
        ziinfo是一个字典，keys={'zi','py','py2','wb','bs','bh','jj','xj'}
        其中'zi'是主键
        '''
        ziinfo['zi'] = ziinfo['zi']
        s = self.getpy(ziinfo['zi'])
        if s:
            self._cursor.execute(_update, ziinfo)
        else:
            self._cursor.execute(_insert, ziinfo)
        self._connect.commit()

    def spell(self, zi):
        '''
        拼写汉字
        '''
        pyinfo = self.getpy(zi)
        if pyinfo:
            return tuple(pyinfo['py'][1:-1].split('|'))

    def spell2(self, zi):
        '''
        拼写汉字带音调
        '''
        pyinfo = self.getpy(zi)
        if pyinfo:
            return tuple(pyinfo['py2'][1:-1].split('|'))

    def firstletter(self, zi):
        '''
        拼写汉字拼音首字母
        '''
        r = self.spell(zi)
        if r:
            return tuple(set(i[0] for i in r))

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        del self

    def __del__(self):
        self._connect.close()


def update(**ziinfo):
    '''更新拼音'''
    with ChChars() as sp:
        sp.update(**ziinfo)


def spell(zi):
    '''拼写汉字'''
    with ChChars() as sp:
        return sp.spell(zi)


def spell2(zi):
    '''带音调拼写汉字'''
    with ChChars() as sp:
        return sp.spell2(zi)


def firstletter(zi):
    '''拼写汉字的首字母'''
    with ChChars() as sp:
        return sp.firstletter(zi)


def detail(zi):
    '''获取汉字的详细信息'''
    with ChChars() as sp:
        return sp.getdetail(zi)


def spellsentence(spellfunc, ju):
    '''获取汉字句子的拼音拼写组合'''
    _list = []
    for zi in ju:
        py = spellfunc(zi)
        if py:
            _list.append(py)
        else:
            if len(_list) == 0 or isinstance(_list[-1], tuple):
                _list.append(zi)
            else:
                _list[-1] += zi
    return _list


def asseblelist(_list, zifunc=None, qtfunc=None):
    '''
    将句子的拼音按照多音字进行排列组合
    可以指定zifunc函数对于每个汉字拼音进行变换
    可以指定qtfunc函数对句子中非汉字进行变换
    '''
    if len(_list) == 0:
        return [[]]
    itemend = _list[-1]
    former = asseblelist(_list[0:-1], zifunc, qtfunc)
    result = []
    for l in former:
        if isinstance(itemend, tuple):
            for i in itemend:
                m = copy.copy(l)
                i = zifunc(i) if zifunc else i
                m.append(i)
                result.append(m)
        else:
            m = copy.copy(l)
            itemend = qtfunc(itemend) if qtfunc else itemend
            m.append(itemend)
            result.append(m)
    return result


if __name__ == '__main__':
    print(spell('说'))
    for i in spell2('说'):
        print(i)
    print(firstletter('说'))
    for i in detail('说').values():
        print(i)
    print(spellsentence(spell, 'lihuaf李华峰jiangce姜策'))
    print(spellsentence(firstletter, 'lihuaf李华峰jiangce姜策'))
    _list = spellsentence(spell, '12我和你34')
    print(_list)
    print(asseblelist(_list, lambda x: x.upper()))

    # ############以下代码从excel文件中导入数据############
    # import quickexcel
    #        app = quickexcel.ExApp()
    #        app.visible = True
    #        wb = app.getworkbook(r'f:\py.xlsx')
    #        ws = wb.getworksheet(0)
    #        for i in xrange(2, 20824):
    #            zi = ws.gettext('b%s' % i)
    #            py = ws.gettext('c%s' % i).replace(',', '|')
    #            py = '|' + py + '|'
    #            py2 = ws.gettext('g%s' % i).replace(',', '|')
    #            py2 = '|' + py2 + '|'
    #            wb = ws.gettext('d%s' % i).replace(' ', '')
    #            bs = ws.gettext('e%s' % i)
    #            bs = bs if len(bs) == 1 else None
    #            bh = int(ws.gettext('f%s' % i))
    #            jj = ws.gettext('h%s' % i)
    #            xj = ws.gettext('i%s' % i)
    #            update(**zidict(zi, py, py2, wb, bs, bh, jj, xj))
    #            print i,zi
