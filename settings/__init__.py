from sys import argv

try:
    from .base import *
except:
    from settings_no_password import  *
try:
    from .local import *
except ImportError:
    pass

if 'nosetests' in argv[0]:
    from .test import *