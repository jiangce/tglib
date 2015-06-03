# -*- coding: utf-8 -*-
'''
用于将数字转换为中文表示法
Created on 2012-6-30
@author: JC
'''

import decimal

decimal.getcontext().prec = 32


class HZNumberConverter(object):
    '''
    将数字转换为中文表示法的类
    设置实例对象的Number属性，并调用toString()方法
    '''
    _s1 = ['', '拾', '佰', '仟']
    _s2 = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']

    def __init__(self, num):
        '传递一个数字初始化一个转换对象'
        self.Number = decimal.Decimal(str(num))

    @property
    def Number(self):
        return self._number

    @Number.setter
    def Number(self, value):
        self._number = decimal.Decimal(str(value))

    def _getIntegralPart(self):
        '返回数字的整数部分'
        return abs(int(self.Number))

    def _getDecimalPart(self):
        '返回数字的小数部分'
        return abs(self.Number) - self._getIntegralPart()

    def _isInteger(self):
        '指示数字是否是整数'
        return self._getDecimalPart() == 0

    def toString(self, RMB=False):
        '''
        返回中文表示法
        RMB若为True，则以人民币方式表示
        '''
        if self.Number < 0:
            return '负' + self._getAbsolute(RMB)
        else:
            return self._getAbsolute(RMB)

    def _getAbsolute(self, RMB):
        intp = self._getIntegralPart()
        isint = self._isInteger()
        result = self._convert16(intp)

        if RMB:
            result += '圆'
            result += '整' if isint else self._convertDecimal(RMB)
        elif not isint:
            result += '点' + self._convertDecimal(RMB)
        return result

    def _convertDecimal(self, RMB):
        num = self._getDecimalPart()
        result = ''

        def decbit(n, i):
            return int(n * pow(10, i) % 10)

        if RMB:
            b = decbit(num, 1)
            if b != 0:
                result += HZNumberConverter._s2[b] + '角'
            b = decbit(num, 2)
            if b != 0:
                result += HZNumberConverter._s2[b] + '分'
            b = decbit(num, 3)
            if b != 0:
                result += HZNumberConverter._s2[b] + '厘'
        else:
            d = 10 * num % 10
            while d != 0:
                b = int(d)
                result += HZNumberConverter._s2[b]
                d = 10 * d % 10
        return result

    def _convert4(self, num):
        if num < 0:
            raise NumberOutException
        if num == 0:
            return '零'
        if num >= 10000:
            return self._convert8(num)
        nx, lt, s, i = num, 0, '', 0
        while True:
            bit = nx % 10
            if bit == 0:
                if lt != 0:
                    s = '零' + s
            else:
                s = HZNumberConverter._s2[bit] + HZNumberConverter._s1[i] + s
            lt = bit
            i += 1
            nx //= 10
            if nx == 0:
                break
        return s

    def _convert8(self, num):
        if num < 10000:
            return self._convert4(num)
        if num >= 10 ** 8:
            return self._convert16(num)
        if num % 10000 == 0:
            return self._convert4(num // 10000) + '万'
        if num % 10000 // 1000 == 0:
            return self._convert4(num // 10000) + '万零' + self._convert4(
                num % 10000)
        else:
            return self._convert4(num // 10000) + '万' + self._convert4(
                num % 10000)

    def _convert16(self, num):
        if num < 10 ** 8:
            return self._convert8(num)
        if num >= 10 ** 16:
            raise NumberOutException
        if num % 10 ** 8 == 0:
            return self._convert8(num // 10 ** 8) + '亿'
        if num % 10 ** 8 // 10 ** 7 == 0:
            return self._convert8(num // 10 ** 8) + '亿零' + self._convert8(
                num % 10 ** 8)
        else:
            return self._convert8(num // 10 ** 8) + '亿' + self._convert8(
                num % 10 ** 8)


class NumberOutException(Exception):
    pass


_converter = HZNumberConverter(0)


def convert(num, RMB=False):
    '''
    直接将数字转换为汉字的方法，不需要手动创建转换对象
    '''
    _converter.Number = num
    return _converter.toString(RMB)


if __name__ == '__main__':
    print(convert('0'))
    print(convert('0', True))
    print('-' * 20)
    print(convert('100.2'))
    print(convert('100.2', True))
    print('-' * 20)
    print(convert(10000))
    print(convert(10000, True))
    print('-' * 20)
    print(convert(100000000001))
    print(convert(100000000001, True))
    print('-' * 20)
    print(convert(-9876543210.0123456789))
    print(convert('-9876543210.0123456789'))
    print('-' * 20)
    print(convert('0000.000000000000000000000000000000000000000000000000000001'))
    print(convert('0000.000000000000000000000000000000000000000000000000000001', True))
    print('-' * 20)
    print(convert(10 ** 15 + 1))
    print(convert(10 ** 16 - 1))