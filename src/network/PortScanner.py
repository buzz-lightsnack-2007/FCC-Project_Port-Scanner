# PortScanner.py
# A simple port scanner that checks for open ports on a given hostname.

# Imports
# Standard Library
from typing import Optional
import socket
import re

# Project modules
from network import errors
from network.ScannerResults import ScannerResults

class PortScanner: 
    hostname: str = None
    host: str = None
    ports: list[int]|tuple[int]|set[int]|range = None
    timeout: int|float = 2.5

    def __setattr__(self, attribute, value): 
        super().__setattr__(attribute, value)
        if attribute == 'ports':
            if isinstance(value, (list, tuple, range)): 
                self.ports = set(value) # convert to set for faster lookup
    
    def resolve(self) -> bool: 
        # Use Regex to determine if the hostname looks like an IPv4 address
        def _test_IPv4(hostname: str) -> bool:
            ipv4_pattern = re.compile(r"^\d+(\.\d+){3}$")
            return bool(ipv4_pattern.match(hostname))

        status: bool|Exception = True

        if self.hostname is not None: 
            if _test_IPv4(self.hostname): 
                # Move from hostname to host
                self.host = str(self.hostname)
                self.hostname = None
                return self.resolve()
            elif self.hostname: 
                # Try to resolve the hostname to an IP address
                try: 
                    self.host = socket.gethostbyname(self.hostname)
                except socket.gaierror as e: 
                    status = errors.Invalid_Hostname(domain=self.hostname, parent=e)
            else: 
                status = errors.Invalid_Hostname(domain=self.hostname)
        elif self.host is not None: 
            if self.host and _test_IPv4(self.host): 
                # Check if the host name is a valid IPv4 address
                try: 
                    socket.inet_aton(self.host)
                    self.hostname = socket.gethostbyaddr(self.host)[0]
                except (socket.error, Exception) as e:
                    status = errors.Invalid_IPAddress(address=self.host, parent=e)
            else: 
                status = errors.Invalid_IPAddress(address=self.host)

        if isinstance(status, Exception):
            raise status
        return status

    def __sub__(self, value: int|float): 
        if (self.timeout - value) <= 0: 
            raise ValueError("Timeout value must be greater than 0.")
        self.timeout -= value

        return self

    def __add__(self, value: int|float):
        if (self.timeout + value) <= 0: 
            raise ValueError("Timeout value must be greater than 0.")
        self.timeout += value
        return self

    def __prepare(self, *socket_args, **socket_kwargs) -> socket.socket:
        new: socket.socket = socket.socket(*(socket_args or [socket.AF_INET, socket.SOCK_STREAM]), **socket_kwargs)
        new.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try: 
            new.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except AttributeError:
            """SO_REUSEPORT may not be available on all systems"""
        new.settimeout(self.timeout)
        return new

    def scan(self, verbose: bool = False, *socket_args, **socket_kwargs) -> ScannerResults:
        results: ScannerResults = ScannerResults()

        def prefill() -> ScannerResults:
            nonlocal results
            results.hostname = self.hostname
            results.host = self.host
            
            return results

        def validate() -> bool:
            nonlocal results
            try: 
                self.resolve()
            except (errors.Invalid_IPAddress, errors.Invalid_Hostname) as e: 
                results.error = e
            return not bool(results.error)

        def scan(port): 
            nonlocal socket_args, socket_kwargs
            status: bool|Exception = True
            unexpected: Exception|None = None

            print(f"Scanning {self.host}:{port}\033[5m…\033[0m") if verbose else None

            with self.__prepare(*socket_args, **socket_kwargs) as sock:
                try: 
                    sock.connect((self.host, port))
                except (ConnectionRefusedError, TimeoutError, socket.timeout) as e: 
                    status = e
                except Exception as e:
                    unexpected = e
            
            if unexpected: 
                print(f"\033[F\033[K\033[1mScanning {self.host}:{port} \033[31mfailed\033[0m\n{str(unexpected)}") if verbose else None
                raise unexpected
            print(f"\033[F\033[KScanning {self.host}:{port} \033[32mcomplete\033[0m; got {status}") if verbose else None
            return [port, status]

        def finalize(): 
            nonlocal results
            results.lock()
            return results

        validate()
        prefill()

        if results.error: return finalize()

        for port in self.ports:
            scan_result = scan(port)
            results += scan_result
        
        return finalize()

