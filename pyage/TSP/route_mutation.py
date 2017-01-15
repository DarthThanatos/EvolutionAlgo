import logging
from random import *

from pyage.TSP.route_genotype import Route
from pyage.core.operator import Operator

logger = logging.getLogger(__name__)


class AbstractMutation(Operator):
    def __init__(self, type, probability):
        super(AbstractMutation, self).__init__()
        self.probability = probability

    def process(self, population):
        for genotype in population:
            if random.random() < self.probability:
                self.mutate(genotype)


class RouteArbitraryMutation(AbstractMutation):
    def __init__(self, probability, evol_probability):
        super(RouteArbitraryMutation, self).__init__(Route, evol_probability)
        self.probability = probability

    def mutate(self, genotype):
        logger.debug("Mutating genotype: {0}".format(genotype))
        P = genotype.route
        points_to_swap = sample(P,2)
        #swapping arbitrary points in route
        i,j = P.index(points_to_swap[0]), P.index(points_to_swap[1])
        P[i], P[j] = P[j], P[i]

class RouteConsecutiveMutation(AbstractMutation):
    def __init__(self, probability, evol_probability):
        super(RouteConsecutiveMutation, self).__init__(Route, evol_probability)
        self.probability = probability

    def mutate(self, genotype):
        logger.debug("Mutating genotype: {0}".format(genotype))
        P = genotype.route
        points_to_swap = []
        points_to_swap.append(choice(P))
        points_to_swap.append((P[P.index(points_to_swap)+1] if P.index(points_to_swap)+1 < len(P) else P[P.index(points_to_swap)-1]))
        #swapping consecutive points in route
        i,j = P.index(points_to_swap[0]), P.index(points_to_swap[1])
        P[i], P[j] = P[j], P[i]
