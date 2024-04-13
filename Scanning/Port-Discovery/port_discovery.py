import socket
import argparse
import signal
import sys

class PortScanner:
    def __init__(self, target, start_port, end_port, verbose):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.verbose = verbose
        self.open_ports = []
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, sig, frame):
        print('\nCtrl+C detectado. Saliendo...')
        sys.exit(0)

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

def parse_arguments():
    parser = argparse.ArgumentParser(description="Scan ports of a target host.")
    parser.add_argument("--host", help="Target host IP address", required=True)
    parser.add_argument("-p", "--ports", help="Port range to scan (e.g., 1-100)", required=True)
    parser.add_argument("-v", "--verbose", help="Print each port as it is being scanned", action="store_true")
    args = parser.parse_args()

    # Parse port range
    try:
        start_port, end_port = map(int, args.ports.split("-"))
    except ValueError:
        print("Error: Invalid port range format. Please use format 'start-end'.")
        sys.exit(1)

    return args.host, start_port, end_port, args.verbose

if __name__ == "__main__":
    target, start_port, end_port, verbose = parse_arguments()

    scanner = PortScanner(target, start_port, end_port, verbose)
    scanner.scan_ports()

    open_ports = scanner.open_ports

    if open_ports:
        print(f"Los siguientes puertos están abiertos en {target}:")
        for port in open_ports:
            print(port)
    else:
        print(f"No se encontraron puertos abiertos en {target}.")
