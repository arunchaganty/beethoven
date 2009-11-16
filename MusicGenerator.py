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

class NoviceComposer(MusicComposer):
    """Generates notes using a simple state machine"""
    def __init__(self, scale):
        MusicComposer.__init__(self, scale)
        self.ttable = MonoTransitionTable(scale)

    def compose(self):
        """
        Composes another bar of music
        """
        cur_note = random.choice(self.scale)
        cur_pitch = 3
        cur_interval = 0

        len_ = len(self.scale)

        intervals_ = [i for i in range(-len_,len_+1)]
        while(1):
            pitch_ = -1
            interval_ = 0
            #pdb.set_trace()

            while pitch_ <= 0 or pitch_ > 5:
                pitch_ = cur_pitch
                val = random.random()
                cdf = 0
                for i_, p in ((interval, self.ttable[(cur_interval, interval)]) for interval in intervals_):
                    if cdf < val and val < cdf + p:
                        interval_ =  i_
                        break
                    else:
                        cdf += p
                note_ = intervals.get_interval(cur_note, interval_)
                try:
                    self.scale.index(note_)
                    if (interval_) < 0:
                        pitch_-=1
                        interval_ = interval_ + 12
                    elif (interval_) > 12:
                        pitch_+=1
                        interval_ = interval_ - 12
                except ValueError:
                    pitch_ = -1

            cur_pitch = pitch_
            cur_interval = interval_
            cur_note = intervals.get_interval(cur_note, interval_)
            print cur_note, cur_pitch, cur_interval

            yield "%s-%d"%(cur_note,cur_pitch)

