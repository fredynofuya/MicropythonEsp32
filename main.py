#Libraries:
import network
import time
import ubinascii
import machine
import urequests
import _thread
#SPI library
from machine import SPI, Pin
from machine import sleep
import max6675
#I2C library
from machine import Pin, I2C
from BMI160 import BMI160_I2C
from time import sleep_ms
#UART library
from machine import UART
from pms7003 import Pms7003
#PWM library
from machine import Pin, PWM
#LCD library
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
#JSON library
import json

#For LCD:
I2C_ADDR = 0x27 #LCD slave address
totalRows = 4
totalColumns = 20

#For UBIDOTS:
token_ubi = 'BBFF-YA3RbMGvQYUZ0nAkWCFP3H5Sj7bZp9'
ubi_url = 'http://industrial.api.ubidots.com'
ubi_dev = '/api/v1.6/variables/'
var_id_W = '6315923c108bc324a6d9b44c' #write the uC //Temp
var_id_W1 = '63182773b683c943955ba069' #write the uC //Acelx
var_id_W2 = '6318277a72505c72443df34b' #write the uC //Acely
var_id_W3 = '63159311b2ffac445d2dce45' #write the uC //Acelz
var_id_W4 = '6315932c2d7cba4e1957e24f' #write the uC //PM2.5
var_id_R = '63159348b2ffac432b43858b'#read the uC//Motor: Speed
var_id_R1 = '632206d78dc57f1956991ee2'#read the uC//Motor: Sense
get_cmd = '/values/?page_size=1'
put_cmd = '/values'

#Function for motor control
def control(sense,duty):
    # parameters assigned to local variables
    sense = sense
    duty = duty
    # function logic for motor 
    if sense == "1":
        # set the sense of rotation  
        in1a.value(0)
        in1b.value(1)
        # set the speed of rotation
        pwm.duty(duty)
    
    elif sense == "0":
        # set the sense of rotation
        in1a.value(1)
        in1b.value(0)
        # set the speed of rotation
        pwm.duty(duty)

# Setup WiFi connection and IP:
class ip_wife:
    def wifi_connect(ssid='Redmi Note 8 Pro', key= 'juanma20'):
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            if not wlan.isconnected():
                print('connecting to network...')
                wlan.connect(ssid, key)
                while not wlan.isconnected():
                    time.sleep_ms(50)
        except Exception as e:
            print('[ERR] problem wifi_connect(): {}'.format(str(e)))
    
    def IP():
        wlan = network.WLAN(network.STA_IF)
        sta1=list(wlan.ifconfig())
        sta=sta1[0]
        return sta
 
# POST HTTTP(s) request
#For temperature
def http_write_data(dat):
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        json_data = {"value":dat}
        while response >= 400 and attemps <=5:
            http_request = urequests.post(url=ubi_url + ubi_dev + var_id_W + put_cmd,
                headers = headers, json = json_data)
            response = http_request.status_code
            print('[INFO W] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO W] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR W] Not response from server')
    except Exception as e:
        print('[ERR W] Exception: ' + str(e))

#For Acceleration X
def http_write_data1(dat):
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        json_data = {"value":dat}
        while response >= 400 and attemps <=5:
            http_request = urequests.post(url=ubi_url + ubi_dev + var_id_W1 + put_cmd,
                headers = headers, json = json_data)
            response = http_request.status_code
            print('[INFO W] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO W] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR W] Not response from server')
    except Exception as e:
        print('[ERR W] Exception: ' + str(e))
        
#For Acceleration Y
def http_write_data2(dat):
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        json_data = {"value":dat}
        while response >= 400 and attemps <=5:
            http_request = urequests.post(url=ubi_url + ubi_dev + var_id_W2 + put_cmd,
                headers = headers, json = json_data)
            response = http_request.status_code
            print('[INFO W] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO W] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR W] Not response from server')
    except Exception as e:
        print('[ERR W] Exception: ' + str(e))
        
#For Acceleration Z
def http_write_data3(dat):
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        json_data = {"value":dat}
        while response >= 400 and attemps <=5:
            http_request = urequests.post(url=ubi_url + ubi_dev + var_id_W3 + put_cmd,
                headers = headers, json = json_data)
            response = http_request.status_code
            print('[INFO W] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO W] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR W] Not response from server')
    except Exception as e:
        print('[ERR W] Exception: ' + str(e))

#Particulate Matter 2.5
def http_write_data4(dat):
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        json_data = {"value":dat}
        while response >= 400 and attemps <=5:
            http_request = urequests.post(url=ubi_url + ubi_dev + var_id_W4 + put_cmd,
                headers = headers, json = json_data)
            response = http_request.status_code
            print('[INFO W] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO W] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR W] Not response from server')
    except Exception as e:
        print('[ERR W] Exception: ' + str(e))
        
#GET HTTTP(s) request
#For DC MOTOR Direction
def http_read_data():
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        while response >= 400 and attemps <=5:
            http_request = urequests.get(url=ubi_url + ubi_dev + var_id_R + get_cmd,
                headers = headers)
            response = http_request.status_code
            print('[INFO R] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO R] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR R] Not response from server')
    except Exception as e:
        print('[ERR R] Exception hhtp_read_data: ' + str(e))
    return http_request.json()

#For DC MOTOR speed       
def http_read_data1():
    try:
        headers = {'X-Auth-Token':token_ubi, "Content-Type": "application/json"}
        attemps = 0 # Try to do the request for sometimes
        response = 400 # Failed http request
        while response >= 400 and attemps <=5:
            http_request = urequests.get(url=ubi_url + ubi_dev + var_id_R1 + get_cmd,
                headers = headers)
            response = http_request.status_code
            print('[INFO R] http response code: {}'.format(response))
            # Print the data of volume
            print('[INFO R] http response text: {}'.format(http_request.text))
            attemps = attemps + 1
        if attemps == 5:
            print('[ERR R] Not response from server')
    except Exception as e:
        print('[ERR R] Exception hhtp_read_data: ' + str(e))
    return http_request.json()

#For reading the speed and direction of the DC motor
def read_var():
    while True:
        print("************************************")
        http_read_data()
        hv=http_read_data()
        hv=hv['results']
        hv=hv[0]
        speed=(hv['value']) #Speed ​​value capture
        print("************************************")
        http_read_data1()
        hv2=http_read_data1()
        hv2=hv2['results']
        hv2=hv2[0]
        hv2=int(hv2['value'])
        sense=str(hv2) #Sense ​​value capture
        print("************************************")
        if sense=="1":
            print("The sense is: Right")
            print("The speed is: {}".format(speed))
        else:
            print("The sense is: Left")
            print("The speed is: {}".format(speed))
        print("************************************")
        duty = int((speed * 1023) / 100) #Duty motor
        control(sense,duty)
        time.sleep(3)

#UART Communication:PM
pms = Pms7003(uart=1)
pms_data = pms.read()

#I2C Communication:Accelerometer
i2c = I2C(sda=Pin(8), scl=Pin(9), freq=400000)
bmi160 = BMI160_I2C(i2c) #Direction 1  Hex:x69
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns) #Direction 2 Hex:x27

#SPI Communication:Temperature
spi = SPI(1, baudrate=4300000, polarity=0, phase=0, sck=Pin(36), mosi=Pin(35), miso=Pin(37))
mx= max6675.MAX6675()

#For Motor DC
# pin declarations
en = Pin(45, Pin.OUT)
in1a = Pin(42, Pin.OUT)
in1b = Pin(41, Pin.OUT)

# set pwm object for the motor at 25 Hz
# for motor 
pwm = PWM(en)
pwm.freq(25)
    
#Main
if __name__ == '__main__':
    print('HTTP(s) example')
    ip_wife.wifi_connect() 
    IP=ip_wife.IP()
    _thread.start_new_thread(read_var, ())
    while True:
        lcd.clear() #LCD clear 
        lcd.move_to(0,0)
        lcd.putstr("IP:")
        lcd.move_to(3,0)
        lcd.putstr(IP)
        
        """The Temperature variable is printed in UBIDOTS and LCD 
        """
        lcd.move_to(0,1)
        lcd.putstr("T:")
        print("***************** Temperature UBI:{} °C" .format(int(mx.readCelsius())))
        http_write_data(int(mx.readCelsius()))
        lcd.move_to(2,1)
        t=mx.readCelsius()
        t2=str(t)
        lcd.putstr(t2)
        print("***************** Temperature LCD:{} °C" .format(t2))
        sleep_ms(1000)
        
        """The PM2.5 variable is printed in UBIDOTS and LCD: 
        """
        lcd.move_to(0,2)
        lcd.putstr("P2.5:")
        print("*** PM2.5:{} ugm3" .format(pms_data['PM2_5']))
        http_write_data4(pms_data['PM2_5'])
        lcd.move_to(5,2)
        pm25=pms_data['PM2_5']
        pm25s=str(pm25)
        lcd.putstr(pm25s)
        sleep_ms(1000)
        
        """The PM10 variable is printed in LCD: 
        """
        lcd.move_to(9,2)
        lcd.putstr("P10:")
        print("*** PM10:{} ugm3" .format(pms_data['PM10_0']))
        lcd.move_to(13,2)
        pm10=pms_data['PM10_0']
        pm10s=str(pm10)
        lcd.putstr(pm10s)
        sleep_ms(1000)
        
        """The Acceleration X variable is printed in UBIDOTS and LCD: 
        """
        lcd.move_to(0,3)
        lcd.putstr("X:")
        print("Acceleration X:{} ms2" .format(*bmi160.getAccelerationX()))
        http_write_data1(*bmi160.getAccelerationX())
        lcd.move_to(2,3)
        x=bmi160.getAccelerationX()
        x1=x[0]
        x2=str(x1)
        lcd.putstr(x2)
        sleep_ms(1000)
        
        """The Acceleration Y variable is printed in UBIDOTS and LCD: 
        """
        lcd.move_to(6,3)
        lcd.putstr("Y:")
        print("Acceleration y:{} ms2" .format(*bmi160.getAccelerationY()))
        http_write_data2(*bmi160.getAccelerationY())
        lcd.move_to(8,3)
        y=bmi160.getAccelerationY()
        y1=y[0]
        y2=str(y1)
        lcd.putstr(y2)
        sleep_ms(1000)
        
        """The Acceleration Z variable is printed in UBIDOTS and LCD:  
        """
        lcd.move_to(13,3)
        lcd.putstr("Z:")
        print("Acceleration z:{} ms2" .format(*bmi160.getAccelerationZ()))
        http_write_data3(*bmi160.getAccelerationZ())
        lcd.move_to(15,3)
        z=bmi160.getAccelerationZ()
        z1=z[0]
        z2=str(z1)
        lcd.putstr(z2)
        lcd.hal_sleep_us(5000000) #2 seconds:LCD
