# taste_task
This task is a frankenstein of previous experiments in large part based on the work of Burger and Stice.
The original iteration was written by Poldrack for pyschopy and can be found here: https://github.com/poldrack/liquid
Further iterations, edited by Shearrer, for use in the Sugar Brain experiment can be found here: https://github.com/grace-shearrer/taste_task
This current version has further been altered with help of the CRAVECRUSH script from Nathan Nichols, 
which can be found at https://github.com/natsn/sweetcrave, and has partially been included here

The meaty code part is:
taste_task.py

Onsets can be randomly generated using the helper scripts:
making_runs_func.py
making_runs_func_pe.py (for prediction error onsets)
--or-- you can use your own onset scripts as long as you change the naming utility in the taste_task.py script

Make sure exputils.py and stim jpegs are all in the same
folder.

There are drivers that need to be installed and unfortunately you just
have to google them depending on the pump system you have set up.

The python code requires PsychoPy2. The best way to get this is downloading
the gui from here:

http://www.psychopy.org/

Photos of all the pump stuff is in the folder named pumpstuff.

The sugar brain lab notebook powerpoint details how I set up the gustometer to
prevent bubbles.

Questions:
email grace.shearrer@gmail.com


