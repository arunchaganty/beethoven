from Gene import Gene
from mingus.containers import *
from mingus.midi import fluidsynth

class MusicGene(Gene):
    def __init__(self, track):
        Gene.__init__(self)
        self.track = track

    def __str__(self):
        str_ = "MusicGene: " + "fitness " + str(self.fitness) + '\n' 
        str_ += self.print_track(self.track)
        return str_

    def __repr__(self):
        return str(self)

    def print_track(self, track):
        str_ = ""
        for bar in track:
            for note in bar.get_note_names():
                str_ += note + " "
        return str_

    def get_fitness(self):
        return 0.1

    def mate(self, other):
        # Most naive method - interleave bars
        assert(len(self.track) == len(other.track))
        children = []

        track = Track()
        for i in xrange(len(self.track)):
            if i%2 == 0:
                track.add_bar(self.track[i])
            else:
                track.add_bar(other.track[i])

        print "Mating:"
        print "P1: " + self.print_track(self.track)
        print "P2: " + self.print_track(other.track)
        print "C1: " + self.print_track(track)

        children.append(MusicGene(track))

        return children


    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(self.track)

