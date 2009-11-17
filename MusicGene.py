import pdb
import random

from Gene import Gene
from mingus.containers import *
from mingus.core import *
from mingus.midi import fluidsynth

from evaluators import *

def convert_from_track(track):
    """ Converts a mingus track to a more convenient notation """
    assert(isinstance(track, Track))
    track_ = []
    for bar in track:
        for beat, duration, notes in bar:
            assert(len(notes) == 1)
            track_.append((notes[0], duration))

    return track_

def convert_to_track(track):
    """ Convert our notation of a track to a mingus one """
    assert(not isinstance(track, Track))
    track_ = Track()
    for note, duration in track:
        track_.add_notes([note], duration)

    return track_

class MusicGene(Gene):
    def __init__(self, track):
        if isinstance(track, Track):
            self.track = convert_from_track(track)
        else:
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
        #wt = (0.5, 1)
        #features = (range_evaluator(self.track), contour_evaluator(self.track))
        #wt = (0.5,)
        #features = (range_evaluator(self.track),)
        #fitness = inner_pdt(wt, features)
        fitness = 0.1
        return fitness

    def mate(self, other):
        return self.interleaved_single_pt_crossover(other)

    def interleaved_single_pt_crossover(self, other):
        if (random.randint(0,1)):
            return self.single_pt_crossover(other)
        else:
            return self.interleave_crossover(other)

    def double_pt_crossover(self, other):
        # Most naive method - interleave bars
        #print "Mating:"
        #print "P1: " + self.print_track(self.track)
        #print "P2: " + self.print_track(other.track)
        assert(len(self.track) == len(other.track))
        children = []

        crossover = random.randint(0,len(self.track))
        crossover_ = random.randint(crossover,len(self.track))

        child = []
        child_ = []
        for i in xrange(len(self.track)):
            note = self.track[i]
            note_ = other.track[i]

            if i < crossover or i > crossover_:
                child.append(note)
                child_.append(note_)
            else:
                child.append(note_)
                child_.append(note)

        children += [MusicGene(child), MusicGene(child_)]

        return children


    def single_pt_crossover(self, other):
        # Most naive method - interleave bars
        #print "Mating:"
        #print "P1: " + self.print_track(self.track)
        #print "P2: " + self.print_track(other.track)
        assert(len(self.track) == len(other.track))
        children = []

        crossover = random.randint(0,len(self.track))

        child = []
        child_ = []
        for i in xrange(len(self.track)):
            note = self.track[i]
            note_ = other.track[i]

            if i < crossover:
                child.append(note)
                child_.append(note_)
            else:
                child.append(note_)
                child_.append(note)

        children += [MusicGene(child), MusicGene(child_)]

        return children

    def interleave_crossover(self, other):
        assert(len(self.track) == len(other.track))

        children = []

        child = []
        child_ = []
        for i in xrange(len(self.track)):
            note = self.track[i]
            note_ = other.track[i]

            if i%2 == 0:
                child.append(note)
                child_.append(note_)
            else:
                child.append(note_)
                child_.append(note)

        children += [MusicGene(child), MusicGene(child_)]
        return children

    def mutate(self):
        return self

    def play(self):
        track = convert_to_track(self.track)
        fluidsynth.play_Track(track)

