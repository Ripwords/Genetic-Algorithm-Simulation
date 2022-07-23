import pygame as pg
import numpy as np
from time import sleep
from copy import copy, deepcopy
from Creatures import Creatures


class Simulation:
    # Initialize variables and simulation parameters
    def __init__(
        self, size=600, cells=30, dark=False, pop=100, mut=0.1, gen=100, lifespan=100
    ):
        pg.init()

        self.size = size
        self.cells = cells
        self.dark = 0 if dark else 255
        self.pop = pop
        self.mut = mut
        self.gen = gen
        self.currentGen = 0
        self.lifespan = lifespan
        self.currentLife = copy(self.lifespan)

        self.screen = pg.display.set_mode((self.size, self.size))
        self.cellSize = self.size // self.cells

        self.map = np.array([[0 for _ in range(self.cells)] for _ in range(self.cells)])
        self.creatures = []
        self.offsprings = []

    def spawnCreatures(self):
        """
        It creates a list of creatures, each with a random position and a random weights for the 4 directions.
        """
        for _ in range(self.pop):
            self.creatures.append(Creatures(self.cells))

    def drawGrid(self):
        """
        It draws a grid on the screen
        """
        self.screen.fill((self.dark, self.dark, self.dark))
        for i in range(0, self.size, self.cellSize):
            for j in range(0, self.size, self.cellSize):
                pg.draw.rect(
                    self.screen,
                    (255 - self.dark, 255 - self.dark, 255 - self.dark),
                    (i, j, self.cellSize, self.cellSize),
                    1,
                )

    def drawCreatures(self):
        """
        It draws a rectangle on the screen for each creature in the creatures list
        """
        for i in self.creatures:
            pg.draw.rect(
                self.screen,
                i.color,
                (
                    i.x * self.cellSize,
                    i.y * self.cellSize,
                    self.cellSize,
                    self.cellSize,
                ),
            )

    def updateCreaturePos(self, creature):
        """
        It draws a rectangle over the previous position of the creature to reset it,
        then draws a rectangle over the new position of the creature

        :param creature: The creature to be updated
        """
        creature.step()
        pg.draw.rect(
            self.screen,
            (self.dark, self.dark, self.dark),
            (
                creature.prevX * self.cellSize,
                creature.prevY * self.cellSize,
                self.cellSize,
                self.cellSize,
            ),
        )
        pg.draw.rect(
            self.screen,
            (255 - self.dark, 255 - self.dark, 255 - self.dark),
            (
                creature.prevX * self.cellSize,
                creature.prevY * self.cellSize,
                self.cellSize,
                self.cellSize,
            ),
            1,
        )
        self.drawCreatures()

    def summary(self):
        """
        It prints the current generation and the current life of the simulation
        """
        print("===================")
        print("Generation: ", self.currentGen)
        print("Number of creatures: ", len(self.creatures))
        print("Number of offsprings: ", len(self.offsprings))
        print("===================")

    def crossover(self):
        """
        It takes two creatures and crossover their weights
        """
        if len(self.creatures) % 2 != 0:
            self.creatures.pop()

        for i in range(0, len(self.creatures), 2):
            parent_1 = self.creatures[i]
            parent_2 = self.creatures[i + 1]
            child_1 = [parent_1.mvN, parent_1.mvE, parent_2.mvS, parent_2.mvW]
            child_2 = [parent_2.mvN, parent_2.mvE, parent_1.mvS, parent_1.mvW]
            self.offsprings.append(child_1 if np.random.rand() < 0.5 else child_2)

        self.drawGrid()
        self.summary()
        self.creatures = []
        for i in range(len(self.offsprings)):
            self.creatures.append(Creatures(self.cells))

    def mutate(self):
        """
        It mutates the weights of the creatures
        """
        for i, c in enumerate(self.creatures):
            c.mvN = self.offsprings[i][0]
            c.mvE = self.offsprings[i][1]
            c.mvS = self.offsprings[i][2]
            c.mvW = self.offsprings[i][3]
            mv = [c.mvN, c.mvE, c.mvS, c.mvW]
            for j in range(4):
                if np.random.rand() < self.mut:
                    mv[j] *= np.random.uniform(0, 1)
            c.setColor()

    def mate(self):
        # Selection
        creaturesCopy = deepcopy(self.creatures)
        for i, c in enumerate(creaturesCopy):
            if (c.x * self.cellSize > (self.size / 4)) and (
                c.y * self.cellSize > (self.size / 4)
            ):
                del creaturesCopy[i]
        self.creatures = creaturesCopy
        self.crossover()
        self.mutate()
        self.drawGrid()
        self.drawCreatures()

    def step(self):
        """
        For each creature in the list of creatures, update the creature's position
        """
        for i in self.creatures:
            self.updateCreaturePos(i)

    def stepGeneration(self):
        """
        If the current life is greater than 0, then step and update the display. If not, reset the
        current life to the lifespan
        """
        while True:
            if self.currentLife > 0:
                self.step()
                sleep(0.2)
                self.currentLife -= 1
                pg.display.update()
            else:
                self.currentLife = copy(self.lifespan)
                break

        self.mate()

    def run(self):
        self.drawGrid()
        self.drawCreatures()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pg.display.set_caption(
                        f"Genetic Algorithm - Generation {self.currentGen}"
                    )
                    for _ in range(self.gen):
                        self.currentGen += 1
                        pg.display.set_caption(
                            f"Genetic Algorithm - Generation {self.currentGen}"
                        )
                        self.stepGeneration()
                # elif event.type == pg.KEYDOWN:
                #     if event.key == pg.K_1:
                #         self.step()
                #     elif event.key == pg.K_2:
                #         self.mate()
                #         print(len(self.creatures))

            pg.display.flip()


if __name__ == "__main__":
    ai = Simulation(dark=True)
    ai.spawnCreatures()
    ai.run()
