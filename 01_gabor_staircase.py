#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from psychopy import  gui, visual, core, data, event, logging
from time import strftime
from random import choice
from numpy.random import choice as choice2
from numpy.random import random
import random as rd
import numpy as np
import csv

##### SETUP #####

### Parameters ###

###### EDIT PARAMETERS BELOW #######

num_trials = 30  # number of trials in the experiment on target side
stim_dur = 1.     # time in seconds that the subliminal stim appears on the screen [strong,weak,catch]
stepsize = 0.005     # The stepsize for the staircase procedure
response_dur = 1.   # time the response period stays on the screen
iti_durs = [.5,1]  # time with no no image present between trials
stim_size = 512
initalOpacity = 0.07         #size of the stimulus on screen
response_keys = {'left':'b','right':'z'}     # keys to use for a left response and a right response
response_keys_inv = {v: k for k, v in response_keys.items()}
reskeys_list = ['b','z']
pix_size = .001

practice_iti_dur = 2
practice_stim_dur = .3
practice_blank_dur = .033
practice_mask_dur = .3


###### STOP EDITING BELOW THIS LINE #######


#Experimenter input
dlg = gui.Dlg(title = 'Experiment Parameters')
dlg.addField('Subject ID:')
dlg.addField('Session:')
dlg.addField('Scanner', choices = ['yes','no'])
dlg.addField('Practice', choices = ['yes','no'])
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
win = visual.Window(size=[800, 600],  screen = 0, fullscr = False, units = 'pix', blendMode = 'avg')
win.setMouseVisible(False)

#Gabor PARAMETERS

X = stim_size; # width of gabor patch in pixels

sf = 10 / X; # cycles per pixel
left = 357; #left angle in deg
right = 3; #right angle in deg
noiseTexture = random([X,X])*2.0-1. # a X-by-X array of random numbers in [-1,1]


# noise patch
n = visual.GratingStim(
    win = win, mask='gauss', tex = noiseTexture,
    size = X, contrast = 1.0, opacity = 1.0,
)

# Fixation Cross
fixation = visual.ShapeStim(
    win=win, name='polygon', vertices='cross',
    size=(20, 20),
    ori=0, pos=(0, 0),
    lineWidth=1, lineColor=[1,1,1], lineColorSpace='rgb',
    fillColor=[1,1,1], fillColorSpace='rgb',
    opacity=1, depth=0.0, interpolate=True)

###text
#headers
instructions_header = visual.TextStim(win, text='INSTRUCTIONS', color = 'black', alignHoriz = 'center', pos=(0.0,.8))
experiment_header = visual.TextStim(win, text='MAIN EXPERIMENT', color = 'black', alignHoriz = 'center', pos=(0.0,.8))

# #instructions
# instructions_text1 = visual.TextStim(win, text='In each trial of this experiment a diamond shape will appear in the middle of the screen', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.2))
# instructions_text2 = visual.TextStim(win, text='It will have a point missing from its left side or its right side.', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.2))
#
# instructions_text3 = visual.TextStim(win, text='left side missing                 right side missing', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-0.5))
# instructions_text4 = visual.TextStim(win, text='The diamond will be followed immediately by a frame shape.', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.2))
# frame_example = visual.ImageStim(
# 	win=win,
# 	image="pics/mask.png",
# 	units="pix",
# 	pos=[0,-50])
#
#
# instructions_text5 = visual.TextStim(win, text='Press the "%s" key if the frame is preceded by a diamond missing a point on its %s side.'%(response_keys['left'],'left'), height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
# instructions_text6 = visual.TextStim(win, text='Press the "%s" key if the frame is preceded by a diamond missing a point on its %s side.'%(response_keys['right'],'right'), height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-0.1))
#
#
# instructions_text1.wrapWidth = 4
# instructions_text2.wrapWidth = 4
# instructions_text3.wrapWidth = 4
# instructions_text4.wrapWidth = 4
# instructions_text5.wrapWidth = 4
# instructions_text6.wrapWidth = 4
#
# instructions2_text = [visual.TextStim(win, text='Geat job! Make sense?', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.1)),
# 			visual.TextStim(win, text='In the real experiment you will only have %s seconds to respond.'%response_dur, height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))]
#
# for instruction in instructions2_text:
# 	instruction.wrapWidth = 4
#
#
# #mis
# example_text = visual.TextStim(win, text='Here are some practice examples . . .', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0))
# get_ready_text = [visual.TextStim(win, text='Now let\'s move on the the real experiment.', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,0.0)),
# 				  visual.TextStim(win, text='Get ready . . .', height = .065, color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,-0.1))]
# press_left_text = visual.TextStim(win, text='Press the "%s" key'%response_keys['left'], color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,stim_size+.2))
# press_right_text = visual.TextStim(win, text='Press the "%s" key'%response_keys['right'], color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,stim_size+.2))
# press_nothing_text = visual.TextStim(win, text='Press nothing', color = 'black', alignHoriz = 'center', alignVert = 'center', pos=(0.0,stim_size+.2))

### Timing ###

practice_clock = core.Clock()
experiment_clock = core.Clock()

### Results Logging ###
time_stamp = strftime('%d-%m-%Y_%H:%M:%S').replace(':','_')
output_file_path = 'results/%s_%s_%s.csv'%(subid,session,time_stamp)
output_file = open(output_file_path,'w+')

###TO DO
output_file.write('trial,trial_type,response,correct,response_time,cumulative_response_time,iti_onset,iti_dur,stim_onset,stim_dur,opacity\n')
output_file.flush()


### Quitting ###
event.globalKeys.clear()
quit_key = 'q'
def quit_experiment():
	core.quit()
event.globalKeys.add(key=quit_key, func=quit_experiment)


##### RUN EXPERIMENT #####

# ###  instructions  ###
# #explain task
# if show_practice:
# 	#intro to experiment
# 	instructions_header.draw()
# 	instructions_text1.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
# #
# #	#show missing corner shapes
# 	instructions_header.draw()
# 	instructions_text2.draw()
# 	instructions_text3.draw()
# 	left_example.draw()
# 	right_example.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
# #
# #	#show frame shape
# 	instructions_header.draw()
# 	instructions_text4.draw()
# 	frame_example.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
# #
# #	#tell what buttons to press
# 	instructions_header.draw()
# 	instructions_text5.draw()
# 	instructions_text6.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
# #
# 	instructions_header.draw()
# 	example_text.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
# #
# 	for practice_side in ['left','right']:
# 		instructions_header.draw()
# 		win.flip()
# 		core.wait(practice_iti_dur)
# 		#press practice stim
# 		practice_clock.reset()
# 		while practice_clock.getTime() < practice_stim_dur:
# 			instructions_header.draw()
# 			white_diamond.draw()
# 			blockers[practice_side].draw()
# 			win.flip()
# 		#blank screen
# 		while practice_clock.getTime() < practice_stim_dur+practice_blank_dur:
# 			instructions_header.draw()
# 			win.flip()
# 		#press mask
# 		while practice_clock.getTime() < practice_stim_dur+practice_blank_dur+practice_mask_dur:
# 			instructions_header.draw()
# 			mask.draw()
# 			black_diamond.draw()
# 			if version == 'go-nogo' and target_side == practice_side:
# 				press_nothing_text.draw()
# 			else:
# 				if practice_side == 'left':
# 					press_left_text.draw()
# 				else:
# 					press_right_text.draw()
# 			win.flip()
# 		#response
# 		instructions_header.draw()
# 		if practice_side == 'left':
# 			press_left_text.draw()
# 		else:
# 			press_right_text.draw()
# 		win.flip()
# 		event.waitKeys(keyList=response_keys[practice_side])
#
#
# 	#Post practice text, get ready for experiment
# 	instructions_header.draw()
# 	for instruction in instructions2_text:
# 		instruction.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
# 	experiment_header.draw()
# 	for get_ready in get_ready_text:
# 		get_ready.draw()
# 	win.flip()
# 	event.waitKeys(keyList='space')
#

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
	gabor = visual.GratingStim(win = win, tex = gabor_tex, mask = None, units = 'pix',  size = X, contrast = 1.0, opacity = opacity)

	# iti presentation
	#Add the Parallelport stuff here -> see parallel_port.py
	while experiment_clock.getTime() < stim_onset:
		win.flip()
	#stim presentation
	responded = False
	response = []
	event.clearEvents(eventType=None)
	while experiment_clock.getTime() < response_end:
		n.draw()
		gabor.draw()
		fixation.draw()
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
				else:
					correct = 0
				output_file.write(','.join([str(trial),str(side),str(sub_response),str(correct),str(response_time),str(cumulative_response_time),str(iti_onset),str(iti_dur),str(stim_onset),str(stim_dur),str(opacity)+'\n']))
				output_file.flush()

	if not responded:
		correct = 0
		output_file.write(','.join([str(trial),str(side),'NA',str(correct),'NA','NA',str(iti_onset),str(iti_dur),str(stim_onset),str(stim_dur),str(opacity)+'\n']))
		output_file.flush()
	#timing update
	last_trial_dur = iti_dur + stim_dur + response_dur
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
