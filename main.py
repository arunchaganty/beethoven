#!/usr/bin/env python
#
#   Beethoven 
#

import pdb

import sys
import os
import time
import re
import random

import genetic
from Gene import *
from MusicGene import *
from mingus.midi import *

SF2 = "/usr/share/soundfonts/fluidr3/FluidR3GM.SF2"
DRIVER = "alsa"

DB_DIR = "awesomeSet"

def chop_evenly(track, n_bars):
    """
    Evenly chop up a track into sets of 'n_bars' bars
    Discards an uneven set of bars at the very end
    """

    tracks = [] 
    bars = track.bars[:]
    while(len(bars) > n_bars):
        bars_ = bars[:n_bars]
        bars = bars[n_bars:]

        track_ = Track()
        track_.bars = bars_

        tracks.append(track_)
        
    return tracks 

def import_midi_db(dir):
    mid_re = re.compile(".*\.mid$")
    population = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            print file 
            if mid_re.match(file):
                composition, bpm = MidiFileIn.MIDI_to_Composition(os.path.join(root,file))
                genes = [MusicGene(track) for track in  composition]
                for gene in genes:
                    gene.bachian = True
                population += genes

    return population

def import_population(filename):
    file = open(filename, "r")

    population = []
    for track in file:
        if track.strip() == "": continue
        if track.strip()[0] == "#": continue

        notes = track.strip().split()
        track = Track()
        for note in notes:
            track.add_notes(note)
        gene = MusicGene(track)
        population.append(gene)

    return population

def save_tracks(population):
    for i in xrange(len(population)):
        gene = population[i]
        if (gene.bachian): continue
            
        try:
            MidiFileOut.write_Track("HannaMontana-%d-%d.mid"%(i, gene.fitness), gene.track, bpm=64)
        except:
            pass

def print_popluation(population, play=False, all=False):
    if all:
        cnt = len(population)
    else:
        if len(population) < 0:
            cnt = len(population)
        else:
            cnt = 3

    for i in xrange(cnt):
        track = population[i]
        if track.bachian: continue
        print "Track #%d:"%i
        print track
        if play: 
            track.play()
            time.sleep(1)
    return


if __name__ == "__main__":
    verbose = False
    play = False
    all = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "-v" or sys.argv[1] == "--verbose":
            verbose = True
        elif sys.argv[1] == "-vv" or sys.argv[1] == "--very-verbose":
            verbose = True
            play = True
        elif sys.argv[1] == "-vvv" or sys.argv[1] == "--very-verbose":
            verbose = True
            play = True
            all = True
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print "Usage: %s [-v|-vv|-h]"%(sys.argv[0])
            sys.exit(-1)
        else:
            print "Usage: %s [-v|-vv|-h]"%(sys.argv[0])
            sys.exit(-1)

    if play: fluidsynth.init(SF2, DRIVER)
    population = import_midi_db(DB_DIR)
    #population = import_population("initial.db")
    g = genetic.evolve(population, 200, 0.1)

    print "Generation #%d (size=%d)"%(0, len(population))
    #if verbose:
    #    print_popluation(population, play, all)

    for i in xrange(40):
        pop = g.next()
        #if verbose:
        #    print_popluation(population, play, all)
        print "Generation #%d (size=%d)"%((i+1),len(population))
    if verbose:
        print_popluation(population, play, True)

    #Save stuff!
    save_tracks(population)

    
    
        
