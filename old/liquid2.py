"""
deliver juice
"""
#####to run, in shell window <execfile("liquid2.py"), it initially doesn't work run via gui, then close and run cmdline##################################################
import psychopy.app
import numpy as N
import sys,os,pickle
sys.path.insert(0, '/Users/nibl/Documents/pyserial-2.6')
#####THIS IS IMPORTANT DON'T MESS WITH IT#######
sys.path.append('/Users/nibl/Documents/taste_task')
import cv2
import syringe_pump_original as syringe_pump
from psychopy import visual, core, event, logging, data, misc, sound
import socket
from socket import gethostname
import inspect
sys.path.append('/Users/nibl/Documents/taste_task/psychtask')
import exptutils
from exptutils import *
import datetime
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
# initialize subdata dictionary to store info about the study
subdata={}
#subdata['subcode']=raw_input('subject id: ')
subdata['subcode']='test'
subdata['completed']=0
subdata['cwd']=os.getcwd()
subdata['hostname']=socket.gethostname()
clock=core.Clock()
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
#where to save the data 
dataFileName='/Users/nibl/Documents/Output/%s_%s_subdata.log'%(subdata['subcode'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
##########################
dataFileName='/Users/nibl/Documents/Output/%s_%s_subdata.log'%(subdata['subcode'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
##############################################################################
###########test if pump exists################################################
##############################################################################
try:
    print 'initializing serial device:'
<<<<<<< HEAD
<<<<<<< HEAD
    #dev=syringe_pump.SyringePump('/dev/tty.usbserial')
    dev=syringe_pump.SyringePump('/dev/tty.USA19H142P1.1')
=======
    dev=syringe_pump.SyringePump('/dev/tty.KeySerial1', debug=True)
>>>>>>> working
=======
    dev=syringe_pump.SyringePump('/dev/tty.USA19H142P1.1', debug=True)
>>>>>>> working
    print dev
    print 'using serial device: ', dev
    if not dev.isOpen():
        raise Exception('noPump')
    hasPump=True
except:
    hasPump=False
##############################################################################
##############################################################################
###############creating variable jitter#######################################
##############################################################################

jitter=N.zeros(23).astype('float')
#trial conditions, need to change here for training or prediction error
jitter[0:7]=2.0 
jitter[7:21]=3.0
jitter[21:23]=6.0

N.random.shuffle(jitter)
njitter=len(jitter)

#this will make the random trial_lengths
for x in N.nditer(jitter, op_flags=['readwrite']):
    x[...] = 8 + x


tlength=jitter.tolist()

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
rate = mls_to_deliver*(3600.0/delivery_time)  # mls/hour

trial_length=cue_time+delivery_time+wait_time+rinse_time+swallow_time


trialcond=N.zeros(24).astype('int')

#trial conditions, need to change here for training or prediction error
trialcond[0:8]=0     # water cue, water delivery
trialcond[8:12]=1    # water cue, juice delivery
trialcond[12:20]=2   # juice cue, juice delivery
trialcond[20:24]=3   # juice cue, water delivery

#will need to change these images
stim_images=['bottled_water.jpg','bottled_water.jpg','tampico.jpg','tampico.jpg']
ntrials=len(trialcond)
pump=N.zeros(ntrials)

N.random.shuffle(trialcond)

# pump zero is neutral, pump 1 is juice
#this will need another pump built in
pump[trialcond==1]=1
pump[trialcond==2]=1

preonsets=[0]
#setting the onsets
for i, item in enumerate(tlength):
    x=preonsets[-1]+tlength[i]
    preonsets.append(x)

onsets=N.array(preonsets)

##############################################################################
############infusion measurements######################################
#dev.write('0PHN01\r')
#dev.write('1PHN01\r')
#dev.write('0CLDINF\r')
#dev.write('1CLDINF\r')
#dev.write('0DIRINF\r')
#dev.write('1DIRINF\r')
#dev.write('0RAT900.0MH\r')
#dev.write('1RAT900.0MH\r')
#dev.write('0VOL0.5\r')
#dev.write('1VOL0.5\r')
#dev.write('0DIA26.6MH\r')
#dev.write('1DIA26.6MH\r')
##############################################################################
if hasPump:
    
    commands_to_send=['0PHN01','1PHN01','0CLDINF','1CLDINF','0DIRINF','1DIRINF','0RAT%0.1fMH'%rate,'1RAT%0.1fMH'%rate,'0VOL%0.1f'%mls_to_deliver,'1VOL%0.1f'%mls_to_deliver,'0DIA%0.1fMH'%diameter,'1DIA%0.1fMH'%diameter]
    subdata['pumpver']=dev.sendCmd('VER')

    dev.setBaudrate(9600)
#i think the issue is here
#should be sending commands to the pumps
    for cmd in commands_to_send:
        print 'sending: ',cmd
        dev.sendCmd(cmd)
        core.wait(0.1)

    subdata['pumpdata']={}
    for p in [0,1]:
        for cmd in ['DIS','DIR','RAT','VOL','DIA']:
            fullcmd='%d%s'%(p,cmd)
            subdata['pumpdata'][fullcmd]=dev.sendCmd(fullcmd)
            core.wait(0.1)

    print subdata['pumpdata']
###########################################################################
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
##################set up trials#############################################
############################################################################

subdata['trialdata']={}
clock.reset()
event.clearEvents()

for trial in range(ntrials):
    if check_for_quit(subdata,win):
        exptutils.shut_down_cleanly(subdata,win)
        sys.exit()

    trialdata={}
    print 'trial %d'%trial
    trialdata['onset']=onsets[trial]
    print 'condition %d'%trialcond[trial]
    logging.log(logging.DATA,"Condition: %d"%trialcond[trial])
    print 'showing image: %s'%stim_images[trialcond[trial]]
    visual_stim.setImage(stim_images[trialcond[trial]])
    visual_stim.draw()
    logging.log(logging.DATA, "image=%s"%stim_images[trialcond[trial]])
    while clock.getTime()<trialdata['onset']:#wait until the specified onset time to display image_file
        if check_for_quit(subdata,win):
            exptutils.shut_down_cleanly(subdata,win)
            sys.exit()
    win.flip()

    while clock.getTime()<(trialdata['onset']+cue_time):#show the image
        pass

    if hasPump:
        print 'injecting via pump at address %d'%pump[trial]
        logging.log(logging.DATA,"injecting via pump at address %d"%pump[trial])

        dev.write('%dRUN\r'%pump[trial])
    else:
        print 'no pump: should be injecting via pump at address %d'%pump[trial]

    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):#wait until liquid is delivered
        pass
    message=visual.TextStim(win, text='')
    message.draw()
    win.flip()
    if hasPump:
        trialdata['dis']=[dev.write('0DIS'),dev.write('1DIS')]


    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
        pass

    if hasPump:
        print 'injecting rinse via pump at address %d'%0
        dev.write('%dRUN\r'%0)
    else:
        print 'no pump: should be injecting rinse via pump at address %d'%pump[trial]

    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time):
        pass

    #message=visual.TextStim(win, text='swallow')
    message=visual.TextStim(win, text='jitter')
    message.draw()
    win.flip()
#need to change the swallow time here
    while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time+swallow_time):
        pass
    message=visual.TextStim(win, text='')
    message.draw()
    win.flip()
#doesn't like the trial_length is variable
    while clock.getTime()<(trialdata['onset']+trial_length):
        pass

    subdata['trialdata'][trial]=trialdata           

win.close()

#print dev.sendCmd('VER')

f=open('/Users/nibl/Documents/Output/liquid_subdata_%s.pkl'%datestamp,'wb')
pickle.dump(subdata,f)
f.close()
