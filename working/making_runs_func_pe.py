#making a function to make the onset files#
import numpy as N
import sys
from subprocess import check_output
import datetime

def make_onsets(run):
    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    print('check check')
    jitter=N.zeros(24).astype('float')
#trial conditions, need to change here for training or prediction error
    jitter[0:15]=4.0 #60% 
    jitter[15:22]=5.0 #30%
    jitter[22:24]=11.0 #10%

    N.random.shuffle(jitter)
    njitter=len(jitter)
    jitter2=jitter.tolist()
#this will make the random trial_lengths
    for x in N.nditer(jitter, op_flags=['readwrite']):
        x[...] = 11 + x

    tlength=jitter.tolist()

    trialcond=N.zeros(24).astype('int')
    trialcond[0:7]=0     # :) cue, :) delivery 30%
    trialcond[7:14]=1    # :( cue, :( delivery 30%
    trialcond[14:24]=2   # :) cue, :( delivery 40%

    N.random.shuffle(trialcond)
    conds=trialcond.tolist()
#    ntrials=len(trialcond)#set 24 trials
#    pump=N.zeros(ntrials)#0 array, length 24
#    pump zero is neutral, pump 1 is juice, pump 2 is milkshake
#    pump[trailcond==0]=1 #tampico pump
#    pump[trialcond==1]=2 #milkshake pump
#    pump[trialcond==2]=2 #milkshake pump
#    stim_images=['tampico.jpg', 'Milkshake.jpg', 'Milkshake.jpg']

    preonsets=[0]
    print(preonsets)
    for i, item in enumerate(tlength):
        x=preonsets[-1]+tlength[i]
        preonsets.append(x)
#write file with the onset
    f=open('/Users/nibl/Documents/taste_task/onset_files/onsets_'+run, 'w')
    print f
    for item in preonsets:
        print>>f, item
    f.close()
#write file with the jitter    
    g=open('/Users/nibl/Documents/taste_task/onset_files/jitter_'+run, 'w')
    print g
    for item in jitter2:
        print>>g, item
    g.close()
#write file with conditions
    h=open('/Users/nibl/Documents/taste_task/onset_files/conds_'+run, 'w')
    print h
    for item in conds:
        print>>h, item
    h.close()
    
def main ():
#input subject id to be run; this will generate an error message if no subject id is given
  check_args=1
  if len(sys.argv)<2:
    print('usage error: must specify a run number')
    sys.exit()
  elif check_args==1:
    run=sys.argv[1]

  
  make_onsets(run)
main()



