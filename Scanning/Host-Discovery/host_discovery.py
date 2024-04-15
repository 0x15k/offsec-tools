import ipaddress
from ping import Ping
import signal
import sys

class HostDiscovery:
    def __init__(self, network=None):  # Modificado para aceptar network como argumento opcional
        self.ping = Ping()
        self.network = network  # Guardar el network en la instancia

    def discover_hosts(self):  # Eliminado el parámetro network_with_mask
        if not self.network:
            raise ValueError("Network is not provided")
        
        hosts = []
        net = ipaddress.ip_network(self.network, strict=False)
        for ip in net.hosts():
            ip_address = str(ip)
            if self.ping.is_host_active(ip_address):
                hosts.append(ip_address)
                print(ip_address)
        return hosts

    def scan_hosts(self):  # Eliminado el parámetro network_with_mask
        signal.signal(signal.SIGINT, self.signal_handler)
        
        try:
            hosts = self.discover_hosts()  # Llamada sin argumentos
            print(f'The following hosts are active in the network {self.network}:')  # Usar self.network
            for host in hosts:
                print(host)
        except KeyboardInterrupt:
            print('Ctrl+C detected. Exiting...')
            sys.exit(0)

    def signal_handler(self, sig, frame):
        print('Ctrl+C detected. Exiting...')
        sys.exit(0)
        
    @classmethod
    def main(cls, network):
        host_scanner = cls(network)
        host_scanner.scan_hosts()  # Llamada al método scan_hosts en lugar de discover_hosts

