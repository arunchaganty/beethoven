#
#   Beethoven 
#

import pdb

import genetic
from Gene import *
from MusicGene import *

SF2 = "/usr/share/soundfonts/fluidr3/FluidR3GM.SF2"
DRIVER = "alsa"

def import_population(filename):
    file = open(filename, "r")

    population = []
    for track in file:
        notes = track.split()
        track = Track()
        for note in notes:
            track.add_notes(note)
        gene = MusicGene(track)
        population.append(gene)

    return population

if __name__ == "__main__":
    fluidsynth.init(SF2, DRIVER)

    population = import_population("initial.db")
    g = genetic.evolve(population)

    print "Generation #%d"%0
    for i in xrange(len(population)):
        print "Track #%d"%i
        population[i].play()

    for i in xrange(10):
        pdb.set_trace()
        pop = g.next()
        print "Generation #%d"%i
        for i in xrange(len(population)):
            print "Track #%d"%i
            population[i].play()
        

