from random import *

from pyage.TSP.route_genotype import Point, Route
from pyage.core.emas import EmasAgent
from pyage.core.operator import Operator
from pyage.elect.el_genotype import Votes
from pyage.core.inject import Inject
import random


class RouteEmasInitializer(object):
    def __init__(self, route, energy, size):
        self.route = route
        self.energy = energy
        self.size = size

    @Inject("naming_service")
    def __call__(self):
        agents = {}
        for i in range(self.size):
            agent = EmasAgent(Route(self.route), self.energy, self.naming_service.get_next_agent())
            agents[agent.get_address()] = agent
        return agents


def root_agents_factory(count, type):
    def factory():
        agents = {}
        for i in range(count):
            agent = type('R' + str(i))
            agents[agent.get_address()] = agent
        return agents

    return factory


class RouteNormalInitializer(object):
    def __init__(self, points_nr, start_x, end_x, start_y, end_y):
        self.points_nr = points_nr
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y

    def __call__(self):
        P = [Point(randint(self.start_x, self.end_x), randint(self.start_y, self.end_y), 0)
             for _ in range(self.points_nr)]
        return P


class RouteClusterInitializer(object):
    def __init__(self, clusters_nr, points_in_cluster, start_x, end_x, start_y, end_y, min_dist, max_dist):
        self.clusters_nr = clusters_nr
        self.points_in_cluter = points_in_cluster
        self.start_x = start_x
        self.end_x = end_x
        self.start_y = start_y
        self.end_y = end_y
        self.min_dist = min_dist
        self.max_dist = max_dist

    def __call__(self):
        X = self.generate_cluster_coord(self.start_x)
        Y = self.generate_cluster_coord(self.start_y)
        shuffle(X)
        shuffle(Y)
        clusters = [Point(x,y,0) for (x,y) in zip(X, Y)] # centers of the cluster, we put more verticies around those centers below
        surrounding_points = []
        for cluster in clusters:
            for i in range(self.points_in_cluter):
                #  each cluster consists of N + 1 nodes
                #  the first "central" node in a cluster is selected in the code above, the rest N nodes surrounds it
                x = randrange(int(cluster.x - self.min_dist / 4.0), int(cluster.x + self.min_dist / 4.0))
                y = randrange(int(cluster.y - self.min_dist / 4.0), int(cluster.y + self.min_dist / 4.0))
                surrounding_points.append(Point(x, y, 0))
        print (clusters + surrounding_points).__len__()
        return clusters + surrounding_points  # 9 sets of (N + 1)-element-clusters


    def generate_cluster_coord(self, starting_margin):
        clusters_coords = [randrange(starting_margin)]
        for i in range(1, self.clusters_nr):
            #  first cluster already is in place so we start with 1, not 0
            clusters_coords.append(clusters_coords[-1] + randrange(self.min_dist,self.max_dist))
            #  we move those clusters by more or less fixed amount of units
        return clusters_coords