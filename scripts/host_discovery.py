import subprocess
import platform
import time
import ipaddress

def is_host_active(ip_address):
    if platform.system() == 'Windows':
        command = ['ping', '-n', '1', '-w', str(1 * 1000), ip_address]
    else:
        command = ['ping', '-c', '1', '-W', str(1), ip_address, '&']

    try:
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait(timeout=1)
        if process.returncode == 0:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False
    except:
        return False

def discover_hosts(network, mask):
    hosts = []
    net = ipaddress.ip_network(f'{network}/{mask}', strict=False)
    for ip in net.hosts():
        ip_address = str(ip)
        if is_host_active(ip_address):
            hosts.append(ip_address)
            print(ip_address)
    return hosts

if __name__ == '__main__':
    network = input('Enter the network address (e.g. 192.168.1): ')
    mask = input('Enter the subnet mask (e.g. 255.255.255.0): ')
    hosts = discover_hosts(network, mask)
    print(f'The following hosts are active in the network {network}/{mask}:')
    for host in hosts:
        print(host)