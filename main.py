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

def save_tracks(population, outdir):
    for i in xrange(len(population)):
        gene = population[i]
        if (gene.bachian): continue
            
        try:
            MidiFileOut.write_Track("%s/HannaMontana-%d-%d.mid"%(outdir, i, gene.fitness), gene.track, bpm=64)
        except:
            print "Error writing %s/HannaMontana-%d-%d.mid"%(outdir, i, gene.fitness)
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

    if len(sys.argv) != 4:
        print "Usage: %s [-h|-q|-v|-vv] <midi-db> <outdir>"
        sys.exit(-1)

    if sys.argv[1] == "-h":
        print "Usage: %s [-v|-vv|-h]"%(sys.argv[0])
        sys.exit(0)
    elif sys.argv[1] == "-q" or sys.argv[1] == "--quiet":
        pass
    elif sys.argv[1] == "-v" or sys.argv[1] == "--verbose":
        verbose = True
    elif sys.argv[1] == "-vv" or sys.argv[1] == "--very-verbose":
        verbose = True
        play = True
    elif sys.argv[1] == "-vvv" or sys.argv[1] == "--very-verbose":
        verbose = True
        play = True
        all = True
    else:
        print "Usage: %s [-v|-vv|-h]"%(sys.argv[0])
        sys.exit(-1)

    mididb = sys.argv[2]
    outdir = sys.argv[3]

    if play: fluidsynth.init(SF2, DRIVER)
    population = import_midi_db(mididb)
    g = genetic.evolve(population, 200, 0.1)

    print "Generation #%d (size=%d)"%(0, len(population))

    for i in xrange(40):
        pop = g.next()
        print "Generation #%d (size=%d)"%((i+1),len(population))
    if verbose:
        print_popluation(population, play, True)

    save_tracks(population, outdir)

        
