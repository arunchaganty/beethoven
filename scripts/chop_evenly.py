#!/usr/bin/env python

from mingus.midi import *

def chop_evenly(track, n_bars):
    """
    Evenly chop up a track into sets of 'n_bars' bars
    Discards an uneven set of bars at the very end
    """
    tracks = [] 
    bars = track.bars[:]
    while(len(bars) > n_bars):
        bars_ = bars[:n_bars]
        bars = bars[n_bars:]

        track_ = Track()
        track_.bars = bars_

        tracks.append(track_)
        
    return tracks 

if __name__=="__main__":
    if len(sys.argv) != 4:
        print "Usage: %s <bars> <midi-db> <out-dir>"%sys.argv[0]
        sys.exit(-1)

    bars = sys.argv[1]
    mididb = sys.argv[2]
    outdir = sys.argv[3]


    mid_re = re.compile(".*\.mid$")
    for root, dirs, files in os.walk(mididb):
        for file in files:
            print file 
            if mid_re.match(file):
                composition, bpm = MidiFileIn.MIDI_to_Composition(os.path.join(root,file))
                for track in composition:
                    even_tracks = chop_evenly(track, bars)
                    for i in xrange(len(even_tracks)):
                        MidiFileOut.write_Track("%s/%s-%d.mid"%(outdir, os.path.basename(file), i), even_tracks[i], bpm)

