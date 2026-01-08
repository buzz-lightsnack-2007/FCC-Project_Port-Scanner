# port_scanner.py
# A simple script to scan for open ports on a given target.

# Imports
# Standard Library
import socket

# Project modules
from network.PortScanner import PortScanner
from output.ScannerDisplay import ScannerDisplay

def get_open_ports(target, port_range, verbose = False):
    open_ports = []

    scanner = PortScanner()
    scanner.hostname, scanner.ports, scanner.timeout = target, range(port_range[0], port_range[1]+1), 0.5
    display = ScannerDisplay()
    display.results = scanner.scan()

    if verbose: 
        return display.display()
    
    if display.results.error: 
        return str(display)
    return display.results.open
    # return(open_ports)
