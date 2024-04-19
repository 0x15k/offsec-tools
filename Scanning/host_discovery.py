import subprocess
import platform
import ipaddress
import signal
import sys

class HostDiscovery:
    @staticmethod
    def is_host_active(ip_address):
        if platform.system() == 'Windows':
            command = ['ping', '-n', '1', '-w', str(1 * 1000), ip_address]
        else:
            command = ['ping', '-c', '1', '-W', str(1), ip_address]

        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait(timeout=2)
        if process.returncode == 0:
            return True
        else:
            return False

    def __init__(self, network=None):
        self.network = network

    def discover_hosts(self):
        if not self.network:
            raise ValueError("Network is not provided")

        hosts = []
        net = ipaddress.ip_network(self.network, strict=False)
        for ip in net.hosts():
            ip_address = str(ip)
            if self.is_host_active(ip_address):
                hosts.append(ip_address)
                print(f'{ip_address}')  # Aquí se muestra la dirección IP directamente
        return hosts

    def scan_hosts(self):
        signal.signal(signal.SIGINT, self.exit_program)
        hosts = self.discover_hosts()
        print(f'The following hosts are active in the network {self.network}:')
        for host in hosts:
            print(host)

    def exit_program(self, sig, frame):
        print('\nCtrl+C detected. Exiting...')
        sys.exit(0)

    @classmethod
    def main(cls, network):
        host_scanner = cls(network)
        host_scanner.scan_hosts()
