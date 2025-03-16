
import random
from HeraEngine import *

class Maze():
    def __init__(self,core:Core):
        self._core = core
        self.size = Vec2(89,89)
        self.seed = 1
        self.FREE,self.WALL,self.NORTH, self.SOUTH, self.EAST, self.WEST = True,False,'n', 's', 'e', 'w'
        random.seed(self.seed)
        self._core.log.INFO("Created MAZE.")

    def _debug_display_maze(self):
        for y in range(self.size.y):
            for x in range(self.size.x):
                    print("⬜" if self.maze[(x, y)] else "⬛", end='')
            print()

    def _setup_walls(self):
        for x in range(self.size.x):
            for y in range(self.size.y):
                self.maze[(x, y)] = self.WALL 

    def _visit(self,x,y):
        self.maze[(x, y)] = self.FREE

        while True:
                unvisitedNeighbors = []
                if y > 1 and (x, y - 2) not in self.hasVisited:
                    unvisitedNeighbors.append(self.NORTH)

                if y < self.size.y - 2 and (x, y + 2) not in self.hasVisited:
                    unvisitedNeighbors.append(self.SOUTH)

                if x > 1 and (x - 2, y) not in self.hasVisited:
                    unvisitedNeighbors.append(self.WEST)

                if x < self.size.x - 2 and (x + 2, y) not in self.hasVisited:
                    unvisitedNeighbors.append(self.EAST)

                if len(unvisitedNeighbors) == 0:
                    return
                else:
                    nextIntersection = random.choice(unvisitedNeighbors)
                    if nextIntersection == self.NORTH:
                        nextX = x
                        nextY = y - 2
                        self.maze[(x, y - 1)] = self.FREE
                    elif nextIntersection == self.SOUTH:
                        nextX = x
                        nextY = y + 2
                        self.maze[(x, y + 1)] = self.FREE 
                    elif nextIntersection == self.WEST:
                        nextX = x - 2
                        nextY = y
                        self.maze[(x - 1, y)] = self.FREE 
                    elif nextIntersection == self.EAST:
                        nextX = x + 2
                        nextY = y
                        self.maze[(x + 1, y)] = self.FREE 

                    self.hasVisited.append((nextX, nextY)) 
                    self._visit(nextX, nextY)

    def _setup_maze(self):
        self.maze = {}
        self.hasVisited = [(1, 1)]
        self._setup_walls()
        self._visit(1,1)
        self._core.log.DEBUG("Finished maze generation.")


    def setup(self):
        self._core.update = self.update
        self._setup_maze()
        self._debug_display_maze()
        self._core.log.INFO("Launched MAZE.")

    def update(self,_):
        pass





