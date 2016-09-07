# Crave Crush Experiement. 11/20/2015
# Author: Nathan Nichols <nathann@ori.org>

from psychopy import visual, core, data, gui, event, data, logging
import csv
import time
import serial
import numpy as N
import sys,os,pickle
import datetime
# Lab tech setup

monSize = [800, 600]
info = {}
info['fullscr'] = False
info['port'] = '/dev/tty.USA19H142P1.1'
info['participant'] = 'test'
dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()
#######################################
subdata={}

subdata['subcode']='test'
subdata['completed']=0
subdata['cwd']=os.getcwd()

clock=core.Clock()
datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
subdata['datestamp']=datestamp
subdata['expt_title']='tampico_probabilistic'

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
##########################
dataFileName='/Users/nibl/Documents/Output/%s_%s_subdata.log'%(subdata['subcode'],subdata['datestamp'])
logging.console.setLevel(logging.INFO)
logfile=logging.LogFile(dataFileName,level=logging.DATA)
#######################################
# Serial connection and commands setup
ser = serial.Serial(
                    port=info['port'],
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS
                   )
if not ser.isOpen():
    ser.open()

time.sleep(1)

pump_setup = ['0VOL ML\r', '1VOL ML\r']
pump_phases=['0PHN01\r','1PHN01\r','0CLDINF\r','1CLDINF\r','0DIRINF\r','1DIRINF\r','0RAT900MH\r','1RAT900MH\r','0VOL0.5\r','1VOL0.5\r','0DIA26.95MH\r','1DIA26.95MH\r']

for c in pump_setup:
    ser.write(c)
    time.sleep(.25)

for c in pump_phases:
    ser.write(c)
    time.sleep(.25)

# HELPER FUNCTIONS
def show_instruction(instrStim):
    # shows an instruction until a key is hit.
    while True:
        instrStim.draw()
        win.flip()
        if len(event.getKeys()) > 0:
            break
        event.clearEvents()


def show_stim(stim, seconds):
    # shows a stim for a given number of seconds
    for frame in range(60 * seconds):
        stim.draw()
        win.flip()

# MONITOR
win = visual.Window(monSize, fullscr=info['fullscr'],
                    monitor='testMonitor', units='deg')
visual_stim=visual.ImageStim(win, image=N.zeros((300,300)), size=(0.75,0.75),units='height')
# STIMS
instruction1_text = visual.TextStim(win, pos=(0, 0), text="You will see pictures of a chocolate milkshake that will be followed by tastes of milkshake. At certain points, you will be asked for a rating from 0 to 4. \n\nUse the button box to rate your craving for chocolate milkshake after seeing the picture. \n\nPress a button to continue.")
instruction2_text = visual.TextStim(win, pos=(0, 0), text="When you are instructed to administer the dose of Crave Crush or placebo, move slowly and wait until the last five seconds to put it in your mouth. \n\nPress a button to continue.")
instruction3_text = visual.TextStim(win, pos=(0, 0), text="Remember to follow the instructions carefully. \n\nPress a button to continue.")
fixation_text = visual.TextStim(win, text='+', pos=(0, 0), height=2)

pumping_ready_text = visual.TextStim(win, text='Ready to pump. Press \'c\' to initiate.', pos=(0, 0))
scan_trigger_text = visual.TextStim(win, text='Waiting for scan trigger...', pos=(0, 0))
swallow_text = visual.TextStim(win, text='Swallow', pos=(0, 0))
tampico_image = visual.ImageStim(win, image='tampico.jpg')
water_image=visual.ImageStim(win, image='bottled_water.jpg')
ratings_and_onsets = []

#global settings
diameter=26.59
mls_to_deliver=0.5
delivery_time=2.0
cue_time=2.0
wait_time=2.0
rinse_time=2.0
swallow_time=2.0
rate = mls_to_deliver*(3600.0/delivery_time)  # mls/hour 900
###########Grace notes##################
#need to make 2 sets of runs with randomized onsets of 45 events each with random jitters
#15 tasty, 15 not tasty, 15 neutral
#need to make 2 sets of runs with 24 events per block of mismatched and matched, with 14 matched

#Trials
trialcond=N.zeros(6).astype('int')
trialcond[0:3]=0    # water cue, water delivery
trialcond[3:6]=1    # juice cue, juice delivery
#made an array of 0s and 1s
stim_images=['bottled_water.jpg','tampico.jpg']
ntrials=len(trialcond)#set 24 trials
pump=N.zeros(ntrials)#0 array, length 24
trial_length=10
onsets=N.arange(0,ntrials*trial_length,step=trial_length)

#N.random.shuffle(trialcond)#randomize conditions

# pump zero is neutral, pump 1 is juice
#this will need another pump built in
pump[trialcond==1]=1
stim_images=['bottled_water.jpg','tampico.jpg']
subdata['trialdata']={}

"""
    The main run block!
"""

def run_block():

    # Instructions (press any key to continue)
    show_instruction(instruction1_text)
    show_instruction(instruction2_text)
    show_instruction(instruction3_text)

    # Await scan trigger
    while True:
        scan_trigger_text.draw()
        win.flip()
        if 'c' in event.waitKeys():
            break
        event.clearEvents()

    clock=core.Clock()
    for cycle in [0,1]:
        t = clock.getTime()
        ratings_and_onsets.append(['fixation',t])
        show_stim(fixation_text, 7)  # 10 sec blank screen with fixation cross
        t = clock.getTime()
        for trial in range(ntrials):
                    
            trialdata={}#dictionary
            trialdata['onset']=onsets[trial]#onsets, trial is the number, the trialdata is getting the onset time and adding it to the trial data dictionary 
            visual_stim.setImage(stim_images[trialcond[trial]])#need to insert the stim_image array here
            print 'condition %d'%trialcond[trial]
            print 'showing image: %s'%stim_images[trialcond[trial]]
            visual_stim.draw()
            logging.log(logging.DATA, "image=%s"%stim_images[trialcond[trial]])
            
            while clock.getTime()<trialdata['onset']:
                pass
            win.flip()
            
            while clock.getTime()<(trialdata['onset']+cue_time):#show the image
                pass
            print 'injecting via pump at address %d'%pump[trial]
            logging.log(logging.DATA,"injecting via pump at address %d"%pump[trial])
            ser.write('%drun\r'%pump[trial])
            while clock.getTime()<(trialdata['onset']+cue_time+delivery_time):
                pass
            message=visual.TextStim(win, text='')
            message.draw()
            win.flip()
            
            trialdata['dis']=[ser.write('0DIS\r'),ser.write('1DIS\r')]
            print(trialdata['dis'])

            while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time):
                pass
            
            print 'injecting rinse via pump at address %d'%0
            ser.write('%dRUN\r'%0)
        
            while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time):
                pass

            message=visual.TextStim(win, text='swallow')
            message.draw()
            win.flip()

            while clock.getTime()<(trialdata['onset']+cue_time+delivery_time+wait_time+rinse_time+swallow_time):
                pass
            message=visual.TextStim(win, text='')
            message.draw()
            win.flip()

            while clock.getTime()<(trialdata['onset']+trial_length):
                pass
            
            subdata['trialdata'][trial]=trialdata
        win.close()

run_block()

f=open('/Users/nibl/Documents/Output/liquid_subdata_%s.pkl'%datestamp,'wb')
pickle.dump(subdata,f)
f.close()

core.quit()
