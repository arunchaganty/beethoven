
from mingus.containers import *
from mingus.core import *
from mingus.midi import fluidsynth

import MusicGene
import random

def interleaved_single_pt_crossover(gene1, gene2):
    if (random.randint(0,1)):
        return single_pt_crossover(gene1, gene2)
    else:
        return interleave_crossover(gene1, gene2)

def double_pt_crossover(gene1, gene2):
    # Most naive method - interleave bars
    #print "Mating:"
    #print "P1: " + gene1.print_track(gene1.track)
    #print "P2: " + gene1.print_track(gene2.track)
    assert(len(gene1.track) == len(gene2.track))
    children = []

    crossover = random.randint(0,len(gene1.track))
    crossover_ = random.randint(crossover,len(gene1.track))

    child = []
    child_ = []
    for i in xrange(len(gene1.track)):
        note = gene1.track[i]
        note_ = gene2.track[i]

        if i < crossover or i > crossover_:
            child.append(note)
            child_.append(note_)
        else:
            child.append(note_)
            child_.append(note)

    children += [MusicGene.MusicGene(child), MusicGene.MusicGene(child_)]

    return children

def crossover_bars(bar, bar_):
    new_bar = Track()
    new_bar_ = Track()

    # Find notes which share a beat
    shared_beats = []
    for beat, duration, note in bar:
        for beat_, duration_, note_ in bar_:
            if beat == beat_: shared_beats.append(beat)

    beat_crossover = random.choice(shared_beats)
    i,j = 0,0
    while(i < len(bar) or j < len(bar_)):
        if i < len(bar): beat, duration, note = bar[i]
        else: beat = 1
        if j < len(bar_): beat_, duration_, note_ = bar_[j]
        else: beat_ = 1

        if i < len(bar) and beat < beat_crossover:
            new_bar.add_notes(note, duration)
            i += 1
        elif j < len(bar_) and beat_ < beat_crossover:
            new_bar_.add_notes(note_, duration_)
            j += 1

        if beat >= beat_crossover and beat_ >= beat_crossover:
            if i < len(bar):
                new_bar_.add_notes(note, duration)
                i+=1
            if j < len(bar_):
                new_bar.add_notes(note_, duration_)
                j+=1
   
    assert(len(new_bar) == 1)
    assert(len(new_bar_) == 1)

    return new_bar[0], new_bar_[0]

def single_pt_crossover(gene1, gene2):
    # Most naive method - interleave bars
    #print "Mating:"
    #print "P1: " + gene1.print_track(gene1.track)
    #print "P2: " + gene1.print_track(gene2.track)
    children = []

    bar_crossover = random.randint(0,len(gene1.track))

    child = Track()
    child_ = Track()

    len_ = len(gene1.track)
    if len_ > len(gene2.track): len_ = len(gene2.track)
    for i in xrange(len_):
        bar = gene1.track[i]
        bar_ = gene2.track[i]

        if i < bar_crossover:
            child.add_bar(bar)
            child_.add_bar(bar_)
        elif i > bar_crossover:
            child.add_bar(bar_)
            child_.add_bar(bar)
        # At crossover
        else:
            new_bar, new_bar_ = crossover_bars(bar, bar_)
            child.add_bar(new_bar)
            child_.add_bar(new_bar_)

    children.append(MusicGene.MusicGene(child))
    children.append(MusicGene.MusicGene(child_))

    return children

def interleave_crossover(gene1, gene2):
    assert(len(gene1.track) == len(gene2.track))

    children = []

    child = []
    child_ = []
    for i in xrange(len(gene1.track)):
        note = gene1.track[i]
        note_ = gene2.track[i]

        if i%2 == 0:
            child.append(note)
            child_.append(note_)
        else:
            child.append(note_)
            child_.append(note)

    children += [MusicGene.MusicGene(child), MusicGene.MusicGene(child_)]
    return children

