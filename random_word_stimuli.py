"""
Written for Programming in Neuroimaging course of the University of York, 2019-2020
Assessment 1
This script takes a text file with words on separate lines, and selects all words of a specified length (4).
These words are grouped by same word ending (last two letters), and word-endings with enough words are selected (30) 
Then a random word from each word-ending group is selected to create a list of stimuli.
This list of stimuli is then printed to the console.

Created on Nov 14, 2019 ; Last modified on Nov 26, 2019
Written by Emma Raat
"""
import random

### Settings ###
filename = 'words.txt'
word_length = 4 #Length of words selected (integer)
wordending_length = 2 #Note: This value cannot be bigger than  word_length 
word_minimum = 30 #Minimum amount of words for a word_ending to be selected as stimulus
excluded_characters = ["'"] #Note: Only strings can be added in this list!
# Any words containing one or more of the strings in this list will be excluded, eg adding 'od' will exclude odor, odds etcera.

#Opening the file and extracting all the lines to a list of words
f = open(filename, 'r') 
words = f.readlines()

#Creating a list of all four letter words converted to lowercase, excluding all words containing apostrophes
word_list = []
for word in words:
    word = word.strip().lower() 
    if not any(exclude in word for exclude in excluded_characters):
        if len(word) == word_length:
            word_list.append(word)

#Removing duplicate words
word_list_unique = list(set(word_list)) 
print('The file contains {} unique {}-letter words \n'.format(len(word_list_unique), word_length))

#Creating a dictionary of unique word-endings with all words with that ending
wordending_dict = {}
for word in word_list_unique:
    ending = word[-wordending_length:]
    if ending in wordending_dict.keys():
        wordending_dict[ending].append(word)
    else:
        wordending_dict[ending] = [word]

#Selecting only the word-endings with equal or more than the minimum amount of words set, in this case 30.
#For each word ending with enough words, the word ending and the amount of words will be printed
wordending_dict_stimuli = {}
print('The following unique word-endings with at least {} words are present in the file'.format(word_minimum))
print('Word ending: Amount')
for ending in wordending_dict.keys():
    if len(wordending_dict[ending]) >= word_minimum:
        print('{}: {:3d}'.format(ending, len(wordending_dict[ending])))
        wordending_dict_stimuli[ending] = wordending_dict[ending]

#Selecting and printing a random word for each word ending
stimuli= []
print('\n{} random words selected\nStimuli:'.format(len(wordending_dict_stimuli.keys())))
for ending in wordending_dict_stimuli.keys():
    randomword = random.choice(wordending_dict_stimuli[ending])
    print(randomword)
    stimuli.append(randomword)