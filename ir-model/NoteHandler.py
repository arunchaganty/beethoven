from midi.MidiOutStream import MidiOutStream


class NoteHandler(MidiOutStream):
    """
    This class keeps track of the notes in the midi stream (of a channel), and assigns I-R values based on a 3-note window
    """
    window_table = { (

    #############################
    # channel events
    def __init__(self):
        self.

    
    def window_start(self):
        self.window = (0,0,0)

    def window_push(self, note):
        self.window = (self.window[1], self.window[2], note)
    
    def note_on(self, channel=0, note=0x40, velocity=0x40):
        self.window_push(note)

    def start_of_track(self, n_track=0):
        print 'Start - track #%s' % n_track
        self.window = [0,0,0]


    def end_of_track(self):
        print 'End of track'
        print ''


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
        print "Usage: %s <midi-file>"%sys.argv[0]
        sys.exit(-1)

    filename = sys.argv[1]
    f = open(filename, 'rb')
    
    # do parsing
    from midi.MidiInFile import MidiInFile
    midiIn = MidiInFile(NoteHandler(), f)
    midiIn.read()
    f.close()

