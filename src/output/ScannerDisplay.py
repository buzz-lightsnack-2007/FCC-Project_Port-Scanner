# Import modules
# FCC modules
from common_ports import ports_and_services

# Local modules
from network.ScannerResults import ScannerResults
from utils.cls import class_utils

class ScannerDisplay: 
	def __init__(self, results: ScannerResults): 
		self.results: ScannerResults = results
	
	def __str__(self, placeholder: str = 'unknown'): 
		def results_display(): 
			return '\n'.join((
				f"Open ports for {self.results.hostname} ({self.results.host})",
				"PORT\tSERVICE", 
				*['\t'.join([str(port), ports_and_services[port] if port in ports_and_services else placeholder]) for port in self.results.open]
			))
		
		def error_display(): 
			return f"Error: {self.results.error}"

		return [results_display, error_display][bool(self.results.error)]()
	
	def display(self):
		print(self.__str__())
		return self.__str__()
	
	@class_utils.validation
	def __setattr__(self):
		return {
			"type": ScannerDisplay,
			"pre": {
				"results": lambda value, *args: isinstance(value, ScannerResults)
			}
		}
	
