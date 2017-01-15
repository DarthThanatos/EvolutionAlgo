import random

from pyage.TSP.route_genotype import Route
from pyage.core.operator import Operator

import logging

logger = logging.getLogger(__name__)
class AbstractCrossover(Operator):
    def __init__(self, type, size):
        super(AbstractCrossover, self).__init__(type)
        self.__size = size

    def process(self, population):
        parents = list(population)
        for i in range(len(population), self.__size):
            p1, p2 = random.sample(parents, 2)
            genotype = self.cross(p1, p2)
            population.append(genotype)

class RouteCrossover(AbstractCrossover):
    def __init__(self, size):
        super(RouteCrossover, self).__init__(Route, size)

    def cross(self, p1, p2):
        logger.debug("Crossing:\n{0}\nAND\n{1}".format(p1, p2))
        division = random.randint(1, len(p1.route)-2)
        new_route = p1.route[:division] + p2.route[division:]
        return Route(new_route)
