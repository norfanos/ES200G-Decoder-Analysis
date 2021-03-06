import re
import struct
import binascii
from crccheck.crc import Crc8, Crc8Maxim
from crccheck.checksum import Checksum8

class data:
    # def __init__(self):
    #     self.a_random_arg = a_random_arg
    #     display(self)
    #
    @staticmethod
    def signed(n):
        if n >= 0x8000:
            n -= 0x10000
        return n

    # @classmethod


    # @ Native
    # = Standard
    # < Little Endian
    # > Big Endian
    # ! Network
    @staticmethod
    def getInt(val, typeChar='<'):
        return data.getUnsignedInt(val, typeChar=typeChar)


    @staticmethod
    def getUnsignedInt(val, typeChar='>'):
        encodedData = val.encode()
        encodedDataLen = len(encodedData)

        s = struct.Struct(typeChar + ' ' + str(encodedDataLen) + 's')
        packedData = s.pack(encodedData)

        if typeChar == '<':
            f = lambda n:n.to_bytes(int(encodedDataLen/2), "little").hex()
        else:
            f = lambda n:n.to_bytes(int(encodedDataLen/2), "big").hex()

        lsbVal = f(int(packedData, 16))

        return int(lsbVal, 16)


    @staticmethod
    def getIntLE(val):
        return data.getInt(val=val, typeChar='<')


    @staticmethod
    def getUnsighedIntLE(val):
        return data.getUnsignedInt(val=val, typeChar='<')


    @staticmethod
    def getCRC(val):
        crcinst = Crc8Maxim()
        crcinst.process(val)
        crchex = crcinst.finalhex().upper()
        return crchex


    @staticmethod
    def getFahrenheit(val):
        return round((val * (9/5)) + 32, 2)
