import pdb
import random

from Gene import Gene
from mingus.containers import *
from mingus.core import *
from mingus.midi import fluidsynth

from evaluators import *
from crossovers import *

def getNotes(track):
    """ Gets (notes, duration) from all bars"""
    assert(isinstance(track, Track))

    for bar in track:
        for beat, duration, notes in bar:
            yield notes,duration

def convert_to_track(track):
    """ Convert our notation of a track to a mingus one """
    assert(not isinstance(track, Track))
    track_ = Track()
    for notes, duration in track:
        track_.add_notes(notes, duration)

    return track_

class MusicGene(Gene):
    def __init__(self, track):
        self.track = track
        Gene.__init__(self)

    def __str__(self):
        str_ = "MusicGene: " + "fitness " + str(self.fitness) + '\n' 
        str_ += str(self.track)
        return str_

    def __repr__(self):
        return str(self)

    def print_track(self, track):
        return str(self.track)

    def get_fitness(self):
        fitness = 0.1
        return fitness

    def mate(self, other):
        return self
        #return interleaved_single_pt_crossover(self, other)

    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(track)

