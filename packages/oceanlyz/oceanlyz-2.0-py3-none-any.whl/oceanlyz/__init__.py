"""
.. ++++++++++++++++++++++++++++++++YA LATIF++++++++++++++++++++++++++++++++++
.. +                                                                        +
.. + ScientiMate                                                            +
.. + Earth-Science Data Analysis Library                                    +
.. +                                                                        +
.. + Developed by: Arash Karimpour                                          +
.. + Contact     : www.arashkarimpour.com                                   +
.. + Developed/Updated (yyyy-mm-dd): 2020-08-01                             +
.. +                                                                        +
.. ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""

#----------------------------------------------------------

#Package Information
#-------------------
__version__ = "2.0"
__author__ = 'Arash Karimpour'
#__credits__ = 'xyz Laboratory'    

#----------------------------------------------------------
#Import subdirectory modules
#It uses for module base import such as:
#import oceanlyz as sm
#from scientimate import plotting
#sm.plotting.plot2d(x,y,'line_confid','blue_red','large')
#----------------------------------------------------------
# from . import colormap
from . import oceanlyz


#----------------------------------------------------------
#Import all modules
#It uses for direct use of functions such as:
#import scientimate as sm
#sm.plot2d(x,y,'line_confid','blue_red','large')
#----------------------------------------------------------

#OCEANLYZ
#--------
from .oceanlyz.oceanlyz import oceanlyz
from .oceanlyz.PcorFFTFun import PcorFFTFun
from .oceanlyz.PcorZerocrossingFun import PcorZerocrossingFun
from .oceanlyz.SeaSwellFun import SeaSwellFun
from .oceanlyz.WaveSpectraFun import WaveSpectraFun
from .oceanlyz.WaveZerocrossingFun import WaveZerocrossingFun
