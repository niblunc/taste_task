import numpy as N

###############creating variable jitter#######################################
##############################################################################

jitter=N.zeros(45).astype('float')
#trial conditions, need to change here for training or prediction error
jitter[0:27]=2.0 #60% 
jitter[27:40]=3.0 #30%
jitter[40:45]=6.0 #10%

N.random.shuffle(jitter)
njitter=len(jitter)

#this will make the random trial_lengths
for x in N.nditer(jitter, op_flags=['readwrite']):
    x[...] = 8 + x


tlength=jitter.tolist()#same as jitter just a list

trialcond=N.zeros(45).astype('int')
trialcond[0:15]=0      # water cue, water delivery
trialcond[15:30]=1    # :) cue, :) delivery
trialcond[30:45]=2    # :( cue, :( delivery

N.random.shuffle(trialcond)

#made an array of 0s and 1s
stim_images=['bottled_water.jpg','tampico.jpg', 'third_image.jpg']
ntrials=len(trialcond)#set 45 trials
pump=N.zeros(ntrials)#0 array, length 45
#trial_length=10
#onsets=N.arange(0,ntrials*trial_length,step=trial_length)

#N.random.shuffle(trialcond)#randomize conditions
# pump zero is neutral, pump 1 is juice
#this will need another pump built in
pump[trialcond==1]=1
pump[trialcond==2]=2

preonsets=[0]
#setting the onsets
for i, item in enumerate(tlength):
    x=preonsets[-1]+tlength[i]
    preonsets.append(x)

#onsets2=N.array(preonsets)

#for item in thelist:
#  print>>thefile, item

