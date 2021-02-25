import re
import struct
import binascii
from crccheck.crc import Crc8, Crc8Maxim
from crccheck.checksum import Checksum8

class data:
    # def __init__(self):
    #     self.a_random_arg = a_random_arg
    #     display(self)

    @staticmethod
    def getInt(val, typeChar='>'):
        encodedData = val.encode()
        encodedDataLen = len(encodedData)

        # @ Native
        # = Standard
        # < Little Endian
        # > Big Endian
        # ! Network
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
    def getCRC(val):
        crcinst = Crc8Maxim()
        crcinst.process(val)
        crchex = crcinst.finalhex().upper()
        return crchex


    @staticmethod
    def getFahrenheit(val):
        return round((val * (9/5)) + 32, 2)
