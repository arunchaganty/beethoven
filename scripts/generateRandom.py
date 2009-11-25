#!/usr/bin/env python

import sys
from mingus.containers import *
from mingus.midi import *
from MusicGenerator import *

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "Usage: %s <scale> <bars> <pieces>"%sys.argv[0]
        sys.exit(-1)

    scale = sys.argv[1]
    bars = int(sys.argv[2])
    pieces = int(sys.argv[3])

    composer = NoviceComposer(scale)
    for i in xrange(pieces):
        piece = composer.compose_track(bars)
        MidiFileOut.write_Track("random%s-%d.mid"%(scale,i), piece)

