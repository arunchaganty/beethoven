import pdb
import random

from Gene import Gene
from mingus.containers import *
from mingus.core import *
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

def remove_duplicates(lst):
    assert(len(lst) > 0)
    lst.sort()
    lst_ = []
    x = lst[0]
    lst_.append(x)
    for i in lst:
        if i == x: continue
        x = i
        lst_.append(x)

    return lst_

def merge_note_container(noteC):
    key = [normalise_note(note) for note in noteC]
    key = remove_duplicates(key)
    if len(key) == 1: 
        return Note(key[0])
    chord = chords.determine(key, True, True, True)

    if chord and notes.is_valid_note(chord[0]):
        if len(chord) > 1 and (chord[1] == '#' or chord[1] == 'b'):
            return Note(chord[:2])
        else:
            return Note(chord[0])
    else: 
        return None

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

# TODO: Should be a state machine that keeps track of the last (say) 2 - 3 notes
def contour_evaluator(track):
    # Check difference between first and last notes to get the "direction" of
    # the bar

    wt = (0.4, 0.5, 0.2)

    contour = (0, 0, 0)

    dir = 0
    note = Note()
    for bar in track:
        for beat_, duration_, note_ in bar:
            if not note_: continue
            note_ = merge_note_container(note_)
            if not note_: continue
            dir_ = int(note_) - int(note)

            if (dir > 0 and dir_ > 0) or (dir < 0 and dir_ < 0): contour = vector_sum(contour,(1, 0, 0))
            elif (dir < 0 and dir_ > 0) or (dir > 0 and dir_ < 0): contour = vector_sum(contour,(0, 1, 0))
            elif dir_ == 0: contour = vector_sum(contour,(0, 0, 1))
            dir = dir_
    if sum(contour):
        contour = tuple([value/sum(contour) for value in contour])

    return inner_pdt(contour, wt)

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
        wt = (0.5, 1)
        features = (range_evaluator(self.track), contour_evaluator(self.track))
        #wt = (0.5,)
        #features = (range_evaluator(self.track),)
        fitness = inner_pdt(wt, features)
        return fitness

    def mate(self, other):
        return self.interleaved_single_pt_crossover(other)

    def interleaved_single_pt_crossover(self, other):
        if (random.randint(0,1)):
            return self.single_pt_crossover(other)
        else:
            return self.interleave_crossover(other)

    def single_pt_crossover(self, other):
        # Most naive method - interleave bars
        #print "Mating:"
        #print "P1: " + self.print_track(self.track)
        #print "P2: " + self.print_track(other.track)
        assert(len(self.track) == len(other.track))
        children = []

        note_count = 0
        for bar in self.track:
            note_count += len(bar)
        crossover = random.randint(0, note_count)

        child = Track()
        child_ = Track()
        note_count = 0
        for i in xrange(len(self.track)):
            bar = self.track[i]
            bar_ = other.track[i]
            for j in xrange(len(bar)):
                beat, duration, notes = bar[j]
                beat_, duration_, notes_ = bar_[j]
                note_count+=1
                if note_count < crossover:
                    child.add_notes(notes, duration)
                    child_.add_notes(notes_, duration_)
                else:
                    child.add_notes(notes_, duration_)
                    child_.add_notes(notes, duration)

        children += [MusicGene(child), MusicGene(child_)]

        return children

    def interleave_crossover(self, other):
        assert(len(self.track) == len(other.track))

        children = []

        child = Track()
        child_ = Track()

        note_count = 0
        for i in xrange(len(self.track)):
            bar = self.track[i]
            bar_ = other.track[i]
            for j in xrange(len(bar)):
                beat, duration, notes = bar[j]
                beat_, duration_, notes_ = bar_[j]
                note_count+=1
                if note_count%2:
                    child.add_notes(notes, duration)
                    child_.add_notes(notes_, duration_)
                else:
                    child.add_notes(notes_, duration_)
                    child_.add_notes(notes, duration)

        children += [MusicGene(child), MusicGene(child_)]

        return children

    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(self.track)

