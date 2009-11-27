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

import optparse

import genetic
from Gene import *
from MusicGene import *
from mingus.midi import *

SF2 = "/usr/share/soundfonts/fluidr3/FluidR3GM.SF2"
DRIVER = "alsa"

def ticker():
    i = 0
    chr = ['|','/','-','\\']
    while True:
        i = (i+1) % (len(chr))
        sys.stderr.write("\b%s"%chr[i])
        yield

def import_midi_db(dir):
    sys.stderr.write("Importing samples from %s:  "%mididb)
    tick = ticker()

    mid_re = re.compile(".*\.mid$")
    population = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            tick.next()
            if mid_re.match(file):
                composition, bpm = MidiFileIn.MIDI_to_Composition(os.path.join(root,file))
                genes = [MusicGene(track) for track in  composition]
                for gene in genes:
                    gene.bachian = True
                population += genes
    sys.stderr.write("\n")
    return population

def save_tracks(population, outdir):
    try:
        os.stat(outdir)
    except OSError:
        os.mkdir(outdir)

    sys.stderr.write("Saving riff database:  ") 
    tick = ticker()
    for i in xrange(len(population)):
        tick.next()
        gene = population[i]
        if (gene.bachian): continue
            
        try:
            MidiFileOut.write_Track("%s/HannaMontana-%d-%d.mid"%(outdir, i, gene.fitness), gene.track, bpm=64)
        except:
            print "Error writing %s/HannaMontana-%d-%d.mid"%(outdir, i, gene.fitness)
            pass
    sys.stderr.write("\n")

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

def create_riff_db(initial_pop, options):
    """
    Create a database of riffs to be used by the "composer" to generate it's master pieces
    """

    # Ideally categorise or create new riff_dbs for every scale?
    sys.stderr.write("Creating riff database:  ") 
    tick = ticker()

    g = genetic.evolve(initial_pop, options.pop_limit, options.mutation_rate)
    for i in xrange(options.generations):
        tick.next()
        g.next()
    sys.stderr.write("\n") 
    pop = g.next()

    return pop

if __name__ == "__main__":
    verbose = False
    play = False
    all = False

    parser = optparse.OptionParser()
    parser.add_option("-l", "--loud", action="store_true", dest="loud",
            help="Play generated tracks", default=False)
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="Print out generated tracks", default=True)
    parser.add_option("-n", "--num", type="int", dest="num",
            help="Print/play only the top 'n' tracks", default=3)
    parser.add_option("-g", "--generations", type="int", dest="generations",
            help="Number of generations to be evolved", default=20)
    parser.add_option("-p", "--population-limit", type="int", dest="pop_limit",
            help="Population Limit", default=200)
    parser.add_option("-m", "--mutation-rate", type="float", dest="mutation_rate",
            help="Population Limit", default=0.3)
    parser.add_option("-c", "--create", action="store_true", dest="create",
            help="Use input MIDI to create riffs", default=False)
    parser.add_option("-i", "--input", dest="input",
            help="Input MIDI directory")
    parser.add_option("-o", "--output", dest="output",
            help="Output MIDI directory")

    (options, args) = parser.parse_args()

    if options.loud:
        fluidsynth.init(SF2, DRIVER)

    mididb = options.input
    outdir = options.output

    if options.create:
        initial_pop = import_midi_db(mididb)
        db = create_riff_db(initial_pop, options)
        save_tracks(db, outdir)
    else:
        sys.stderr.write("Loading riff db from %s\n"%mididb)
        initial_pop = import_midi_db(mididb)
        # do something

        
