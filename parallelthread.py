# -*- coding: utf-8 -*-

from threading import Thread
from math import ceil


class Pool(object):
    def __init__(self, method, argsmap, threadcount):
        self.method = self._wrapmethod(method)
        self.argsmap = argsmap
        self.threadcount = threadcount

    def _wrapmethod(self, method):
        def innerMethod(*args):
            for arg in args:
                method(arg)

        return innerMethod

    def _div(self):
        size = len(self.argsmap)
        c = int(ceil(float(size) / self.threadcount))
        return [self.argsmap[i:i + c] for i in range(0, size, c)]

    def start(self):
        threads = []
        for subargmap in self._div():
            t = Thread(target=self.method, args=subargmap)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()


if __name__ == '__main__':
    import time

    def test(i):
        print('[%s]' % i)
        time.sleep(2)

    pool = Pool(test, range(20), 3)
    pool.start()
