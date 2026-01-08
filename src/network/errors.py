# errors.py
# Custom exceptions for network-related errors.

# Imports
# Standard Library
import socket

class Invalid_IPAddress(socket.error): 
    """
        Raised when an invalid IP address is provided.
    """
    address: str # the invalid address
    args: list[str]
    parent: Exception|None

    def __init__(self, address: str = None, parent: Exception = None): 
        super().__init__()
        self.args = ["Invalid IP address"]
        self.address = address
        self.parent = parent

class Invalid_Hostname(socket.error): 
    """
        Raised when an invalid hostname is provided.
    """
    domain: str # the invalid domain
    args: list[str]

    def __init__(self, domain: str = None, parent: Exception = None): 
        super().__init__()
        self.args = ["Invalid hostname"]
        self.domain = domain
        self.parent = parent