from math import log

class LogCalculator():

  def __init__(self):
    self.stored = {}

  def log(self, x):
    if x not in self.stored:
      self.stored[x] = log(x)

    return self.stored[x]
