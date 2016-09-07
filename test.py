import psychopy.app
from psychopy import visual, core, event, logging, data, misc, sound

import numpy as N
import sys,os,pickle
sys.path.insert(0, '/Users/nibl/Documents/pyserial-2.6')
sys.path.append('/Users/nibl/Documents/taste_task')
#import cv2
import socket
from socket import gethostname
import inspect
sys.path.append('/Users/nibl/Documents/taste_task/psychtask')
#import exptutils
#from exptutils import *
import datetime
import serial
import time

dev=serial.Serial(port='/dev/tty.USA19H142P1.1',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
print dev
if not dev.isOpen():
    dev.open()
subdata={}
clock=core.Clock()

trialcond=N.zeros(12).astype('int')
trialcond[0:6]=0     # water cue, water delivery
trialcond[6:12]=1    # juice cue, juice delivery
#made an array of 0s and 1s
stim_images=['bottled_water.jpg','tampico.jpg']
ntrials=len(trialcond)#set 24 trials
pump=N.zeros(ntrials)#0 array, length 24

N.random.shuffle(trialcond)#randomize conditions

# pump zero is neutral, pump 1 is juice
#this will need another pump built in
pump[trialcond==1]=1#set when which pump is supposed to pump


diameter=26.59
mls_to_deliver=0.5
delivery_time=2.0
cue_time=2.0
wait_time=2.0
rinse_time=2.0
swallow_time=2.0
rate = mls_to_deliver*(3600.0/delivery_time)  # mls/hour 900
trial_length=cue_time+delivery_time+wait_time+rinse_time+swallow_time

#pump_setup = ['0VOL ML\r', '1VOL ML\r']
#pump_phases=['0PHN01\r','1PHN01\r','0DIRINF\r','1DIRINF\r','0RAT900MH\r','1RAT900MH\r','0VOL0.5\r','1VOL0.5\r','0DIA26.95MH\r','1DIA26.95MH\r']
#
#for c in pump_setup:
#    dev.write(c)
#    time.sleep(.25)
#
#for c in pump_phases:
#    dev.write(c)
#    time.sleep(.25)

dev.write('0PHN01\r')
dev.write('1PHN01\r')
dev.write('0CLDINF\r')
dev.write('1CLDINF\r')
dev.write('0DIRINF\r')
dev.write('1DIRINF\r')
dev.write('0RAT900.0MH\r')
dev.write('1RAT900.0MH\r')
dev.write('0VOL0.5\r')
dev.write('1VOL0.5\r')
dev.write('0DIA26.6MH\r')
dev.write('1DIA26.6MH\r')

subdata['trialdata']={}
clock.reset()
event.clearEvents()
onsets=N.arange(0,ntrials*trial_length,step=trial_length)
print(onsets)
for trial in range(ntrials):#for trial in 24 trials
    trialdata={}
    print 'trial %d'%trial
    trialdata['onset']=onsets[trial]
    print 'condition %d'%trialcond[trial]

    print 'injecting via pump at address %d'%pump[trial]
    dev.write('%dRUN\r'%pump[trial])
       
    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):#wait until liquid is delivered
        pass
   
    trialdata['dis']=[dev.write('0DIS\r'),dev.write('1DIS\r')]
    print(trialdata['dis'])

    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
        pass

    
    print 'injecting rinse via pump at address %d'%0
    dev.write('%dRUN\r'%0)
    
        
    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time):
        pass


    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time+swallow_time):
        pass
    while clock.getTime()<(trialdata['onset']+trial_length):
        pass

    subdata['trialdata'][trial]=trialdata
f=open('Output/liquid_subdata_%s.pkl'%datestamp,'wb')
pickle.dump(subdata,f)
f.close()
