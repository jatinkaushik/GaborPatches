4    #!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging
from time import strftime
from random import choice
from numpy.random import choice as choice2
from numpy.random import random
import random as rd
import numpy as np
import csv
import os

##### SETUP #####

### Parameters ###

###### EDIT PARAMETERS BELOW #######

num_trials = 100  # number of trials in the experiment on target side
stim_dur = 2.     # time in seconds that the subliminal stim appears on the screen [strong,weak,catch]
stepsize = 0.05     # The stepsize for the staircase procedure
response_dur = 1.   # time the response period stays on the screen
iti_durs = [.5,1]  # time with no no image present between trials
stim_size = 256
initalOpacity = 0.10         #size of the stimulus on screen
response_keys = {'left':'b','right':'n'}     # keys to use for a left response and a right response
response_keys_inv = {v: k for k, v in response_keys.items()}
reskeys_list = ['b','n']
pix_size = .001

practice_iti_dur = 2
practice_stim_dur = 1.5



###### STOP EDITING BELOW THIS LINE #######


#Experimenter input
dlg = gui.Dlg(title = 'Experiment Parameters')
dlg.addField('Subject ID:')
dlg.addField('Session:')
dlg.addField('Scanner', choices = ['yes','no'])
dlg.addField('Practice', choices = ['yes','no'])
dlg.addField('Visual Field', choices = ['left', 'right'])
exp_input = dlg.show()

subid = exp_input[0]
session = exp_input[1]
if exp_input[2] == 'yes':
	scanner = True
else:
	scanner = False
if exp_input[3] == 'yes':
	show_practice = True
else:
	show_practice = False

vis_field = [0,0]
xpos = 400

hemifield = exp_input[4]

if exp_input[4] == 'left':
	vis_field = [-xpos,0]
elif exp_input[4] == 'right':
	vis_field = [xpos,0]

#get shuffled list of trials
trial_states = {}
n = 0
for i in range(int(num_trials)):
	n+=1
	trial_states[n] = {'target':'left'}
	n+=1
	trial_states[n] = {'target':'right'}

trial_order = list(range(1,(1+num_trials)))
rd.shuffle(trial_order)


### Visuals ###

#window
win = visual.Window(size=[1024, 768],  screen = 0, fullscr = False, units = 'pix')
win.setMouseVisible(False)

#Gabor PARAMETERS

X = stim_size; # width of gabor patch in pixels

sf = 10 / X; # cycles per pixel
left = 357; #left angle in deg
right = 3; #right angle in deg
noiseTexture = random([X,X])*2.0-1. # a X-by-X array of random numbers in [-1,1]

noiseTexture_example = random([256,256])*2.0-1. # a X-by-X array of random numbers in [-1,1]

n_example = visual.GratingStim(
    win = win, mask='gauss', tex = noiseTexture_example,
    size = 256, contrast = 1.0, opacity = 1.0,
)


# noise patch
n = visual.GratingStim(
    win = win, mask='gauss', tex = noiseTexture,
    size = X, contrast = 1.0, opacity = 1.0,
	pos = vis_field
)

# Fixation Cross
fixation = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(20, 20),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)

fixation_green = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(20, 20),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[0,1,0], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)


gabor_tex_example_left = (
		    visual.filters.makeGrating(res=256, cycles=256 * sf, ori = 357, gratType = "sin" ) *
		    visual.filters.makeMask(matrixSize=256, shape="gauss", range=[0, 1])
		)


gabor_tex_example_right = (
		    visual.filters.makeGrating(res=256, cycles=256 * sf, ori = 3, gratType = "sin" ) *
		    visual.filters.makeMask(matrixSize=256, shape="gauss", range=[0, 1])
		)


			# signal grating patch
gabor_left_example_vis = visual.GratingStim(win = win, tex = gabor_tex_example_left, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = 1, pos= (-200,-100.0))

gabor_right_example_vis = visual.GratingStim(win = win, tex = gabor_tex_example_right, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = 1, pos= (200,-100.0))

gabor_left_example = visual.GratingStim(win = win, tex = gabor_tex_example_left, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = .8)

gabor_right_example = visual.GratingStim(win = win, tex = gabor_tex_example_right, mask = None, units = 'pix',  size = 256, contrast = 1.0, opacity = .8)

###text
#headers
instructions_header = visual.TextStim(win, text='INSTRUCTIONS', color = 'black', alignHoriz = 'center', alignVert = 'top', pos = (0.0,250.))
experiment_header = visual.TextStim(win, text='MAIN EXPERIMENT', color = 'black', alignHoriz = 'center',  alignVert = 'top', pos = (0.0,0.0))

#Left
left_text = visual.TextStim(win, text='LEFT', color = 'black', alignHoriz = 'center', alignVert = 'top', pos = (-200.0,100))
right_text = visual.TextStim(win, text='RIGHT', color = 'black', alignHoriz = 'center', alignVert = 'top', pos = (200.0,100))

#instructions
instructions_text1 = visual.TextStim(win, text='In each trial of this experiment angled black and white stripes will appear in the middle of the screen', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
instructions_text2 = visual.TextStim(win, text='The stripes will be angled to the left or to the right', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,160.0))


instructions_text5 = visual.TextStim(win, text='Press the "%s" key if the stripes are angled to the %s side.'%(response_keys['left'],'left'), color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,50.0))
instructions_text6 = visual.TextStim(win, text='Press the "%s" key if if the stripes are angled to the %s side.'%(response_keys['right'],'right'),  color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-50))



instructions2_text = visual.TextStim(win, text='Geat job! Make sense?',  color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.1))



#mis
example_text = visual.TextStim(win, text='Here are some practice examples . . .',  color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
get_ready_text = visual.TextStim(win, text='Now let\'s move on the the real experiment.', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
press_left_text = visual.TextStim(win, text='Press the "%s" key'%response_keys['left'], color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-200.))
press_right_text = visual.TextStim(win, text='Press the "%s" key'%response_keys['right'], color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-200))

### Timing ###

practice_clock = core.Clock()
experiment_clock = core.Clock()

#Create results folder

if not os.path.exists('my_folder'):
    os.makedirs('my_folder')

### Results Logging ###
time_stamp = strftime('%d-%m-%Y_%H:%M:%S').replace(':','_')
output_file_path = 'results/%s_%s_%s_staircase.csv'%(subid,session,time_stamp)
output_file = open(output_file_path,'w+')

###TO DO
output_file.write('trial,trial_type,response,correct,response_time,cumulative_response_time,iti_onset,iti_dur,stim_onset,stim_dur,opacity,currentDirection,visfield\n')
output_file.flush()


### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)


##### RUN EXPERIMENT #####

###  instructions  ###
#explain task
if show_practice:
	#intro to experiment
	instructions_header.draw()
	instructions_text1.draw()
	win.flip()
	event.waitKeys(keyList='space')
	instructions_text2.draw()
	gabor_left_example_vis.draw()
	left_text.draw()
	right_text.draw()
	gabor_right_example_vis.draw()
	win.flip()
	event.waitKeys(keyList='space')
	instructions_text5.draw()
	instructions_text6.draw()
	win.flip()
	event.waitKeys(keyList='space')
	example_text.draw()
	win.flip()
	event.waitKeys(keyList='space')
	n_example.draw()
	gabor_left_example.draw()
	press_left_text.draw()
	win.flip()
	event.waitKeys(keyList=response_keys['left'])

	for i in range(80):
		fixation.draw()
		win.flip()


	#right


	n_example.draw()
	gabor_right_example.draw()
	press_right_text.draw()
	win.flip()
	event.waitKeys(keyList=response_keys['right'])
	instructions2_text.draw()
	win.flip()
	event.waitKeys(keyList='space')
	get_ready_text.draw()


### Main Experiment ###servicde
#clock reset
win.flip()
elapse_time = 0
last_trial_dur = 0

#trigger scanner
if scanner:
	#port.write(chr(np.uint8(128+32+64+1)))
    event.waitKeys(keyList=['t'])

experiment_clock.reset()

correctInARow = 0
opacity = initalOpacity
trial = 0
reversal_counter = 0
currentDirection = ''
directions = ['a'] * (len(trial_order) + 1)
#save opacities

opacities = [0] * (len(trial_order)+1)
for shuffled_trial in trial_order:
	trial += 1
	iti_dur = choice(iti_durs)
	target_side = trial_states[shuffled_trial]['target']
	if (target_side == 'left'):
		side = 'left'
		gabor_tex = (
		    visual.filters.makeGrating(res=X, cycles=X * sf, ori = left, gratType = "sin" ) *
		    visual.filters.makeMask(matrixSize=X, shape="gauss", range=[0, 1])
		)


	else:
		side = 'right'
		gabor_tex = (
			visual.filters.makeGrating(res=X, cycles=X * sf, ori = right, gratType = "sin" ) *
			visual.filters.makeMask(matrixSize=X, shape="gauss", range=[0, 1])
			)


	elapse_time += last_trial_dur
	iti_onset = elapse_time
	stim_onset = elapse_time + iti_dur
	response_end = elapse_time + iti_dur + stim_dur

			# signal grating patch
	gabor = visual.GratingStim(win = win, tex = gabor_tex, mask = None, units = 'pix',  size = X, contrast = 1.0, opacity = opacity, pos = vis_field)

	# iti presentation
	#Add the Parallelport stuff here -> see parallel_port.py
	while experiment_clock.getTime() < stim_onset:
		fixation.draw()
		win.flip()
	#stim presentation
	responded = False
	response = []
	event.clearEvents(eventType=None)
	while experiment_clock.getTime() < response_end:
		n.draw()
		gabor.draw()
		fixation.draw()
		if responded:
			fixation_green.draw()
		win.flip()
		#event.waitKeys(keyList=reskeys_list)
		#response collection
		if not responded:
			response = event.getKeys(keyList=reskeys_list, timeStamped=True)
			if len(response) > 0:
				responded = True
				cumulative_response_time = round(experiment_clock.getTime(),3)
				response_time = round(experiment_clock.getTime() - elapse_time - iti_dur,3)
				sub_response = response_keys_inv[response[0][0]]
				if sub_response == side:
					correct = 1
					currentDirection = 'down'
				else:
					correct = 0
					currentDirection = 'up'
				output_file.write(','.join([str(trial),str(side),str(sub_response),str(correct),str(response_time),str(cumulative_response_time),str(iti_onset),str(iti_dur),str(stim_onset),str(stim_dur),str(opacity),str(currentDirection),str(hemifield)+'\n']))
				output_file.flush()
	if not responded:
		correct = 0
		fixation.draw()
		output_file.write(','.join([str(trial),str(side),'NA',str(correct),'NA','NA',str(iti_onset),str(iti_dur),str(stim_onset),str(stim_dur),str(opacity),str(currentDirection),str(hemifield)+'\n']))
		output_file.flush()
		win.flip()

	#timing update
	last_trial_dur = iti_dur + stim_dur + response_dur
	#change stimulus
	directions[trial] = currentDirection
		#reduce stepsize


	if trial > 1:
		if not directions[trial] == directions[trial-1]:
			stepsize = stepsize / 1.1


	if correct == 1:
		correctInARow += 1
		if correctInARow == 2:
			opacity -= stepsize
			correctInARow = 0
	else:
		correctInARow = 0
		opacity += stepsize
	if opacity < 0:
		opacity = 0








output_file.close()
win.close()
