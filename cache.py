# -*- coding: utf-8 -*-
'''
支持超时的缓存模块

Example：

get = factory()

def f(x,y):
   ## 实现f内部逻辑，并返回值
   return result

get('key1', Lazy(f, x, y), 5)
'''

import time
from lazy import Lazy


def factory():
   '''
   产生缓存存取方法的工厂
   返回值: getter
   '''
   _cache = {}

   def _clearTimeout(key):
      nonlocal _cache
      vs = _cache.get(key)
      if vs:
         value, timeout = vs
         if timeout != None and time.time() >= timeout:
            del _cache[key]


   def getter(key, o, timeout=None):
      '''
      对象缓存存取方法
      key：标识数值的键
      o：如果不是一个Lazy对象，则返回o本身值；如果是Lazy对象，则返回Lazy的执行结果
      timeout：计算超时的秒数
      '''
      _clearTimeout(key)
      if key in _cache.keys():
         return _cache[key][0]
      else:
         v = o() if isinstance(o, Lazy) else o
         _cache[key] = (v, time.time() + timeout if timeout != None else None)
         return v

   return getter


if __name__ == '__main__':
   x = 0

   def test():
      global x
      x += 1
      return x

   get = factory()
   for i in range(10):
      print(get('x', Lazy(test), 2))
      time.sleep(1)
