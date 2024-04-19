import socket
import signal
import sys

def signal_handler(sig, frame):
        print('\nCtrl+C detectado. Saliendo...')
        sys.exit(0)  
class PortScanner:
    def __init__(self, target, start_port, end_port, verbose=None):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.verbose = verbose
        self.open_ports = []
        signal.signal(signal.SIGINT, signal_handler)

    def scan_ports(self):
        try:
            for port in range(self.start_port, self.end_port + 1):
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
        except KeyboardInterrupt:
            print('\nEscaneo interrumpido.')
            sys.exit(0)
        
        if self.open_ports:
            print(f"Los siguientes puertos están abiertos en {self.target}:")
            for port in self.open_ports:
                print(port)
        else:
            print(f"No se encontraron puertos abiertos en {self.target}.")

    def discover_services(self):
        if not self.open_ports:
            print("No hay puertos abiertos para descubrir servicios.")
            return
        
        print("Descubriendo servicios para los puertos abiertos:")
        for port in self.open_ports:
            try:
                service = socket.getservbyport(port)
                print(f"Puerto {port}: {service}")
            except OSError:
                print(f"No se pudo determinar el servicio para el puerto {port}")

    @classmethod
    def main(cls, target, start_port, end_port, verbose):
        port_scanner = cls(target, start_port, end_port, verbose)
        port_scanner.scan_ports()
        port_scanner.discover_services()

if __name__ == "__main__":    
    PortScanner.main("8.8.8.8", 400, 460, verbose=True)
