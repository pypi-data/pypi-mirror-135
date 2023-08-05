
"""
.. include:: ../../docs/intro.md
"""

__version__ = '1.0.5'

# Need to enforce the correct dependency ordering, with the rail class coming
# first. This avoid circular references when the code linter starts rearranging
# things.

from .rail import Ball  # noqa isort: skip
from .rail import Rail  # noqa isort: skip
from .clocks import Clock  # noqa
from .clocks import FastClock  # noqa
from .tools import clear  # noqa
from .tools import runSimulation  # noqa

__pdoc__ = {}
__pdoc__['clocks.Clock.__str__'] = True
__pdoc__['rail.Rail.__eq__'] = True
