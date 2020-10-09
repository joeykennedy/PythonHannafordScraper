import matplotlib.pyplot as pyplot
import numpy as numpy

x = numpy.linspace(0, 20, 100)
pyplot.plot(x, numpy.sin(x))
pyplot.show()