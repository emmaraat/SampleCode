# -*- coding: utf-8 -*-
"""
Programming in Neuroimaging course Assessment 2, Section A
Stroop task Experiment code
This script runs a Stroop task experiment, which presents the names of colours (colourtext) with either 
a matching ink colour (congruent colourname) or a mismatch (incongruent colourname)
Participants need to respond to the ink colour by pressing the corresponding key as specified, as fast and accurate as possible.

Before the main experiment, the participant does some practice trials to familiarize them with the keys. These practice trials 
are each repeated until the participant presses the correct key.
The main experiment has trials equal to n_congruent*number of colours + n_incongruent*number of colours*(number of colours-1).
A short break is given each n_breaks trials.
In this case, there are 120 trials, with a break after each 40 trials.

For each experimental trial, trial number, colourtext, colourname, condition, colour response, reaction time, 
and correctness of response are recorded.

The data is saved in a file called Stroop_P{participantid}_{expdate}.csv to ensure no files 
are overwritten when a participant id is accidentally reused.
"""
from math import ceil
from psychopy import visual, core, gui, event
import random
import datetime

#### GENERAL SETTINGS #####
n_breaks = 40  # Frequency of breaks (every n trials)
n_congruent = 15  # Number of trials matching text and colour
n_incongruent = 5  # Number of trials mismatching text and colour for each colour per alternative colour
fixationduration = 0.35  # Fixation cross display duration: 350 ms
screenresolution = [6000, 6000]  # Max pixel size of the full screen window
# This must be at least equal to the display window resolution, which can be checked under Settings --> Display
# It is set to very large values so the window will always fill the whole display

# These set the height (and thus size) of the words in instructions, fixation cross, and stimuli.
# If the text is too big/small you can decrease/increase them to until you reach a satisfactory size
instructionheight = 20 #size of all instruction text
fixationheight = 25 #size of fixation cross
stimheight = 35 #size of stroop stimuli

#### SETTING UP COLOURS #####
# For each colour, specify the colour name, colour values from (-1, -1, -1) to (1, 1, 1) matching that colour,
# and the corresponding key response
colours = ['red', 'blue', 'green', 'yellow']
colourvalues = {'red': [1, -1, -1], 'blue': [-1, -1, 1], 'green': [-1, 1, -1], 'yellow': [1, 1, -1]}
colourkeys = {'f': 'red', 'g': 'blue', 'h': 'green', 'j': 'yellow'}

#### GENERATING STIMULUS LIST #####
# For each trial this list specifies the word to be written, the colour of the word,
# whether these match (congruent/incongruent), and the colour code to draw
# When the word and colour match, this is congruent, so we create trials equal to n_congruent (as set in General settings above)
# When the word and colour do not match, this is incongruent, so we create trials equal to n_incongruent
stimuli = []
for drawn in colours:
    for word in colours:
        if drawn == word:
            for ii in range(n_congruent):
                stimuli.append({'colourtext': word, 'colourname': drawn, 'condition': 'congruent',
                                'colourvalue': colourvalues[drawn]})
        else:
            for ii in range(n_incongruent):
                stimuli.append({'colourtext': word, 'colourname': drawn, 'condition': 'incongruent',
                                'colourvalue': colourvalues[drawn]})
random.shuffle(stimuli)  # randomize order of list of stimuli

# Calculate total trials and number of blocks
ntrials_total = len(stimuli)
nblocks = ceil(ntrials_total / n_breaks)

#### GENERATING PRACTICE LIST #####
# Practice trials take the first word of the colours list, and generates trials with all different colour values
# This way, the participant practices all different colour response keys.
practice = []
word = colours[0]
for drawn in colours:
    if drawn == word:
        practice.append(
            {'colourtext': word, 'colourname': drawn, 'condition': 'congruent', 'colourvalue': colourvalues[drawn]})
    else:
        practice.append(
            {'colourtext': word, 'colourname': drawn, 'condition': 'incongruent', 'colourvalue': colourvalues[drawn]})
random.shuffle(practice)  # randomize order of practice stimuli

#### PREPARING INSTRUCTIONS AND FEEDBACK TEXT #####
# These specify the instructions given at the start of the experiment (instructiontxt), for the practice trials,
# the feedback during practice, and the text displayed at the end of the experiment
key_instructions = "\n".join("{:>15s}\t\t{}".format(thiscolour, thiskey) for thiskey, thiscolour in colourkeys.items())
instructiontxt = """Welcome to the experiment.
In each trial, a colour name will appear on the screen.
Respond by pressing the key corresponding to the ink colour of the word, ignoring the word itself.
These are the keys you should use:
{}

Please try to respond as fast and accurately as possible!
The main experiment consists of {} blocks of {} trials, so a total of {} trials.

First, you will do some practice trials where you get feedback until you choose the correct key.
Press the space bar to continue to the practice trials.""".format(key_instructions, nblocks, n_breaks, ntrials_total)
practicetxt = 'First, you will do some practice trials for the {} colors, press the space bar to begin'.format(
    len(practice))
feedback_correct_txt = 'Correct, well done.\n Press the space bar to continue.'
feedback_incorrect_txt = 'Incorrect.\n Remember to press the key corresponding to the ink colour of the word.\n Press the space bar to try again.'
endtxt = 'The end.\n\nThank you for your time!\nPress any key to exit the experiment'

#### OUTPUT FILE PREPARATION #####
# Preparing dictionary to get input from experimenter to create filename for output file
# Expdate: Create a string version of the current year/month/day hour/minute
# to ensure each file name will be unique and data will not be overwritten
data = {}
data['expname'] = 'Stroop'
data['expdate'] = datetime.datetime.now().strftime('%H%M_%d%m%Y')
data['participantid'] = ''

# Creating Graphical User Interface to input Participant ID
# Use the 'fixed' argument to stop the user changing the 'expname' and 'expdate' parameters, since these should not be changed
dlg = gui.DlgFromDict(data, title='Input data', fixed=['expname', 'expdate'],
                      order=['expname', 'expdate', 'participantid'])
if not dlg.OK:
    print("User cancelled the experiment")
    core.quit()
filename = '{expname}_P{participantid}_{expdate}.csv'.format(**data)
f = open(filename, 'w')
f.write('trialnum,colourtext,colourname,condition,response,rt,correct\n')

#### DISPLAY WINDOW PREPARATION #####
# Open a full screen window with black background and prepare a text stimulus for later use
win = visual.Window(size=screenresolution, units="pix", color=(-1, -1, -1), fullScr=True, allowGUI=False)
stim = visual.TextStim(win, "", color=(1.0, 1.0, 1.0), height=instructionheight)

# Display Instructions on Screen
stim.setText(instructiontxt)
stim.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Display Practice block start text on Screen
stim.setText(practicetxt)
stim.draw()
win.flip()
event.waitKeys(keyList=['space'])

# Run practice trials
for pracnum, practicetrial in enumerate(practice):
    correct = False
    while correct == False:
        # Display fixation cross for fixationduration
        stim.setText('+')
        stim.setColor((1, 1, 1))
        stim.setHeight(fixationheight)
        stim.draw()
        win.flip()
        core.wait(fixationduration)

        # Display stimulus
        stim.setText(practicetrial['colourtext'])
        stim.setColor(practicetrial['colourvalue'])
        stim.setHeight(stimheight)
        stim.draw()
        starttime = win.flip()

        # Wait until a valid key press is made
        # This is either one of the keys in the colourkeys list, or the escape key to terminate the experiment
        # Other keys are ignored
        waiting = True
        response = ''
        while waiting:
            keyandtime = event.waitKeys(timeStamped=True)
            try:
                # Check if key is one of the response keys, if so, set response to the name of the corresponding colour
                response = colourkeys[keyandtime[0][0]]
                waiting = False
            except:
                if keyandtime[0][0] == 'escape':
                    # Check if key is escape, if so, terminate program
                    print('Experiment was terminated at practice trial {}'.format(pracnum))
                    win.close()  # close data file
                    f.close()
                    waiting = False
                else:
                    # Else return to begin of while loop and keep waiting for a valid key press
                    pass
        # For the practice trials, feedback is given
        # If they respond correctly, they continue to the next trial, otherwise the trial is repeated
        if response == practicetrial['colourname']:
            # Correct response
            stim.setText(feedback_correct_txt)
            stim.setColor((1, 1, 1))
            stim.setHeight(instructionheight)
            stim.draw()
            win.flip()
            event.waitKeys(keyList=['space'])
            correct = True  # This ends the current trial and continues to the next trial
        else:
            # Incorrect response key, give feedback, then repeat trial
            stim.setText(feedback_incorrect_txt)
            stim.setColor((1, 1, 1))
            stim.setHeight(instructionheight)
            stim.draw()
            win.flip()
            event.waitKeys(keyList=['space'])

        # Run experiment
rts = []
blocknum = 1
for trialnum, stimulus in enumerate(stimuli):
    # Display break screen at the start of main experiment and then after each n_breaks trials
    if trialnum % n_breaks == 0:
        # If there are less trials remaining than n_breaks, set nextblocktrials to the amount of trials left
        if len(stimuli) - trialnum < n_breaks:
            nextblocktrials = len(stimuli) - trialnum
        else:
            nextblocktrials = n_breaks
        # Update breaktxt with the information for the next block
        breaktxt = "Block {} out of {}.\nYou're about to start a  block of {}  trials.\nHave a short break, then press the space bar when you are ready to continue the experiment".format(
            blocknum, nblocks, nextblocktrials)
        blocknum += 1
        stim.setText(breaktxt)
        stim.setColor((1, 1, 1))  # white
        stim.setHeight(instructionheight)
        stim.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

    # Display fixation cross for fixationduration
    stim.setText('+')
    stim.setColor((1, 1, 1))
    stim.setHeight(fixationheight)
    stim.draw()
    win.flip()
    core.wait(fixationduration)

    # Display stimulus
    stim.setText(stimulus['colourtext'])
    stim.setColor(stimulus['colourvalue'])
    stim.setHeight(stimheight)
    stim.draw()
    starttime = win.flip()

    # Wait until a valid key press is made
    # This is either one of the keys in the colourkeys list, or the escape key to terminate the experiment
    # Other keys are ignored
    waiting = True
    response = ''
    while waiting:
        keyandtime = event.waitKeys(timeStamped=True)
        try:
            # Check if key is one of the response keys, if so, set response to the corresponding colour and continue to calculate rt
            response = colourkeys[keyandtime[0][0]]
            waiting = False
        except:
            if keyandtime[0][0] == 'escape':
                # Check if key is escape, if so, terminate program
                print('Experiment was terminated at trial {}'.format(trialnum))
                win.close()
                f.close()  # close data file
                waiting = False
            else:
                # Else return to begin of while loop and keep waiting for a valid key press
                pass
    rt = keyandtime[0][1] - starttime
    if response == stimulus['colourname']:
        correct = True
    else:
        correct = False
    # Write results of this trial to data file
    f.write('{:d},{},{},{},{},{:.6f},{}\n'.format(trialnum + 1, stimulus['colourtext'], stimulus['colourname'],
                                                  stimulus['condition'], response, rt, correct))

f.close()  # close data file

# End screen
stim.setText(endtxt)
stim.setColor((1.0, 1.0, 1.0))
stim.setHeight(instructionheight)
stim.draw()
win.flip()
event.waitKeys()

# close window
win.close()
