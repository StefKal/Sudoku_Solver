from time import time

from solving.puzzles.sudoku import Sudoku
from solving.agents.anneal import SimulatedAnnealingAgent
puzzle = Sudoku()
agent = SimulatedAnnealingAgent()
start = time()
agent.solve(puzzle)
seconds = time() - start
print("after:", seconds, "seconds")