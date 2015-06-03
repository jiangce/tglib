# -*- coding: utf-8 -*-
import sys


class MemOut:
    def __init__(self):
        self._buffer = []

    def write(self, buf):
        self._buffer.append(buf)

    @property
    def buffer(self):
        return ''.join(self._buffer)


class OutContext:
    def __init__(self, out=MemOut()):
        self._out = out
        self._temp_output = sys.stdout

    def __enter__(self):
        sys.stdout = self._out
        return self._out

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self._temp_output


if __name__ == '__main__':
    with OutContext() as out:
        print('123')
        print('456')
    print('-' * 10)
    print(out.buffer)
