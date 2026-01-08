class Freezable:
	_locked: bool = False
	
	def lock(self):
		"""
			Lock the class’ attributes. 

			Returns:
				bool: Class successfully locked?
		"""
		self._locked = True
		return (self._locked == True)
	
	def __setattr__(self, name, value):
		if self._locked:
			raise AttributeError(f"Instance {repr(self)} is locked, so attributes can’t be modified.")
		super().__setattr__(name, value)
