import pdb
from mingus.core import *
from mingus.containers import *
import random

LEAP = 7
SKIP = 3
UNISON = 0
PitchRange = range(1,6)

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


def is_flat(interval):
    return interval == 0

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
        norm = sum([self.wt((note,pitch),(note_,pitch_)) for note_ in self.scale for pitch_ in (-1,0,1)])
        for note_ in self.scale:
            for pitch_ in (pitch-1,pitch,pitch+1):
                trans.append(("%s-%d"%(note_,pitch_), float(self.wt((note,pitch),(note_,pitch_))/norm)))
        return trans

class IntervallicTransitionTable(TransitionTable):
    def wt(self, old, new):
        val = 0
        if intervallic(old, new) and is_flat(new): val = 0.05
        elif not intervallic(old, new) and is_flat(new): val = 0.05

        elif intervallic(old, new) and is_leap(old) and registral(old, new): val = 0.4
        elif intervallic(old, new) and is_leap(old) and not registral(old, new): val = 0.6

        elif intervallic(old, new) and not is_leap(old) and registral(old, new): val = 0.5
        elif intervallic(old, new) and not is_leap(old) and not registral(old, new): val = 0.5

        elif not intervallic(old, new) and registral(old, new): val = 0.2
        elif not intervallic(old, new) and not registral(old, new): val = 0.2

        return val

    def __create_ttable(self):
        """
        Creates a transition table for a particular scale
        """
        # Currently assume equiprobable distribution
        # Indexed by previous interval and current interval
        ttable = {}

        len_ = len(self.scale)

        keys = [(i,j) for i in range(-11, 12) for j in range(-11,12)]
        normal=[sum([self.wt(i, j) for j in xrange(-11,12)]) for i in range(-11,12)]
        kv = [(k,float(self.wt(*k))/normal[11+k[0]]) for k in keys]

        ttable = dict(kv)

        self.ttable = ttable

