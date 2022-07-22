import pygame as pg
import numpy as np
from time import sleep
from copy import copy
from Creatures import Creatures


class Simulation:
    # Initialize variables and simulation parameters
    def __init__(
        self, size=600, cells=30, dark=False, pop=100, mut=0.01, gen=100, lifespan=200
    ):
        pg.init()
        pg.display.set_caption("Genetic Algorithm")

        self.size = size
        self.cells = cells
        self.dark = 0 if dark else 255
        self.pop = pop
        self.mut = mut
        self.gen = gen
        self.lifespan = lifespan
        self.currentLife = copy(self.lifespan)

        self.screen = pg.display.set_mode((self.size, self.size))
        self.screen.fill((self.dark, self.dark, self.dark))
        self.cellSize = self.size // self.cells

        self.map = np.array([[0 for _ in range(self.cells)] for _ in range(self.cells)])
        self.creatures = []

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
        if self.currentLife > 0:
            self.step()
            sleep(0.2)
            self.currentLife -= 1
            pg.display.update()
        else:
            self.currentLife = copy(self.lifespan)

    def run(self):
        self.drawGrid()
        self.drawCreatures()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

            pg.display.flip()


if __name__ == "__main__":
    ai = Simulation(dark=True)
    ai.spawnCreatures()
    ai.run()
