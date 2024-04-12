import subprocess
import platform
import time

def is_host_active(ip_address):
    if platform.system() == 'Windows':
        command = ['ping', '-n', '1', '-w', str(1 * 1000), ip_address]
    else:
        command = ['ping', '-c', '1', '-W', str(1), ip_address]

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

if __name__ == '__main__':
    ip_address = input('Enter the IP address: ')
    if is_host_active(ip_address):
        print(f'{ip_address} is active.')
    else:
        print(f'{ip_address} is not active.')