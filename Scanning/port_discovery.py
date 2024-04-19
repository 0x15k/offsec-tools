import socket
import signal
import sys

class PortScanner:
    def __init__(self, target, start_port, end_port, verbose=None):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.verbose = verbose
        self.open_ports = []
        signal.signal(signal.SIGINT, self.signal_handler)

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    self.open_ports.append(port)
                    if self.verbose:
                        print(f"El puerto {port} está abierto.")
        
        except socket.error:
            pass

    def scan_ports(self):
        try:
            for port in range(self.start_port, self.end_port + 1):
                self.scan_port(port)
        except KeyboardInterrupt:
            print('\nEscaneo interrumpido.')
            sys.exit(0)
        if self.open_ports:
            print(f"Los siguientes puertos están abiertos en {self.target}:")
            for port in self.open_ports:
                print(port)
        else:
            print(f"No se encontraron puertos abiertos en {self.target}.")
    def signal_handler(self, sig, frame):
        print('\nCtrl+C detectado. Saliendo...')
        sys.exit(0)    

    @classmethod
    def main(cls, target, start_port, end_port, verbose):
        port_scanner = cls(target, start_port, end_port, verbose)
        port_scanner.scan_ports()

if __name__ == "__main__":    
    '''
    PortScanner.main("192.168.18.1", 50, 90, verbose=True)
    '''