import random
import time
from pyage.core.operator import Operator
from pyage.TSP.route_genotype import Route, Point
from math import *

import logging

logger = logging.getLogger(__name__)


class DistanceEvaluator(Operator):
    def __init__(self, type=None):
        super(DistanceEvaluator, self).__init__(Route)

    def process(self, population):
        for genotype in population:
            genotype.fitness = self.evaluate(genotype)

    def evaluate(self, genotype):
        P = genotype.route
        dist = lambda p1, p2: Point(p2.x, p2.y, p1.d + sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2))
        return reduce(dist,P).d
