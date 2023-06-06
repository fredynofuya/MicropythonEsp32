import machine
import struct

class Pms7003:

    START_BYTE_1 = 0x42 #start byte to conection
    START_BYTE_2 = 0x4d #start byte to conection
    PMS_PM2_5 = 2 #Position to Pm 2.5
    PMS_PM10_0 = 3 #Position to Pm 10

    def __init__(self, uart): #Begin the Uart
        self.uart = machine.UART(uart, baudrate=9600, bits=8, parity=None, stop=1)
        #Begin Uart in 8N1
    @staticmethod
    def _check_byte(byte, expected):#To check if the start uart is ok
        if byte is None or len(byte) < 1 or ord(byte) != expected: # if start is ok
            return False #False if start is no ok
        return True # True if start is ok

    def read(self):

        while True:

            first_byte = self.uart.read(1) # Get first Start byte
            if not self._check_byte(first_byte, Pms7003.START_BYTE_1): #Compare first byte start whit the check_byte
                continue

            second_byte = self.uart.read(1)# Get second Start byte
            if not self._check_byte(second_byte, Pms7003.START_BYTE_2):#Compare second byte whit the check_byte
                continue

            # we are reading 30 bytes left
            read_bytes = self.uart.read(30) # Get all of datas (30) from Pms sensor
            if len(read_bytes) < 30: #check if all of datas is done
                continue

            data = struct.unpack('!HHHHHHHHHHHHHBBH', read_bytes) #Unpack from the buffer read_bytes, and get the tuple whith the values

            return {
                'PM2_5': data[Pms7003.PMS_PM2_5], #Get pm 2.5 from data
                'PM10_0': data[Pms7003.PMS_PM10_0], #Get pm 10 from data

            }