class Currency:
    def __init__(self, pizzarate, wasabirate, snowballrate, shellrate, total = None):
        self.pizzarate = pizzarate
        self.wasabirate = wasabirate
        self.snowballrate = snowballrate
        self.shellrate = shellrate
        self.total = total

class Pizza(Currency):
    def __init__(self, total):
        super.__init__(1, .48, 1.52, 0.71, total)
        self.type = "Pizza"

class Wasabi(Currency):
    def __init__(self, total):
        super.__init__(2.05, 1, 3.26, 1.56, total)
        self.type = "Wasabi"

class Snowball(Currency):
    def __init__(self, total):
        super.__init__(.54, .3, 1, .46, total)
        self.type = "Snowball"

class Shells(Currency):
    def __init__(self, total):
        super.__init__(1.41, 0.61, 2.08, 1, total)
        self.type = "Shells"

class Path:
    def __init__(self, path = []):
        self.path = path

    def printPath(self):
        pathnames = [currency.type for currency in self.path]
        print(",".join(pathnames))

    