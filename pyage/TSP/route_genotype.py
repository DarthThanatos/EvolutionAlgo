class Point:
    def __init__(self, x, y, d=0):
        self.x = x
        self.y = y
        self.d = d

    def toString(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ", " + str(self.d) + ")"

class Route(object):
    def __init__(self, route):
        self.route = route
        self.fitness = None

    def toString(self):
        res = ""
        for p in self.route: res += p.toString() + "\n"
        return res

    def __str__(self):
        return "{0}\nfitness: {1}".format("\n".join(map(str, self.route)), self.fitness)

