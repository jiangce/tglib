# -*- coding: utf-8 -*-

import struct
from pyModbusTCP.client import ModbusClient


class Modbus:
    def __init__(self, host, port, unit):
        self.client = ModbusClient(host, port, unit, timeout=3)

    def __enter__(self):
        self.client.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def toFloat(self, ushorts):
        bs = struct.pack('H', ushorts[0]) + struct.pack('H', ushorts[1])
        return struct.unpack('f', bs)

    def openConnect(self):
        try:
            if not self.isOpen:
                self.client.open()
        except:
            self.closeConnect()

    def closeConnect(self):
        self.client.close()

    @property
    def isOpen(self):
        return self.client.is_open()

    def getValue(self, addr):
        return self.toFloat(self.client.read_holding_registers(addr, 2))[0]

    def getValues(self, tags):
        return [(tag, self.getValue(tag)) for tag in tags]
