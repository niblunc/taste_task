#small script to prime pumps
import time
import serial
from psychopy import visual, core, data, gui, event, data, logging


monSize = [800, 600]
info = {}

info['port'] = '/dev/tty.USA19H141P1.1'
info['volume']='40'
info['time_sec']='5'

dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()

ser = serial.Serial(
                    port='/dev/tty.USA19H142P1.1',
                    baudrate=19200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                   )
if not ser.isOpen():
    ser.open()


time_sec = float(info['time_sec'])
print time
volume = float(info['volume'])
print volume
rate = volume*(3600.0/time_sec)  # mls/hour 300
print rate

pump_setup = ['0VOL ML\r', '1VOL ML\r', '2VOL ML\r']
pump_phases=['0PHN01\r','1PHN01\r', '2PHN01\r','0CLDINF\r','1CLDINF\r','2CLDINF\r','0DIRINF\r','1DIRINF\r','2DIRINF\r','0RAT%sMH\r'%rate,'1RAT%sMH\r'%rate,'2RAT%sMH\r'%rate,'0VOL%s\r'%volume,'1VOL%s\r'%volume, '2VOL%s\r'%volume,'0DIA26.95MH\r','1DIA26.95MH\r', '2DIA26.95MH\r']


for c in pump_setup:
    ser.write(c)
    time.sleep(.25)

for c in pump_phases:
    ser.write(c)
    time.sleep(.25)
   
for x in range(len(pump_setup)):
    y='%dRUN\r'%x
    ser.write(y)
    time.sleep(.25)
    

