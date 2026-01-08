# Import modules
# FCC modules
from common_ports import ports_and_services

# Local modules
from network.ScannerResults import ScannerResults

class ScannerDisplay: 
	results: ScannerResults
	
	def __str__(self, placeholder: str = 'unknown'): 
		result = lambda: '\n'.join((
				f"Open ports for {self.results.hostname} ({self.results.host})",
				'\t'.join(['PORT', 'SERVICE']), 
				*['\t'.join([str(port), ports_and_services[port] if port in ports_and_services else placeholder]) for port in self.results.open]
			))
		error = lambda: f"Error: {str(self.results.error)}"
		
		return [result, error][bool(self.results.error)]()
	
	def display(self):
		print(self.__str__())
		return self.__str__()
