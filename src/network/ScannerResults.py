from utils.freezable import Freezable
from typing import Optional

class ScannerResults(Freezable): 
	def __init__(self): 
		super().__init__()
		self.__results = {}

	host: str = ''
	hostname: str = ''
	error: Optional[Exception|str] = None

	def __add__(self, result: tuple[int|Exception|bool]|list[int|Exception|bool]): 
		# Validate tuple/list shape
		if not (isinstance(result, (tuple, list)) and len(result) == 2):
			raise TypeError("A (port, status) pair can only be added.")

		port, status = result

		# Port must be an int (not bool) in valid port range
		if not (type(port) is int and 0 <= port <= 65535):
			raise ValueError("The first item must be a valid port number from 0 to 65535 (inclusive).")

		# Status must be a bool or an Exception instance
		elif not (type(status) is bool or isinstance(status, Exception)):
			raise TypeError("The second item must be a bool or an Exception instance.")

		# Update the results
		self.__results[port] = status
		return self
	
	def __sub__(self, port: int): 
		if not port in self.__results: 
			raise KeyError(f"Port {port} not found in results.")
		
		# Remove the port
		del self.__results[port]
		return self
	
	@property
	def open(self) -> list[int]: 
		"""
			The open ports

			Returns:
				list[int]: The list of open ports scanned
		"""
		return [port for port, status in self.__results.items() if (status == True)]
	
	@property
	def closed(self) -> dict[int, Exception]: 
		"""
			The closed ports

			Returns:
				dict[int, Exception]: A dictionary mapping the port to the closed state reason
		"""
		return dict([[entry for entry in self.__results.items() if isinstance(entry[1], Exception)]])

	@property
	def ports(self) -> list[int]: 
		"""
			The ports scanned

			Returns:
				list[int]: The list of port numbers scanned
		"""
		return self.__results.keys()