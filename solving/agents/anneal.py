# Author: Stefanos Kalamaras
# Citations: Dylan Dechiara

from solving.utils.framework import Agent
import random, math

class SimulatedAnnealingAgent(Agent):
    def __init__(self):
        self.start = 11.0
        self.stop = 0.01
        self.decay = 0.99
        self.temp = 1.0

    def move(self, puzzle):

        while self.temp >= self.stop:

            move = random.choice(puzzle.moves())

            neighbor = puzzle.neighbor(move)

            prob_val = random.uniform(0, 1)

            if neighbor.solved():
                return move

            if neighbor.heuristic() < puzzle.heuristic() or prob_val < math.exp((puzzle.heuristic()
                                                                - neighbor.heuristic()) / self.temp):

                self.temp *= self.decay
                return move

        print("Failed :(")
        quit()





