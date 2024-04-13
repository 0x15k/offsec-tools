import ipaddress
from ping import Ping
import signal
import sys

def discover_hosts(network, mask):
    hosts = []
    net = ipaddress.ip_network(f'{network}/{mask}', strict=False)
    for ip in net.hosts():
        ip_address = str(ip)
        if Ping.is_host_active(ip_address):
            hosts.append(ip_address)
            print(ip_address)
    return hosts

def signal_handler(sig, frame):
    print('Ctrl+C detected. Exiting...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    network = input('Enter the network address (e.g. 192.168.1.0): ')
    mask = input('Enter the subnet mask (e.g. 255.255.255.0): ')
    try:
        hosts = discover_hosts(network, mask)
        print(f'The following hosts are active in the network {network}/{mask}:')
        for host in hosts:
            print(host)
    except KeyboardInterrupt:
        print('Ctrl+C detected. Exiting...')
        sys.exit(0)
