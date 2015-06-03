# -*- coding: utf-8 -*-
'''
汉字转拼音库
Created on 2012-7-2
@author: JC
'''

import sqlite3, os, copy


class Spell(object):
    '''
    汉字拼音转换类
    '''

    def __init__(self):
        self._dbname = os.path.join(os.path.dirname(__file__), 'hzspell.db3')
        self._connect = sqlite3.connect(self._dbname)
        self._cursor = self._connect.cursor()
        self._sql = 'select * from spell where hzchar=:hzchar'
        self._insert = 'insert into spell (hzchar,spell) values (:hzchar,:spell)'
        self._update = 'update spell set spell=:spell where hzchar=:hzchar'

    def _getspellstr(self, word):
        try:
            hzchar = ord(word)
        except:
            hzchar = ord(word.decode('utf-8'))
        query = self._cursor.execute(self._sql, {'hzchar': hzchar})
        lt = query.fetchall()
        try:
            return lt[0][1]
        except:
            return None

    def updatespell(self, word, spl):
        '''
        更新汉字拼音
        '''
        try:
            hzchar = ord(word)
        except:
            hzchar = ord(word.decode('utf-8'))
        param = {'hzchar': hzchar, 'spell': spl}
        s = self._getspellstr(word)
        if s:
            self._cursor.execute(self._update, param)
        else:
            self._cursor.execute(self._insert, param)
        self._connect.commit()

    def spell(self, word):
        '''
        拼写汉字
        '''
        spells = self._getspellstr(word)
        if not spells:
            return [(word, -1)]
        spells = spells.split('|')
        result = []
        for spell in spells:
            if spell[-1] in '1234':
                item = (spell[0:-1], int(spell[-1]))
            else:
                item = (spell, 0)
            result.append(item)
        return result

    def withouttone(self, word):
        '''
        拼写汉字，不带音调
        '''
        s = self.spell(word)
        return list(set([x[0] for x in s]))

    def firstletter(self, word):
        '''
        拼写汉字的首字母
        '''
        s = self.spell(word)
        return list(set([x[0][0] for x in s]))

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        del self

    def __del__(self):
        self._connect.close()


def update(word, spell):
    '更新拼音'
    with Spell() as sp:
        sp.updatespell(word, spell)


def spell(word):
    '拼写汉字'
    with Spell() as sp:
        return sp.spell(word)


def withouttone(word):
    '拼写汉字，不带音调'
    with Spell() as sp:
        return sp.withouttone(word)


def firstletter(word):
    '拼写汉字的首字母'
    with Spell() as sp:
        return sp.firstletter(word)


def assemble(spellfunc, words):
    '获取汉字句子的拼音拼写组合'
    _list = [spellfunc(x) for x in words]
    return _asseblelist(_list)


def _asseblelist(_list):
    if len(_list) == 0:
        return [[]]
    itemend = _list[-1]
    former = _asseblelist(_list[0:-1])
    result = []
    for l in former:
        for i in itemend:
            m = copy.copy(l)
            m.append(i)
            result.append(m)
    return result


if __name__ == '__main__':
    print(spell('中'))
    print(spell('中'))
    print(spell('ク'))
    print(spell('ク'))
    print(withouttone('中'))
    print(firstletter('中'))
    print(assemble(spell, '李华峰_姜策'))
    print(spell('j'))
    print(spell('Ｊ'))
    print(withouttone('j'))
    print(firstletter('2'))
    update('无', 'wu2')
    print(spell('无'))
