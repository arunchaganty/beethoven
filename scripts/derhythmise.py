#!/usr/bin/env python

from mingus.containers import *
from mingus.core import *
from mingus.midi import *
import os

def derhythmise(track):
    bars = track.bars[:]
    track_ = Track()
    for bar in bars:
        for beat, duration, notes in bar:
            track_.add_notes(notes)
    return track_

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: %s <midi-file>"%sys.argv[0]
        sys.exit(-1)

    file = sys.argv[1]
    if file.rfind(".mid") == -1:
        print "%s is not a MIDI file"%(file)
        sys.exit(-1)

    composition, bpm = MidiFileIn.MIDI_to_Composition(file)

    for i in xrange(len(composition)):
        track = composition[i]
        track_ = derhythmise(track)
        file = os.path.basename(file)
        basename = file[:file.rfind('.mid')]
        MidiFileOut.write_Track("%s-%d.mid"%(basename,i), track_)

    
