__all__ = ["collection_generator","range_generator"]

from random import randrange

class Generator:

	def __init__(self, namein =""):
		self.name = namein
		self.default_gvars = dict()

	def sample(self):
		pass