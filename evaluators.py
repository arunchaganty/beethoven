#
# A library of various track evalutors
#

from mingus.containers import *
from mingus.core import *
from mingus.midi import fluidsynth
import MusicGene

import math

def rangeCompare(value, range):
    if (value < range[0]):
        return 10*(value/range[0] - 1)
    elif (value > range[2]):
        return 10*(1 - value/range[2])
    else:
        # Weighted by how much variation there actually is
        return -abs(range[0] - value)/(range[2] - range[0])

def numericEvaluation(track):
    """ Evaluates the track based on numeric functions """

    pitchVariety_ = [0.15, 0.25, 0.45]

    keyCentric_ = [0.0, 0.28, 0.45]

    noteDensity_ = [0.05, 0.175, 0.25]
    restDensity_  = [0.002, 0.002, 0.006]
    rhythmicRange_ = [0.1, 0.1333, 0.2]
    rhythmicVariety_ = [0.1, 0.25, 0.35]

    val = 0
    val += (pitchVariety(track), pitchVariety_)
    val += (keyCentric(track), keyCentric_)
    rhy_features = rhythmEvaluator(track)
    val += (rhy_features[0], noteDensity_)
    val += (rhy_features[1], restDensity_)
    val += (rhy_features[2], rhythmicRange_)
    val += (rhy_features[3], rhythmicVariety_)

    return val

# PitchFeatures
def pitchEvaluator(track):
    trackNotes = MusicGene.getNotes(track)

    pitchesHeard = set([])
    noteCount = 0
    for notes, duration in trackNotes:
        if len(notes):
            pitchesHeard.add(int(notes[0]))
        noteCount += 1
    min_pitch, max_pitch  = min(pitchesHeard), max(pitchesHeard)

    pitchVariety_ = float(len(pitchesHeard))/noteCount
    if (max_pitch - min_pitch) > 24: 
        pitchRange_ = 1
    else: 
        pitchRange_ = float(max_pitch - min_pitch)/24

    features = (pitchVariety_, pitchRange_)

    return features

def pitchVariety(track):
    trackNotes = MusicGene.getNotes(track)

    pitchesHeard = set([])
    noteCount = 0
    for notes, duration in trackNotes:
        if len(notes):
            pitchesHeard.add(int(notes[0]))
        noteCount += 1
    return float(len(pitchesHeard))/noteCount

def pitchRange(track):
    trackNotes = MusicGene.getNotes(track)

    max_pitch = 0
    min_pitch = 1000    # Randomly huge number
    pitchesHeard = set([])
    noteCount = 0
    for notes, duration in trackNotes:
        if len(notes):
            if int(notes[0]) < min_pitch:
                min_pitch = int(notes[0])
            elif int(notes[0]) > max_pitch:
                max_pitch = int(notes[0])
    if (max_pitch - min_pitch) > 24: return 1
    else: return float(max_pitch - min_pitch)/24

# TonalityFeatures

def isTonic(key, note):
    if isinstance(key, Note): key = key.name
    if isinstance(note, Note): note = note.name
    if (note == key) or (note == intervals.fifth(key, note)):   # Dominant or tonic
        return True
    else:
        return False

def tonalityEvaluator(track):
    primaryQuantaCount = 0 
    nonScaleCount = 0 
    quantaCount = 0 
    dissonantCount = 0
    noteCount = 0

    note_ = None
    for bar in track:
        for beat, duration, notes in bar:
            if len(notes) > 0:
                if isTonic(bar.key, notes[0]):
                    primaryQuantaCount+=(128/duration)

                if notes[0] not in scales.get_notes(bar.key.name):
                    nonScaleCount+=(128/duration)

                note = notes[0]
                if note_ == None: note_ = note
                if intervals.is_dissonant(note_.name, note.name):
                    dissonantCount += 1
                noteCount += 1
                note_ = note

            quantaCount += (128/duration)

    keyCentric_ = float(primaryQuantaCount)/quantaCount
    nonScaleNotes_ = float(nonScaleCount)/quantaCount
    dissonance_ = float(dissonantCount)/(noteCount-1)

    features = (keyCentric_, nonScaleNotes_, dissonance_)

    return features

def keyCentric(track):
    primaryQuantaCount = 0 
    quantaCount = 0 
    for bar in track:
        for beat, duration, notes in bar:
            if len(notes) > 0:
                if isTonic(bar.key, notes[0]):
                    primaryQuantaCount+=(128/duration)
            quantaCount += (128/duration)
    return float(primaryQuantaCount)/quantaCount

def nonScaleNotes(track):
    nonScaleCount = 0 
    quantaCount = 0 
    for bar in track:
        for beat, duration, notes_ in bar:
            if len(notes_) > 0:
                if notes_[0] not in scales.get_notes(bar.key.name):
                    nonScaleCount+=(128/duration)
            quantaCount += (128/duration)
    return float(nonScaleCount)/quantaCount

def dissonance(track):
    trackNotes = MusicGene.getNotes(track)

    dissonantCount = 0
    noteCount = 0
    note_ = None
    for notes_, duration in trackNotes:
        if len(notes_) > 0:
            note = notes_[0]
            if note_ == None: note_ = note
            if intervals.is_dissonant(note_.name, note.name):
                dissonantCount += 1
            noteCount += 1
            note_ = note

    return float(dissonantCount)/(noteCount-1)

# RhythmEvaluators:
def rhythmEvaluator(track):
    """ Combines all the rhythm evalutions in one for efficiency"""

    quantaCount = 0

    noteCount = 0
    restCount = 0

    durations = set([])

    min_duration = 128
    max_duration = 0.25

    offNotes = 0

    for bar in track:
        for beat, duration, notes in bar:
            if len(notes) == 0:
                restCount += 1
            else:
                noteCount += 1

            quantaCount += (128/duration)   # The largest duration (remember it's inverse) 128

            durations.add(duration)

            if duration > max_duration:
                max_duration = duration
            if duration < min_duration:
                min_duration = duration

            if duration <= 4 and math.modf(4*beat/0.25)[0] != 0:
                offNotes += 1
            noteCount += 1
    noteDensity_ = float(noteCount)/quantaCount
    restDensity_ = float(restCount)/quantaCount
    rhythmicVariety_ = float(len(durations))/16
    rhythmicRange_ = float(math.log(max_duration,2) - math.log(min_duration,2))/16
    syncopation_ = float(offNotes)/noteCount

    features = (noteDensity_, restDensity_, rhythmicVariety_, rhythmicRange_, syncopation_)

    return features


def noteDensity(track):
    noteCount = 0
    quantaCount = 0
    trackNotes = MusicGene.getNotes(track)
    for notes, duration in trackNotes:
        if len(notes) != 0:
            noteCount += 1
        quantaCount += (128/duration)

    return float(noteCount)/quantaCount

def restDensity(track):
    restCount = 0
    quantaCount = 0
    trackNotes = MusicGene.getNotes(track)
    for notes, duration in trackNotes:
        if len(notes) == 0:
            restCount += 1
        quantaCount += (128/duration)

    return float(restCount)/quantaCount

def rhythmicVariety(track):
    durations = set([])
    trackNotes = MusicGene.getNotes(track)
    for notes, duration in trackNotes:
        durations.add(duration)

    return float(len(durations))/16

def rhythmicRange(track):
    # Note that the durations in mingus are represented as 1/(actual duration) 
    # Thus, 1/4 => 4
    min_duration = 128
    max_duration = 0.25
    trackNotes = Musictrack.getNotes(track)
    for notes, duration in trackNotes:
        if duration > max_duration:
            max_duration = duration
        if duration < min_duration:
            min_duration = duration

    return float(math.log(max_duration,2) - math.log(min_duration,2))/16

def syncopation(track):
    # The paper uses a very small subset defintion of syncopation
    # It only looks at off-beat syncopation
    offNotes = 0
    noteCount = 0
    for bar in track:
        for beat, duration, note in bar:
            if duration <= 4 and math.modf(4*beat)[0] != 0:
                offNotes += 1
            noteCount += 1

    return float(offNotes)/noteCount

def rhythm_fluctuation_evaluator(track):
	"""
	Evalution function which rewards lower no
	of rhythm fluctuations.
	Returns total no of notes / total no of 
	rhythm fluctuations
	"""
	if len(track.bars) == 0:
		return -1
	count=0
	time=0
	time_prev=0
	transition=0
	for bar in track.bars:
		for beat, duration, notes in bar:
			time_prev = time
			if len(notes) == 0:
				time=-1/duration
			else:
				time = 1/duration
			if time_prev != time:
				transition=transition+1
			count=count+1
	return float(count)/transition

