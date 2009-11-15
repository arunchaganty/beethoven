class Gene:
    def __init__(self):
        self.fitness = self.get_fitness()

    def __str__(self):
        return "Gene: fitness " + self.fitness

    def __repr__(self):
        return "<Gene>: fitness " + self.fitness

    def get_fitness(self):
        return 0

    def mate(self, other):
        return Gene()

    def mutate(self):
        return self

