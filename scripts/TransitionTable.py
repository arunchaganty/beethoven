import pdb
from mingus.core import *
from mingus.containers import *

import re,random

LEAP = 5
SKIP = 3
UNISON = 0
PitchRange = range(1,5)
IntervalRange = range(-11,12)

def xor(x, y):
    return (x and not y) or (not x and y)

def xnor(x, y):
    return (x and y) or (not x and not y)

# Whether this sequence maintains registral direction
def registral(old, new):
    return (old > 0 and new > 0) or (old < 0 and new < 0)

def is_leap(interval):
    return abs(interval)>=LEAP
def is_step(interval):
    return abs(interval)>SKIP and abs(interval) <= LEAP
def is_skip(interval):
    return abs(interval)>UNISON and abs(interval) <= SKIP
def is_unison(interval):
    return abs(interval)==UNISON

def get_pitch(note):
    pitch_re = re.compile("([^-]*)-([0-9])")
    match = pitch_re.match(note)
    if not match: raise ValueError
    else: return int(match.groups()[1])

def get_note(note):
    pitch_re = re.compile("([^-]+)-([0-9])")
    match = pitch_re.match(note)
    if not match: raise ValueError
    else: return match.groups()[0]

# Whether this sequence maintains intervallic direction 
# It's ok as long as you take a short jump after a long jump
def intervallic(old, new):
    return not ((abs(old) >= LEAP) and (abs(new) >= SKIP))

class TransitionTable:
    def __init__(self, scale):
        self.scale = scale
        self.__create_ttable()

    def __create_ttable(self):
        self.ttable = {}

    def transit(self, state):
        #pdb.set_trace()
        val = random.random()
        cdf = 0
        for state_, p in self.ttable[state]:
            if p == 0: continue 
            if cdf < val  and val < cdf + p:
                return state_
            cdf += p
        assert (0)

class MonoTransitionTable(TransitionTable):
    """
    Creates a transition table which uses only the last note to determine the next note
    """
    def __init__(self, scale):
        TransitionTable.__init__(self,scale)
        self.__create_ttable()

    def transit(self, state):
        return TransitionTable.transit(self, state)

    def wt(self, old, new):
        val = 0
        old_note, old_pitch = old
        new_note, new_pitch = new

        interval = 12*(new_pitch - old_pitch) + (notes.note_to_int(new_note) - notes.note_to_int(old_note))

        if new_pitch not in PitchRange: val = 0
        else: val = 0.25

        return val

    def __create_ttable(self):
        # Currently assume equiprobable distribution
        # Indexed by previous interval and current interval
        ttable = {}

        len_ = len(self.scale)

        kv = []
        for pitch in PitchRange:
            for note in self.scale:
                kv.append(("%s-%d"%(note, pitch), self.__create_trans(note,pitch)))

        ttable = dict(kv)
        #pdb.set_trace()
        self.ttable = ttable

    def __create_trans(self, note, pitch):
        trans = []
        norm = sum([self.wt((note,pitch),(note_,pitch_)) for note_ in self.scale for pitch_ in (pitch-1,pitch,pitch+1)])
        for note_ in self.scale:
            for pitch_ in (pitch-1,pitch,pitch+1):
                trans.append(("%s-%d"%(note_,pitch_), float(self.wt((note,pitch),(note_,pitch_))/norm)))
        return trans

class IntervallicTransitionTable(TransitionTable):
    def __init__(self, scale):
        TransitionTable.__init__(self,scale)
        self.__create_ttable()

    def transit(self, state):
        # Here the state has to be derived from the input - which are a set of
        # notes

        note1, note2 = state
        interval, pitch = int(Note(note2)) - int(Note(note1)), get_pitch(note2)
        state = (interval,pitch)

        while(True):
            state_ = TransitionTable.transit(self, state)
            interval, pitch = state_
            note3 = intervals.get_interval(get_note(note2), interval)
            # Limiting Dissonance seems to make a _huge_ improvement to output
            # Getting rid of Dissonance all together is _even better_
            if (intervals.is_dissonant(get_note(note2), note3)):
                continue
                #if random.random() > 0.01: continue # Cut off any dissonant transitions with high probability
            try:
                self.scale.index(note3)
                note3 = "%s-%d"%(note3,pitch)
                break
            except ValueError:
                continue

        state_ = (note2, note3)

        return state_

    def wt(self, old, new):
        val = 0
        old_interval, old_pitch = old
        new_interval, new_pitch = new

        if new_pitch not in PitchRange: val = 0
        elif intervallic(old_interval, new_interval) and is_unison(new_interval): val = 0.05
        elif not intervallic(old_interval, new_interval) and is_unison(new_interval): val = 0.05

        elif intervallic(old_interval, new_interval) and is_leap(old_interval) and registral(old_interval, new_interval): val = 0.4
        elif intervallic(old_interval, new_interval) and is_leap(old_interval) and not registral(old_interval, new_interval): val = 0.6

        elif intervallic(old_interval, new_interval) and not is_leap(old_interval) and registral(old_interval, new_interval): val = 0.5
        elif intervallic(old_interval, new_interval) and not is_leap(old_interval) and not registral(old_interval, new_interval): val = 0.5

        elif not intervallic(old_interval, new_interval) and registral(old_interval, new_interval): val = 0.2
        elif not intervallic(old_interval, new_interval) and not registral(old_interval, new_interval): val = 0.2

        return val

    def __create_ttable(self):
        """
        Creates a transition table for a particular scale
        """
        # Currently assume equiprobable distribution
        # Indexed by previous interval and current interval
        ttable = {}

        len_ = len(self.scale)

        kv = []
        for pitch in PitchRange:
            for interval in IntervalRange:
                kv.append(((interval, pitch), self.__create_trans(interval,pitch)))

        ttable = dict(kv)
        #pdb.set_trace()
        self.ttable = ttable

    def __create_trans(self, interval, pitch):
        trans = []
        norm = sum([self.wt((interval,pitch),(interval_,pitch_)) for interval_ in IntervalRange for pitch_ in (pitch-1,pitch,pitch+1)])
        for interval_ in IntervalRange:
            for pitch_ in (pitch-1,pitch,pitch+1):
                trans.append(((interval_,pitch_), float(self.wt((interval,pitch),(interval_,pitch_))/norm)))
        return trans


