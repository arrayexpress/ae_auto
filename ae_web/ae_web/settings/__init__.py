__author__ = 'Ahmed G. Ali'
from sys import argv

try:
    from .base import *
except:
    from base_no_passwords import *

try:
    from .local import *
except ImportError:
    pass

if 'test' in argv:
    from .test import *
