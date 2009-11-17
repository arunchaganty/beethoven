
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


def single_pt_crossover(gene1, gene2):
    # Most naive method - interleave bars
    #print "Mating:"
    #print "P1: " + gene1.print_track(gene1.track)
    #print "P2: " + gene1.print_track(gene2.track)
    assert(len(gene1.track) == len(gene2.track))
    children = []

    crossover = random.randint(0,len(gene1.track))

    child = []
    child_ = []
    for i in xrange(len(gene1.track)):
        note = gene1.track[i]
        note_ = gene2.track[i]

        if i < crossover:
            child.append(note)
            child_.append(note_)
        else:
            child.append(note_)
            child_.append(note)

    children += [MusicGene.MusicGene(child), MusicGene.MusicGene(child_)]

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

