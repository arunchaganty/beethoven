import pdb

from Gene import Gene
from mingus.containers import *
from mingus.core import intervals, notes
from mingus.midi import fluidsynth

def normalise_note(note):
    return notes.int_to_note(int(note)%12)

def inner_pdt(x, y):
    assert(len(x) == len(y))

    wt = sum([x[i] * y[i] for i in xrange(len(x))])

    return wt

def vector_sum(x, y):
    assert(len(x) == len(y))

    return tuple([x[i] + y[i] for i in xrange(len(x))])

def range_evaluator(track):
    min, max = track[0].get_range()
    if max == -1: 
        min, max = int(min), int(min)
    else:
        min, max = int(min), int(max)
    for bar in track:
        min_, max_ = bar.get_range()
        if max_ == -1: 
            min_, max_ = int(min_), int(min_)
        else:
            min_, max_ = int(min_), int(max_)
        if min_ < min: min = min_
        if max_ > max: max = max_

    return max - min

def contour_evaluator(track):
    # Check difference between first and last notes to get the "direction" of
    # the bar

    wt = (0.4, 0.5, 0.2)

    contour = (0, 0, 0)
    dir = 1
    for bar in track:
        #pdb.set_trace()
        first, last = bar[0][2],bar[-1][2]
        assert(len(first) == len(last) == 1)
        dir_ = int(last[0]) - int(first[0])
        if (dir > 0 and dir_ > 0) or (dir < 0 and dir_ < 0): contour = vector_sum(contour,(1, 0, 0))
        elif (dir < 0 and dir_ > 0) or (dir > 0 and dir_ < 0): contour = vector_sum(contour,(0, 1, 0))
        elif dir_ == 0: contour = vector_sum(contour,(0, 0, 1))

        dir = dir_

    return inner_pdt(contour, wt)

def consonance_evaluator(track):
    bar = track[0]
    first, last = bar[0][2],bar[-1][2]

    assert(len(first) == len(last) == 1)
    first, last = first[0], last[0]

    dissonants = 0
    for bar in track:
        #pdb.set_trace()
        first_, last_ = bar[0][2],bar[-1][2]
        assert(len(first_) == len(last_) == 1)
        first_, last_ = first_[0] , last_[0]
        if intervals.is_dissonant(normalise_note(last), normalise_note(first_)): dissonants += 1

        first, last = first_, last_


    return dissonants


class MusicGene(Gene):
    def __init__(self, track):
        self.track = track
        Gene.__init__(self)

    def __str__(self):
        str_ = "MusicGene: " + "fitness " + str(self.fitness) + '\n' 
        str_ += self.print_track(self.track)
        return str_

    def __repr__(self):
        return str(self)

    def print_track(self, track):
        str_ = ""
        for bar in track:
            for note in bar:
                str_ += str(note[2]) + " "
        return str_

    def get_fitness(self):
        wt = (0.5, 1, 3)
        features = (range_evaluator(self.track), contour_evaluator(self.track), consonance_evaluator(self.track))
        fitness = inner_pdt(wt, features)
        return fitness

    def mate(self, other):
        # Most naive method - interleave bars
        #print "Mating:"
        #print "P1: " + self.print_track(self.track)
        #print "P2: " + self.print_track(other.track)
        assert(len(self.track) == len(other.track))
        children = []

        track = Track()
        for i in xrange(len(self.track)):
            if i%2 == 0:
                track.add_bar(self.track[i])
            else:
                track.add_bar(other.track[i])

        #print "C1: " + self.print_track(track)

        children.append(MusicGene(track))

        return children


    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(self.track)

