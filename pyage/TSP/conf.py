# coding=utf-8
import logging
import os
import math

from pyage.TSP.naming_service import NamingService
from pyage.TSP.route_crossover import RouteCrossover
from pyage.TSP.route_eval import DistanceEvaluator
from pyage.TSP.route_init import RouteNormalInitializer, RouteClusterInitializer, root_agents_factory, RouteEmasInitializer
from pyage.TSP.route_mutation import RouteArbitraryMutation, RouteConsecutiveMutation
from pyage.core import address

from pyage.core.agent.aggregate import AggregateAgent
from pyage.core.emas import EmasService
from pyage.core.locator import GridLocator
from pyage.core.migration import ParentMigration
from pyage.core.stats.gnuplot import GraphStatistics
from pyage.core.stop_condition import StepLimitStopCondition


logger = logging.getLogger(__name__)

number_of_points = 30
start_x = 20
end_x = 50
start_y = 20
end_y = 50
clusters_nr = 2
points_in_cluster = 10

cluster_distance_min = 100
cluster_distance_max = 120

points = RouteClusterInitializer(clusters_nr, points_in_cluster,start_x,end_x,start_y, end_y, cluster_distance_min,cluster_distance_max)()
#points = RouteNormalInitializer(number_of_points,start_x,end_x,start_x,end_y)()
# clusters_nr, points_in_cluster, start_x, end_x, start_y, end_y, min_dist, max_dist):
logger.info("Initial route:\n%s", "\n".join(map(str,points)))

points_nr = len(points)

agents_count = 1
agg_size = 50
logger.debug("EMAS, %s agents", agents_count)
agents = root_agents_factory(agents_count, AggregateAgent)
aggregated_agents = RouteEmasInitializer(points, size=agg_size, energy=40 )

stop_condition = lambda: StepLimitStopCondition(1000)


minimal_energy = lambda: 10
reproduction_minimum = lambda: 75
migration_minimum = lambda: 120
newborn_energy = lambda: 100
transferred_energy = lambda: 40

evaluation = lambda: DistanceEvaluator()
crossover = lambda: RouteCrossover(size=30)
mutation = lambda: RouteConsecutiveMutation(probability=0.1, evol_probability=0.5)

address_provider = address.SequenceAddressProvider
emas = EmasService

migration = ParentMigration
locator = GridLocator

stats = lambda: GraphStatistics('fitness_%s_pyage.txt' % __name__)

naming_service = lambda: NamingService(starting_number=2)
