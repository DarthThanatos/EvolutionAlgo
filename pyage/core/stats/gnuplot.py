import logging
import time
from pyage.core.statistics import Statistics
import os
import matplotlib.pyplot as plt
logger = logging.getLogger(__name__)


class StepStatistics(Statistics):
    def __init__(self, output_file_name='fitness_pyage.txt'):
        self.output_file_name = output_file_name
        self.times = []
        self.history = []
        self.fitness_output = open(output_file_name, 'a')

    def __del__(self):
        self.fitness_output.close()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(step_count - 1) + ';' + str(best_fitness) + '\n')
        self.fitness_output.flush()
        os.fsync(self.fitness_output)

    def update(self, step_count, agents):
        try:
            best_fitness = max([a.get_fitness() for a in agents])
            #print  max(agents, key=lambda a: a.get_fitness()).get_best_genotype()
            logger.debug(best_fitness)
            self.history.append(best_fitness)
            self.times.append(step_count)
            if (step_count - 1) % 100 == 0:
                self.append(best_fitness, step_count)
                print step_count,";", best_fitness
        except Exception as e:
            print e
            logging.exception("")

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            best_agent = max(agents, key=lambda a: a.get_fitness())
            best_genotype = best_agent.get_best_genotype()
            plt.plot(self.times, self.history)
            plt.savefig(self.output_file_name.replace("txt","png"))
            self.fitness_output.write("best genotype:\n%s" % best_genotype)
        except Exception as e:
            print e
            logging.exception(e)

class GraphStatistics(StepStatistics):
    def __init__(self,output_file_name='fitness_pyage.txt'):
        super(GraphStatistics,self).__init__(output_file_name)

    def summarize(self, agents):
        try:
            logger.debug(self.history)
            best_agent = max(agents, key=lambda a: a.get_fitness())
            best_genotype = best_agent.get_best_genotype()
            plt.plot(self.times, self.history)
            plt.savefig(self.output_file_name.replace("txt","png"))
            self.fitness_output.write("best genotype:\n%s" % best_genotype.toString())
            best_route = best_agent.get_best_genotype().route
            plt.clf()
            plt.plot([p.x for p in best_route], [p.y for p in best_route], 'ro')  # drawing vertices
            for i in range(len(best_route)): # drawing edges
                print(best_route[i].toString())
                plt.plot([best_route[i].x, best_route[(i + 1)  % len(best_route)].x], [best_route[i].y, best_route[(i + 1)  % len(best_route)].y], lw=1, c="b")
            plt.savefig(self.output_file_name.replace(".txt","_paths.png"))
            print best_route.__len__()
        except Exception as e:
            print e
            logging.exception(e)


class TimeStatistics(StepStatistics):
    def __init__(self, output_file_name='fitness_pyage.txt'):
        super(TimeStatistics, self).__init__(output_file_name)
        self.start = time.time()

    def append(self, best_fitness, step_count):
        self.fitness_output.write(str(time.time() - self.start) + ';' + str(best_fitness) + '\n')
