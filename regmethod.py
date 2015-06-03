# -*- coding: utf-8 -*-
'''
用于注册方法的模块，形成字符串和方法的配对字典

Example：

register, get = factory()

@register('test')
def f():
   print('Hello world')

get('test')()
'''


def factory():
    '''
    产生注册方法和获取方法的工厂
    返回值: register, getter
    '''
    _dict = {}

    def register(*names):
        def addMethod(f):
            for name in names:
                _dict[name.strip()] = f
            return f

        return addMethod

    def getter(name):
        return _dict.get(name.strip())

    return register, getter


if __name__ == '__main__':
    register, get = factory()

    @register('test1', 'test2')
    def f():
        print('Hello world')

    get('test2')()
