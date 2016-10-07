#small script to prime pumps
import time
import serial

ser = serial.Serial(
                    port='/dev/tty.USA19H141P1.1',
                    baudrate=19200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                   )
if not ser.isOpen():
    ser.open()

pump_setup = ['0VOL ML\r', '1VOL ML\r', '2VOL ML\r']
pump_phases=['0PHN01\r','1PHN01\r', '2PHN01\r','0CLDINF\r','1CLDINF\r','2CLDINF\r','0DIRINF\r','1DIRINF\r','2DIRINF\r','0RAT1800MH\r','1RAT1800MH\r','2RAT1800MH\r', '0VOL5.0\r','1VOL5.0\r', '2VOL5.0\r','0DIA26.95MH\r','1DIA26.95MH\r', '2DIA26.95MH\r']

#rate = mls_to_deliver*(3600.0/delivery_time)  # mls/hour 300


for c in pump_setup:
    print(c)
    ser.write(c)
    time.sleep(.25)

for c in pump_phases:
    ser.write(c)
    time.sleep(.25)
   
for x in range(len(pump_setup)):
    y='%dRUN\r'%x
    print(y)
    ser.write(y)
    time.sleep(.25)
    

