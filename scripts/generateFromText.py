#!/usr/bin/env python

BPM=64

if __name__=="__main__":
    if len(sys.argv) != 3:
        print "Usage: %s <file> <out-dir>"%sys.argv[0]
        sys.exit(-1)

    filename = sys.argv[1]
    outdir = sys.argv[2]

    file = open(filename, "r")
    i=0
    for line in file:
        if line.strip() == "": continue
        if line.strip()[0] == "#": continue

        notes = line.strip().split()
        track = Track()
        for note in notes:
            track.add_notes(note)

        MidiFileOut.write_Track("%s/%s-%d.mid"%(outdir, filename, i), track, BPM)
        i+=1

