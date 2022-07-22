import numpy as np
from copy import copy


class Creatures:
    def __init__(self, Lim):
        self.Lim = Lim
        self.x = np.random.randint(0, self.Lim)
        self.y = np.random.randint(0, self.Lim)
        self.prevX = None
        self.prevY = None
        self.weights = np.random.rand(4)
        self.mvN = self.weights[0]
        self.mvE = self.weights[1]
        self.mvS = self.weights[2]
        self.mvW = self.weights[3]
        self.color = 0
        for i in range(4):
            np.random.seed(np.int(self.weights[i] * 10000000))
            self.color += np.random.rand()
        np.random.seed(np.int(self.color * 10000000))
        self.color = (
            np.random.randint(10, 255),
            np.random.randint(10, 255),
            np.random.randint(10, 255),
        )

    def step(self):
        moves = ["N", "E", "S", "W"]
        weights = list(self.weights.copy().flatten())
        if self.x == self.Lim - 1:
            moves.remove("E")
            del weights[1]
        elif self.x == 0:
            moves.remove("W")
            del weights[-1]
        if self.y == self.Lim - 1:
            moves.remove("S")
            del weights[2]
        elif self.y == 0:
            moves.remove("N")
            del weights[0]
        move = np.random.choice(moves)
        self.prevX = copy(self.x)
        self.prevY = copy(self.y)
        if move == "N":
            self.y -= 1
        elif move == "E":
            self.x += 1
        elif move == "S":
            self.y += 1
        elif move == "W":
            self.x -= 1
        return (self.x, self.y)


if __name__ == "__main__":
    creatures = []
    prevMove = []
    for i in range(10):
        creature = Creatures(20)
        creatures.append(creature)
        prevMove.append(creature.step())
        print(creature.color)
        print(creature.x, creature.y)
        print("====================")
    for index, i in enumerate(creatures):
        i.step()
        print(prevMove[index])
        print((i.x, i.y))
        print("==============")
