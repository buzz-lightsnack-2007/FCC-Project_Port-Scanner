class class_utils: 
	def validation(set_attr):
		"""
			Validate the attributes as they are being updated. All you need to insert are some validation checks to be returned by your setattr function — abstracting the logic.
			
			**WARNING:** `attribute_validator` can only be run as a decorator of a class' `__setattr__`.

			Args:
				set_attr (function): the __setattr__ function goes here. It must return a dictionary containing the class type (required) and the pre and post- checks.
			
			Return:
				function: the validation logic
		"""
		def export(self, name: str, value): 
			flags = set_attr(self)
			
			# Validate
			state = True
			if 'pre' in flags.keys() and flags['pre'] and name in flags['pre'].keys(): state = bool(flags['pre'][name](value))
			
			# If okay, add to the attributes
			if state: 
				super(flags['type'], self).__setattr__(name, value) # get the required super() class. 
				
				# Post-validation
				if 'post' in flags.keys() and flags['post'] and name in flags['post'].keys(): state = bool(flags['post'][name](value))
			
			return state
		
		return export

	def fallback(get_attr): 
		"""
			Provide a fallback value for any unknown attribute. The value may either be static or may be an attribute of another class. 

			Args:
				get_attr (function): Fill this up by using a decorator on a `__getattr__`. It must return a dictionary containing the class type (required) and the subsitute value. 
			
			Returns:
				function: the fallback logic 
		"""
		def export(self, name: str): 
			order = get_attr(self) # run the original function to get the attributes
			
			if hasattr(self, name): 
				return super(order['type'], self).__getattr__(name) # get the attribute
			
			if isinstance(order['order'], tuple): 
				for fallback in order['order']: 
					if hasattr(fallback, name): 
						return getattr(fallback, name)
				raise AttributeError(f"The attribute “{name}” wasn’t found in {', '.join([repr(fallback) for fallback in order['order']])}.")
			
			return order['order'] # The order isn't a tuple

		return export		


			
