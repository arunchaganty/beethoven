from Gene import Gene
from mingus.containers import *
from mingus.midi import fluidsynth

class MusicGene(Gene):
    def __init__(self, track):
        Gene.__init__(self)
        self.track = track

    def __str__(self):
        str_ = "MusicGene: " + "fitness " + str(self.fitness) + '\n' 
        for bar in self.track:
            for note in bar.get_note_names():
                str_ += note + " "
        return str_

    def __repr__(self):
        return str(self)

    def get_fitness(self):
        return 0

    def mate(self, other):
        return MusicGene(self.track)

    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(self.track)


