#####to run, in shell window <execfile("pump_test.py"), it initially doesn't work run via gui, then close and run cmdline##################################################
import psychopy.app
import numpy as N
import sys,os,pickle
sys.path.insert(0, '/Users/nibl/Documents/pyserial-2.6')
#####THIS IS IMPORTANT DON'T MESS WITH IT#######
sys.path.append('/Users/nibl/Documents/taste_task')
import cv2
import syringe_pump
from psychopy import visual, core, event, logging, data, misc, sound
import socket
from socket import gethostname
import inspect
sys.path.append('/Users/nibl/Documents/taste_task/psychtask')
import exptutils
from exptutils import *
import datetime
subdata={}
#where to save the data 
subdata['subcode']='test'
datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
subdata['datestamp']=datestamp
dataFileName='/Users/nibl/Documents/Output/%s_%s_subdata.log'%(subdata['subcode'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
##############################################################################
try:
    print 'initializing serial device:'
    dev=syringe_pump.SyringePump('/dev/tty.KeySerial1', debug=True)
    print dev
    print 'using serial device: ', dev
    if not dev.isOpen():
        raise Exception('noPump')
    hasPump=True
except:
    hasPump=False


##############################################################################
if hasPump:
        #dev = SyringePump('/dev/tty.USA19H142P1.1')
        dev.debug = True 
        dev.setDiameter(1.0)#hanging here
        dev.setRate(5.0,'NS')
        dev.setAccumUnits('UL')
        dev.clearVolumeAccum()
        dev.setDirection('INF')
        infuse, withdraw = dev.getVolumeAccum()
        print('infuse: {0} (nl), withdraw: {1} (nl)'.format(infuse,withdraw))
        dev.run()
        time.sleep(3)
        dev.setDirection('WDR')
        time.sleep(3)
        infuse, withdraw = dev.getVolumeAccum()
        print('infuse: {0} (nl), withdraw: {1} (nl)'.format(infuse,withdraw))
        dev.stop()


##############################################################################
################parameters for how much liquid and how long###################
##############################################################################
#diameter=26.59
#mls_to_deliver=0.5
#delivery_time=2.0
#cue_time=2.0
#wait_time=2.0
#rinse_time=2.0
#swallow_time=2.0
#rate = mls_to_deliver*(3600.0/delivery_time)  # mls/hour
#
#trial_length=cue_time+delivery_time+wait_time+rinse_time+swallow_time
#
#
##############################################################################
############infusion measurements######################################
##############################################################################
#
#if hasPump:
#    
#    commands_to_send=['0PHN01','1PHN01','0CLDINF','1CLDINF','0DIRINF','1DIRINF','0RAT%0.1fMH'%rate,'1RAT%0.1fMH'%rate,'0VOL%0.1f'%mls_to_deliver,'1VOL%0.1f'%mls_to_deliver,'0DIA%0.1fMH'%diameter,'1DIA%0.1fMH'%diameter]
#    subdata['pumpver']=dev.sendCmd('VER')
#
#    dev.setBaudrate(9600)
#i think the issue is here
#should be sending commands to the pumps
#    for cmd in commands_to_send:
#        print 'sending: ',cmd
#        dev.sendCmd(cmd)
#        core.wait(0.1)
#
#    subdata['pumpdata']={}
#    for p in [0,1]:
#        for cmd in ['DIS','DIR','RAT','VOL','DIA']:
#            fullcmd='%d%s'%(p,cmd)
#            subdata['pumpdata'][fullcmd]=dev.sendCmd(fullcmd)
#            core.wait(0.1)
#
#    print subdata['pumpdata']
