#!/usr/bin/env python
import evaluators
from mingus.midi import MidiFileIn 


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Usage: %s <midi-file>"%(sys.argv[0])
        sys.exit(-1)

    filename = sys.argv[1]

    composition, bpm = MidiFileIn.MIDI_to_Composition(filename)
    track = composition[0]

    print "%s %s"%(filename, evaluators.numericEvaluation(track))

