#!/usr/bin/env python
#
#   Beethoven 
#

import pdb

import sys
import time
import genetic
from Gene import *
from MusicGene import *

SF2 = "/usr/share/soundfonts/fluidr3/FluidR3GM.SF2"
DRIVER = "alsa"

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

def print_popluation(population, play=False):
    for i in xrange(len(population)):
        track = population[i]
        print "Track #%d:"%i
        print track
        if play: 
            track.play()
            time.sleep(1)
    return


if __name__ == "__main__":
    verbose = False
    play = False

    if len(sys.argv) == 2:
        if sys.argv[1] == "-v" or sys.argv[1] == "--verbose":
            verbose = True
        elif sys.argv[1] == "-vv" or sys.argv[1] == "--very-verbose":
            verbose = True
            play = True
        elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print "Usage: %s [-v|-vv|-h]"%(sys.argv[0])
            sys.exit(-1)
        else:
            print "Usage: %s [-v|-vv|-h]"%(sys.argv[0])
            sys.exit(-1)

    if play: fluidsynth.init(SF2, DRIVER)
    population = import_population("initial.db")
    g = genetic.evolve(population)

    print "Generation #%d"%0
    if verbose and False:
        print_popluation(population, play)

    for i in xrange(10):
        pop = g.next()
        print "Generation #%d"%(i+1)
    if verbose:
        print_popluation(population, play)
    
        
