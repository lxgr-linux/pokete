class DummyFigure:
	"""A dummy Figure to use in Pokete-Care
    ARGS:
        poke: The poke to contain"""

	def __init__(self, poke):
		self.pokes = [poke]
		self.caught_pokes = []
