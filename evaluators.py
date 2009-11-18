#
# A library of various track evalutors
#

from mingus.containers import *
from mingus.core import *
from mingus.midi import fluidsynth
import MusicGene

import math


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
def rhythmEvalutor(track):
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

            durations = durations.add([duration])

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
        durations = durations.add([duration])

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
            if duration <= 4 and math.modf(4*beat/0.25)[0] != 0:
                offNotes += 1
            noteCount += 1

    return float(offNotes)/noteCount
