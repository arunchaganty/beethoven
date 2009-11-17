import pdb
from mingus.core import *
from mingus.containers import *
import random

import TransitionTable
PitchRange = range(1,6)

class MusicComposer:
    """
    A music composer who constructs a couple of bars from a given scale
    """

    def __init__(self, scale):
        self.scale = scale

    def compose_track(self, n_bars):
        track = Track()
        g = self.compose()
        for i in xrange(4*n_bars):
            track.add_notes(Note(g.next()))

        return track

    def compose(self):
        while(1):
            yield self.scale[0]

class RandomComposer(MusicComposer):
    """ Generates notes from the scale completely randomly """
    def compose(self):
        while(1):
            yield "%s-%d"%(random.choice(self.scale), random.choice(PitchRange))

class NoobComposer(MusicComposer):
    """Generates notes using a simple state machine"""
    def __init__(self, scale):
        MusicComposer.__init__(self, scale)
        self.ttable = TransitionTable.MonoTransitionTable(scale)

    def compose(self):
        """
        Composes another bar of music
        """
        cur_note = "%s-%d"%(random.choice(self.scale), 3)
        while(1):
            yield cur_note
            note_ = self.ttable.transit(cur_note)
            cur_note = note_

class NoviceComposer(MusicComposer):
    """Generates notes using a simple state machine"""
    def __init__(self, scale):
        MusicComposer.__init__(self, scale)
        self.ttable = TransitionTable.IntervallicTransitionTable(scale)

    def compose(self):
        cur_note = "%s-%d"%(random.choice(self.scale), 3)
        state = (cur_note, cur_note)
        while(1):
            yield cur_note
            state_ = self.ttable.transit(state)
            cur_note = state_[1]


