from Gene import Gene
from mingus.containers import *
from mingus.midi import fluidsynth

class MusicGene(Gene):
    def __init__(self, track):
        self.track = track
    def __str__(self):
        return "MusicGene: " + str(track) + "fitness " + self.fitness
    def __repr__(self):
        return "<MusicGene>: " + str(track) + "fitness " + self.fitness

    def get_fitness(self):
        return 0

    def mate(self, other):
        return MusicGene(self.track)

    def mutate(self):
        return self

    def play(self):
        fluidsynth.play_Track(self.track)


