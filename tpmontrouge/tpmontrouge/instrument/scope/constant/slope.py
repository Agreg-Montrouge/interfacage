""" Define constants for the slope of trigger

Example : 

  from scope import slope

  print(slope.PositiveEdge)

"""
from ...utils.text_constant import TextConstant

class Slope(TextConstant):
    pass

PositiveEdge = Slope('PositiveEdge')
NegativeEdge = Slope('NegativeEdge')

convert = Slope.convert


del Slope
