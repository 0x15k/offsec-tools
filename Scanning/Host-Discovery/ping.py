import subprocess
import platform

class Ping:
    @staticmethod
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
        
'''
Ejemplo de uso:
if __name__ == "__main__":
    ip_address = "8.8.8.8"  # Cambia la IP según necesites
    if Ping.is_host_active(ip_address):
        print(f"{ip_address} está activo.")
    else:
        print(f"{ip_address} no está activo.") 
'''