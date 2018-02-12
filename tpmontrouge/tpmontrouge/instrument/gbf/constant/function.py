""" Define function for the generator output

Example : 

  from gbf import function

  print(function.Sinusoid)
  print(function._available)

"""

from ...utils.text_constant import TextConstant

class Function(TextConstant):
    pass

Sinusoid = Function('Sinusoid')
Square = Function('Square')
Ramp = Function('Ramp')
Noise = Function('Noise')
DC = Function('DC')
Triangle = Function('Triangle')

convert = Function.convert


del Function
