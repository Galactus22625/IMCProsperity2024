from copy import deepcopy
class Currency:
    def __init__(self, pizzarate, wasabirate, snowballrate, shellrate, total = None):
        self.pizzarate = pizzarate
        self.wasabirate = wasabirate
        self.snowballrate = snowballrate
        self.shellrate = shellrate
        self.total = total

class Pizza(Currency):
    def __init__(self, total):
        super().__init__(1, .48, 1.52, 0.71, total)
        self.type = "Pizza"

class Wasabi(Currency):
    def __init__(self, total):
        super().__init__(2.05, 1, 3.26, 1.56, total)
        self.type = "Wasabi"

class Snowball(Currency):
    def __init__(self, total):
        super().__init__(.54, .3, 1, .46, total)
        self.type = "Snowball"

class Shells(Currency):
    def __init__(self, total):
        super().__init__(1.41, 0.61, 2.08, 1, total)
        self.type = "Shells"

class Path:
    def __init__(self, path = []):
        self.path = path

    def pathString(self):
        pathnames = [currency.type for currency in self.path]
        return(", ".join(pathnames))
    
    def evaluatePath(self):
        if self.path[-1].type == "Shells":
            return self.path[-1].total
        else:
            return 0

    def nextStep(self):
        if len(self.path) == 6:
            return []
        newpaths = []
        currenttype = self.path[-1].type

        if currenttype != "Pizza":
            pizzapath = deepcopy(self.path)
            pizzapath.append(Pizza(pizzapath[-1].total * pizzapath[-1].pizzarate))
            newpaths.append(Path(pizzapath))

        if currenttype != "Wasabi":
            wasabipath = deepcopy(self.path)
            wasabipath.append(Wasabi(wasabipath[-1].total * wasabipath[-1].wasabirate))
            newpaths.append(Path(wasabipath))

        if currenttype != "Snowball":
            snowballpath = deepcopy(self.path)
            snowballpath.append(Snowball(snowballpath[-1].total * snowballpath[-1].snowballrate))
            newpaths.append(Path(snowballpath))

        if currenttype != "Shells":
            shellpath = deepcopy(self.path)
            shellpath.append(Shells(shellpath[-1].total * shellpath[-1].shellrate))
            newpaths.append(Path(shellpath))
        
        return newpaths
    
DFS = [Path([Shells(1)])]
bestpath = None
bestprofit = 1
while DFS:
    currentpath = DFS.pop()
    if currentpath.evaluatePath() != 0:
        print(currentpath.pathString())
        print(currentpath.evaluatePath())
    if currentpath.evaluatePath() > bestprofit:
        bestprofit = currentpath.evaluatePath()
        bestpath = currentpath.pathString()
    DFS = DFS + currentpath.nextStep()
print("The Best path is:")
print(bestpath)
print(bestprofit)