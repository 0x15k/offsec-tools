import subprocess
import platform
import ipaddress
import signal
import sys

def signal_handler(sig, frame):
    print('\nCtrl+C detected. Exiting...')
    sys.exit(0)

class HostDiscovery:
    def __init__(self, network=None):
        self.network = network
        signal.signal(signal.SIGINT, signal_handler)   
    
    @staticmethod
    def is_host_active(ip_address):
        if platform.system() == 'Windows':
            command = ['ping', '-n', '1', '-w', str(1 * 1000), ip_address]
        else:
            command = ['ping', '-c', '1', '-W', str(1), ip_address]

        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait(timeout=2)
        return process.returncode == 0

    def scan_hosts(self):
        if not self.network:
            raise ValueError("No se proporcionó la red")

        hosts = []
        net = ipaddress.ip_network(self.network, strict=False)
        for ip in net.hosts():
            ip_address = str(ip)
            if self.is_host_active(ip_address):
                hosts.append(ip_address)
                print(ip_address)
        print(f'Los siguientes hosts están activos en la red {self.network}:')
        for host in hosts:
            print(host)

    @classmethod
    def main(cls, network):
        host_scanner = cls(network)
        host_scanner.scan_hosts()

'''if __name__ == "__main__":
    HostDiscovery.main("192.168.1.0/24")'''
