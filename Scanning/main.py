import sys
import argparse
sys.path.append('Scanning/Host-Discovery')
sys.path.append('Scanning/Port-Discovery')
from host_discovery import HostDiscovery
from port_discovery import PortScanner

def parse_arguments():
    parser = argparse.ArgumentParser(description="0x15k Scanner")
    parser.add_argument("--network", help="Network address and subnet mask (e.g., 192.168.1.0/24)")
    parser.add_argument("--target", help="Target (e.g., 192.168.1.1)")
    parser.add_argument("--ports", help="Range ports (e.g.,1-99)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    # Si no se proporcionan argumentos, mostrar la ayuda y salir
    if not any(vars(args).values()):
        parser.print_help()
        sys.exit(1)

    return args

def discover_hosts(network):
    host_discovery = HostDiscovery()
    host_discovery.main(network)

def discover_ports(target, start_port, end_port, verbose):
    port_discovery = PortScanner(target, start_port, end_port, verbose)
    port_discovery.main(target, start_port, end_port, verbose)

if __name__ == "__main__":
    args = parse_arguments()

    if args.network:
        discover_hosts(args.network)
    elif args.target and args.ports:
        try:
            start_port, end_port = map(int, args.ports.split("-"))
        except ValueError:
            print("Error: Invalid port range format. Please use format 'start-end'.")
            sys.exit(1)
           
        discover_ports(args.target, start_port, end_port, args.verbose)