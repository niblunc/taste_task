import psychopy.app
from psychopy import visual, core, event, logging, data, misc, sound

import numpy as N
import sys,os,pickle
sys.path.insert(0, '/Users/nibl/Documents/pyserial-2.6')
sys.path.append('/Users/nibl/Documents/taste_task')
import cv2
import socket
from socket import gethostname
import inspect
sys.path.append('/Users/nibl/Documents/taste_task/psychtask')
import exptutils
from exptutils import *
import datetime
import serial
import time


######################################################################
#helper functions
def store_scriptfile():
    scriptfile= inspect.getfile(inspect.currentframe())# save a copy of the script in the data file
    f=open(scriptfile)
    script=f.readlines()
    f.close()
    return script

def check_for_quit(subdata,win):
    k=event.getKeys()
    print 'checking for quit key %s'%subdata['quit_key']
    print 'found:',k
    if k.count(subdata['quit_key']) >0:# if subdata['quit_key'] is pressed...
        print 'quit key pressed'
        return True
    else:
        return False

def wait_for_trigger():
    event.clearEvents()
    if subdata['simulated_response']:
        msg="SIMULATION MODE"
    else:
        msg=''
    message=visual.TextStim(win, text='%s Waiting for start key (or press %s)\nBe very still!'%(msg,subdata['start_key']),
    font='BiauKai', height=1,color=u'white', colorSpace=u'rgb', opacity=1,depth=0.0,
    alignHoriz='center',wrapWidth=50)
    message.setAutoDraw(True) #automatically draw every frame
    win.flip()
    start=False
    while start==False:
        k=event.waitKeys()
        if k.count(subdata['start_key'])>0:#as soon as subdata['start_key'] is pressed...
            start=True
            message.setText('')#this clears the screen
            win.flip()
        if k.count(subdata['quit_key']) >0:# if subdata['quit_key'] is pressed...
            exptutils.shut_down_cleanly(subdata,win)
            return False
    return True
######################################################################
######################################################################
subdata={}
subdata['subcode']='test'
datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
subdata['datestamp']=datestamp
subdata['expt_title']='tampico_probabilistic'
subdata['script']=store_scriptfile()
subdata['response']={}
subdata['score']={}
subdata['rt']={}
subdata['stim_onset_time']={}
subdata['stim_log']={}
subdata['is_this_SS_trial']={}
subdata['SS']={}
subdata['broke_on_trial']={}
subdata['start_key']='5'
subdata['quit_key']='q'
subdata['simulated_response']=False
datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
subdata['datestamp']=datestamp
clock=core.Clock()
dataFileName='/Users/nibl/Documents/Output/%s_%s_subdata.log'%(subdata['subcode'],subdata['datestamp'])
##############################################################################
###########test if pump exists################################################
##############################################################################
#try:
print 'initializing serial device:'
dev=serial.Serial(port='/dev/tty.USA19H142P1.1',baudrate=9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)
print dev
print 'using serial device: ', dev
if not dev.isOpen():
    dev.open()
##############################################################################
################juice water parameters and onset##############################
##############################################################################
trialcond=N.zeros(24).astype('int')
trialcond[0:12]=0     # water cue, water delivery
trialcond[12:24]=1    # juice cue, juice delivery
#made an array of 0s and 1s
stim_images=['bottled_water.jpg','tampico.jpg']
ntrials=len(trialcond)#set 24 trials
pump=N.zeros(ntrials)#0 array, length 24

N.random.shuffle(trialcond)#randomize conditions

# pump zero is neutral, pump 1 is juice
#this will need another pump built in
pump[trialcond==1]=1#set when which pump is supposed to pump
#pump[trialcond==2]=1

##############################################################################
################parameters for how much liquid and how long###################
##############################################################################
diameter=26.59
mls_to_deliver=0.5
delivery_time=2.0
cue_time=2.0
wait_time=2.0
rinse_time=2.0
swallow_time=2.0
rate = mls_to_deliver*(3600.0/delivery_time)  # mls/hour 900
trial_length=cue_time+delivery_time+wait_time+rinse_time+swallow_time

#pump_setup = ['VOL ML\r','TRGFT\r','PF 0\r']
pump_setup = ['0VOL ML\r', '1VOL ML\r']
pump_phases=['0PHN01\r','1PHN01\r','0CLDINF\r','1CLDINF\r','0DIRINF\r','1DIRINF\r','0RAT900MH\r','1RAT900MH\r','0VOL0.5\r','1VOL0.5\r','0DIA26.95MH\r','1DIA26.95MH\r']
#pump_phases = ['dia26.59\r', 'phn01\r', 'funrat\r', 'rat6.6mm\r', 'vol1\r', 'dirinf\r', 
#'phn02\r', 'funrat\r', 'rat15mm\r', 'vol0.1\r', 'dirwdr\r', \
#'phn03\r', 'funstp\r']

for c in pump_setup:
    dev.write(c)
    time.sleep(.25)

for c in pump_phases:
    dev.write(c)
    time.sleep(.25)



###########################################################################    
#######################setup screen########################################
###########################################################################
###########################################################################
fullscr=False

win = visual.Window([800,600],allowGUI=True, fullscr=fullscr, monitor='testMonitor', units='deg')
visual_stim=visual.ImageStim(win, image=N.zeros((300,300)), size=(0.75,0.75),units='height')

event.clearEvents()
wt=wait_for_trigger()
if not wt:
    print 'quit button pressed!'
    sys.exit()
else:
    print "quit status:",wt
    
message=visual.TextStim(win, text='')
############################################################################
subdata['trialdata']={}
clock.reset()
event.clearEvents()
onsets=N.arange(0,ntrials*trial_length,step=trial_length)
print(onsets)
for trial in range(ntrials):#for trial in 24 trials
    #print(trial)
    #if check_for_quit(subdata,win):
    #    exptutils.shut_down_cleanly(subdata,win)
    #    sys.exit()
    trialdata={}
    print 'trial %d'%trial
    trialdata['onset']=onsets[trial]
    print 'condition %d'%trialcond[trial]
    print 'showing image: %s'%stim_images[trialcond[trial]]
    visual_stim.setImage(stim_images[trialcond[trial]])
    visual_stim.draw()

    while clock.getTime()<trialdata['onset']:#wait until the specified onset time to display image_file
#        if check_for_quit(subdata,win):
#            exptutils.shut_down_cleanly(subdata,win)
#            sys.exit()
#    win.flip()

    while clock.getTime()<(trialdata['onset']+cue_time):#show the image
        pass
    
    if hasPump:
        print 'injecting via pump at address %d'%pump[trial]
        #print('%dRUN\r'%pump[trial])
        dev.write('%dRUN\r'%pump[trial])
        #dev.write('RUN\r')
    else:
        print 'no pump: should be injecting via pump at address %d'%pump[trial]
        
    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):#wait until liquid is delivered
        pass
#    message=visual.TextStim(win, text='')
#    message.draw()
#    win.flip()
    if hasPump:
        trialdata['dis']=[dev.write('0DIS\r'),dev.write('1DIS\r')]
        print(trialdata['dis'])

    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
        pass

    if hasPump:
        print 'injecting rinse via pump at address %d'%0
    #print('%dRUN\r'%0)
        dev.write('%dRUN\r'%0)
    #dev.write('RUN\r')
    else:
        print 'no pump: should be injecting rinse via pump at address %d'%pump[trial]
        
    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time):
        pass

#    message=visual.TextStim(win, text='swallow')
#    message.draw()
#    win.flip()

    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time+swallow_time):
        pass
#    message=visual.TextStim(win, text='')
#    message.draw()
#    win.flip()

    while clock.getTime()<(trialdata['onset']+trial_length):
        pass

    subdata['trialdata'][trial]=trialdata

win.close()

#print dev.sendCmd('VER')
f=open('Output/liquid_subdata_%s.pkl'%datestamp,'wb')
pickle.dump(subdata,f)
f.close()



