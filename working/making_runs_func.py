#making a function to make the onset files#
import numpy as N
import sys
from subprocess import check_output
import datetime

def make_onsets(run):
    datestamp=datetime.datetime.now().strftime("%Y-%m-%d-%H_%M_%S")
    print('check check')
    jitter=N.zeros(43).astype('float')
#trial conditions, need to change here for training or prediction error
    jitter[0:25]=4.0 #60% 
    jitter[25:38]=5.0 #30%
    jitter[38:43]=11.0 #10%

    N.random.shuffle(jitter)
    njitter=len(jitter)
    jitter2=jitter.tolist()
#this will make the random trial_lengths
    for x in N.nditer(jitter, op_flags=['readwrite']):
        x[...] = 11 + x

    tlength=jitter.tolist()

    trialcond=N.zeros(43).astype('int')
    trialcond[0:13]=0      # water cue, water delivery
    trialcond[13:28]=1    # :) cue, :) delivery
    trialcond[28:43]=2    # :( cue, :( delivery

    N.random.shuffle(trialcond)
    conds=trialcond.tolist()
#    ntrials=len(trialcond)#set 45 trials
#    pump=N.zeros(ntrials)#0 array, length 45

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


#not 100% sure i need this   
# pump zero is neutral, pump 1 is juice
#    pump[trialcond==1]=1
#    pump[trialcond==2]=2
    
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



