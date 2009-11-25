import pdb
import random

from Gene import Gene
from mingus.containers import *
from mingus.core import *
from mingus.midi import fluidsynth

from evaluators import *
from crossovers import *
from mutators import *

EXPECTED_CONTOUR = [1,1,2,1]

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
        self.bachian = False

    def __str__(self):
        str_ = "MusicGene [B=%d]: "%self.bachian + "fitness " + str(self.fitness) + '\n' 
        str_ += str(self.track)
        return str_

    def __repr__(self):
        return str(self)

    def print_track(self, track):
        return str(self.track)

    def get_fitness(self):
        val = 0
        val += rhythm_fluctuation_evaluator(self.track)
        val += pitch_class_fluctuation_evaluator(self.track)
        val += dissonant_note_evaluator(self.track)
        val += numericEvaluation(self.track)
        fitness = val
        return fitness

    def mate(self, other):
        children = single_pt_crossover(self, other)
        return children

    def mutate(self):
        algo = random.random()
        if algo < 0.2:
            child = MusicGene(one_note_mutator(self.track))
        else:
            child = MusicGene(permute_duration_mutator(self.track))
        return child

    def play(self):
        fluidsynth.play_Track(self.track)

class CompositionGene(Gene):
    def __init__(self, track):
        self.track = track
        Gene.__init__(self)

    def __str__(self):
        str_ = "CompositionGene: " + "fitness " + str(self.fitness) + '\n' 
        str_ += str(self.track)
        return str_

    def __repr__(self):
        return str(self)

    def print_track(self, track):
        return str(self.track)

    def get_fitness(self):
        val = 0
        val += rhythmicContinuity(self.track)
        val += rhythmicContour(self.track, EXPECTED_CONTOUR)
        fitness = val
        return fitness

    def mate(self, other):
        return []
        #return interleaved_single_pt_crossover(self, other)

    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(self.track)

