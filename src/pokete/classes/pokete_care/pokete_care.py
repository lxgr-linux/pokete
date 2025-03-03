"""The Pokete care is a place a Pokete can be brought to, to let it gain xp
without the player using it"""

from ..poke import Poke


class PoketeCare:
	"""The Pokete care is a place a Pokete can be brought to, to let it gain xp
    without the player using its
    ARGS:
        entry: The in-game timestamp the poke was given in at
        poke: The Pokete that's in care"""

	def __init__(self, entry=0, poke=None):
		self.entry = entry
		self.poke = poke

	def from_dict(self, _dict):
		"""Assembles a PoketeCare from _dict"""
		self.entry = _dict.get("entry", 0)
		self.poke = None if _dict.get("poke") is None else \
			Poke.from_dict(_dict["poke"])

	def dict(self):
		"""Returns a dict from the object"""
		return {
			"entry": self.entry,
			"poke": None if self.poke is None else self.poke.dict(),
		}


pokete_care = PoketeCare()
