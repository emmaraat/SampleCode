"""
Programming in Neuroimaging course Assessment 2, Section B

This script takes all .csv files from a specified directory and analyses them.
The script provides a summary of the mean reaction time and percentage correct per subject, split up into 
congruent and incongruent trials. 
It also generates a graphical representation of the distribution of reaction times and correct responses in the two 
trial conditions.

It saves the table data as a .csv file and the figure as a .png file, as well as outputting them to the console.
"""

import glob
import numpy as np
import matplotlib.pyplot as plt
import datetime 
from math import floor, ceil

#### Plot Settings ####
xtickstep_rt = 0.1 #plot a tick every xtickstep_rt seconds for the reaction time plot: default 0.1, change this value for bigger/smaller steps
xtickstep_percent = 5 #plot a tick every xtickstep_percent % for the correct responses plot: default 5, change this value for bigger/smaller steps
colors = ['#377eb8', '#ff7f00'] #Colors for Congruent and Incongruent condition

#Extracting .csv files from specified directory
directory = 'C:\\Stroop\\data'
filename = '*.csv'
filepath = "{}\\{}".format(directory, filename)

subject_files = glob.glob(filepath)
n_subjects = len(subject_files)

#Preparing file to save reaction time data
analysis_date = datetime.datetime.now().strftime('%H%M_%d%m%Y')
table_filename = 'strooptask_summary_{}.csv'.format(analysis_date) 
table = open(table_filename, 'w')
table.write('ParticipantID,RTCongruent,STDCongruent,%Congruent,RTIncongruent,STDIncongruent,%Incongruent\n')

#Print table headers with specific spacing to match the printed outputs
print('{:^61s}'.format('### REACTION TIMES TABLE ###'))
print('{:<11s}{:^25s}\t{:^25s}'.format('Participant', 'Congruent', 'Incongruent'))
print('{:<11s}{:^16}{:>9}\t{:^16}{:>9}'.format('', 'Mean RT ± STD', '%correct', 'Mean RT ± STD', '%correct'))

#### ANALYSING SUBJECT DATA #####
#Loops through the data files per subject and extracts all reaction times, which are split up depending on whether
#the trial was congruent or incongruent
#It also calculates the percentages of correct responses for both trial types.
#Then, the mean and standard deviation of the subjects reaction time and % correct are printed and saved to the table summary file 
# Mean Reaction time and % correct are also saved in variables for plotting the figure below

meanrts_congruent = []
meanrts_incongruent = []
meanpercent_congruent = []
meanpercent_incongruent = []

for n, file in enumerate(subject_files):
    #Reset variables to collect all reaction times for this subject
    congruent_rts = []
    incongruent_rts = []
    con_correct = 0
    incon_correct = 0
    f = open(file, 'r') 
    
    header = f.readline()
    #Collect all reaction times & %correct for this subject, split up in congruent and incongruent trials
    for line in f.readlines():
        data = line.strip().split(',')
        
        if data[3] == 'congruent':
            congruent_rts.append(float(data[5]))
            if data[6] == 'True':
                con_correct += 1
        
        elif data[3] == 'incongruent':
            incongruent_rts.append(float(data[5]))
            if data[6] == 'True':
                incon_correct += 1
                
    f.close() #close data file
    
    #Calculate mean, std, % correct
    con_mean =np.nanmean(congruent_rts)
    con_std =np.nanstd(congruent_rts)
    con_percentage = 100*con_correct/len(congruent_rts)

    incon_mean = np.nanmean(incongruent_rts)
    incon_std = np.nanstd(incongruent_rts)
    incon_percentage = 100*incon_correct/len(incongruent_rts)
    
    #Save data for distribution plot
    meanrts_congruent.append(con_mean)
    meanrts_incongruent.append(incon_mean)
    meanpercent_congruent.append(con_percentage)
    meanpercent_incongruent.append(incon_percentage)
    
    #Print data for this subject
    print('{:<11}{:<6.3f} ±  {:<6.3f}, {:<6.2f}%\t{:<6.3f} ±  {:<6.3f}, {:<6.2f}%'.format(n+1, con_mean, con_std, con_percentage, incon_mean, incon_std, incon_percentage))
    
    #Save data for this subject to table file
    table.write('{},{:.3f},{:.3f},{:.2f},{:3f},{:.3f},{:.2f}\n'.format(n+1, con_mean, con_std, con_percentage, incon_mean, incon_std, incon_percentage))

#Print mean RT and percentage correct for the whole group and write it to the table
print('{:<11}{:<6.3f} ±  {:<6.3f}, {:<6.2f}%\t{:<6.3f} ±  {:<6.3f}, {:<6.2f}%'.format('Mean', np.nanmean(meanrts_congruent), np.nanstd(meanrts_congruent), np.nanmean(meanpercent_congruent),
                                                                                      np.nanmean(meanrts_incongruent), np.nanstd(meanrts_incongruent), np.nanmean(meanpercent_incongruent)))
table.write('{},{:.3f},{:.3f},{:.2f},{:3f},{:.3f},{:.2f}\n'.format('Mean', np.nanmean(meanrts_congruent), np.nanstd(meanrts_congruent), np.nanmean(meanpercent_congruent),
                                                                   np.nanmean(meanrts_incongruent), np.nanstd(meanrts_incongruent), np.nanmean(meanpercent_incongruent)))
table.close() #close table file 

### Formatting for plotting ###
# PREPARE BINWIDTH AND XTICKS FOR REACTION TIME PLOT
#Extract lowest and highest rt to control the width of the histogram bins and the x-ticks/range of the plot
#For bins: create a range of values from min to max with a specified binwidth of 0.02 seconds, to ensure the data has the same resolution in each condition
#For x-ticks: round down/up with floor/ceiling to the nearest 0.1 seconds respectively to get range of x-ticks needed
min_rt = min([min(meanrts_congruent), min(meanrts_incongruent)])
max_rt = max([max(meanrts_congruent), max(meanrts_incongruent)])
binwidth_rt = 0.02 #Bin resolution for reaction times
bins_rt = np.arange(min_rt, max_rt + binwidth_rt, binwidth_rt)

min_rtx = floor(min_rt*10)/10
max_rtx = ceil(max_rt*10)/10
xticks_rt = np.arange(min_rtx, max_rtx+xtickstep_rt, xtickstep_rt)

# PREPARE BINWIDTH AND XTICKS FOR CORRECT RESPONSES PLOT
#Same as for reaction times plot, but with %correct data
#Binwidth is 1%
#X-ticks are rounded down/up to the nearest 5%. If the plot has too many ticks, increase the step number
min_per = min([min(meanpercent_congruent), min(meanpercent_incongruent)])
max_per = max([max(meanpercent_congruent), max(meanpercent_incongruent)])
binwidth_percent = 1
bins_percent = np.arange(min_per, max_per+binwidth_percent, binwidth_percent)

min_perx = floor(min_per/5)*5
max_perx = ceil(max_per/5)*5
xticks_percent = np.arange(min_perx, max_perx+xtickstep_percent, xtickstep_percent)

### Plotting figure ###
fig, axs = plt.subplots(1, 2, constrained_layout=True)
fig.suptitle('Distribution of RT and % correct\n for congruent and incongruent trials (n={})'.format(n_subjects), fontweight='bold')

#Reaction times subplot
axs[0].hist(meanrts_incongruent, bins = bins_rt, color = colors[0], alpha = 0.5)
axs[0].hist(meanrts_congruent, bins = bins_rt, color = colors[1], alpha = 0.3)
#Replot the data to create the solid outlines
axs[0].hist(meanrts_incongruent, bins = bins_rt, facecolor="None", edgecolor=colors[0], lw=1.3)
axs[0].hist(meanrts_congruent, bins = bins_rt, facecolor="None", edgecolor=colors[1], lw=1.3)
#Set x ticks and labels
axs[0].xaxis.set_ticks(xticks_rt)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Count')
axs[0].set_title('Reaction time')

#Correct responses subplot
axs[1].hist(meanpercent_incongruent, bins = bins_percent, color = colors[0], alpha = 0.5)
axs[1].hist(meanpercent_congruent, bins = bins_percent, color = colors[1], alpha = 0.3)
#create legend on the right outside of subplot
axs[1].legend(['Incongruent', 'Congruent'], loc='upper left', bbox_to_anchor= (1.01, 1.01)) 

#Replot the data to create the solid outlines
axs[1].hist(meanpercent_incongruent, bins = bins_percent, facecolor="None", edgecolor=colors[0], lw=1.3)
axs[1].hist(meanpercent_congruent, bins = bins_percent,facecolor="None", edgecolor=colors[1], lw=1.3)

#Set x ticks and labels
axs[1].xaxis.set_ticks(xticks_percent)
axs[1].set_xlabel('Percentage (%)')
axs[1].set_title('Correct responses')

#Plot figure in console or separate window depending on internal settings of Spyder
fig.show() 

### Saving figure ###
fig.savefig('group.png', dpi=300)

