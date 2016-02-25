from .base import *
try:
	from .local import *
except ImportError:
	print("Can`t find module settings.local, you can create it from local.py.skeleton")

