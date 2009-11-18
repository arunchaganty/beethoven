
from mingus.core import *
from mingus.containers import *
import random

def one_note_mutator(track):
	"""
	This function will pick up one random note
	from the track and replace it with a another note
	which is inturn created by transposing it, or
	similar
	"""
	if len(track.bars) ==0:
		return -1
	notes =[]
	while len(notes)==0:
		#Count the no of notes in the damn thing
#Pick up a random bar
		bar_no = random.randint(0,len(track.bars)-1)
		#Pick up a random note in that bar
		note_no = random.randint(0,len(track.bars[bar_no])-1)
#Select the note and mutate it
		beat, duration, notes = track.bars[bar_no][note_no]

	#print bar_no
	#print note_no
	#print notes[0].name
#mutate note
	if random.randint(0,1)%2==0:
		track.bars[bar_no][note_no][2][0].transpose("3") 
	else:
		track.bars[bar_no][note_no][2][0].transpose("-3") 

	#print track.bars[bar_no][note_no][2][0].name

	return track


def transpose_bar_mutator(track):
	"""
	Find a random bar, transpose it up by a 
	perfect fifth
	"""
	bar=[]
	while len(bar)==0:
		bar_no=random.randint(0,len(track.bars)-1)
		bar = track.bars[bar_no]
	#print bar_no
	#transpose the bar up by a perfect fifth
	if random.randint(0,1) %2==0:
		track.bars[bar_no].transpose("5")
	else:
		track.bars[bar_no].transpose("-5")
	return track

def permute_duration_mutator(track):
	"""
	Permute the durations in the melody.
	I will do this in a bar, so as to preserve the 
	sum of durations =1 property
	"""
	track2=Track()
	for bar in track.bars:
#randomly pick up a duration and 
		x1=[]
		i=0

		for beat,duration, notes in bar:
			x1.append(i)
			i+=1

		x2 = x1[:]
		random.shuffle(x2)
		i=0
		bar_ = Bar()

		for beat,duration, notes in bar:
			bar_.set_meter(bar.meter)
		#	print "---" + str(x2[i]) + "--" + str(bar[x2[i]][1])
			bar_.place_notes(notes, bar[x2[i]][1])
			i+=1

		track2.add_bar(bar_)
	return track2

