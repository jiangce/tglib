# -*- coding: utf-8 -*-
'''
一个用于延迟执行方法的模块
'''


class Lazy(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.func(*self.args, **self.kwargs)


if __name__ == '__main__':
    import random

    f = Lazy(random.randint, 10, 100)
    print(f())