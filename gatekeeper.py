#!/usr/bin/env python3

import socket
import ipaddress
import concurrent.futures
import argparse
from datetime import datetime
import sys
from typing import List, Tuple, Optional

class Colors:
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BLUE = '\033[94m'
	MAGENTA = '\033[95m'
	CYAN = '\033[96m'
	WHITE = '\033[97m'
	RESET = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

SERVICE_BANNERS = {
	21: "FTP",
	22: "SSH",
	23: "Telnet",
	25: "SMTP",
	53: "DNS",
	80: "HTTP",
	110: "POP3",
	143: "IMAP",
	443: "HTTPS",
	3306: "MySQL",
	3389: "RDP",
	5900: "VNC",
	8080: "HTTP-Alt"
}

def validate_ip(target: str) -> bool:
	try:
		ipaddress.ip_address(target)
		return True
	except ValueError:
		return False

def scan_port(target: str, port: int, timeout: float = 1.0) -> Optional[Tuple[int, str]]:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.settimeout(timeout)
			result = s.connect_ex((target, port))

			if result == 0:
				try:
					# Tenta obter banner do serviço
					banner = s.recv(1024).decode('utf-8').strip()
					if not banner:
						banner = SERVICE_BANNERS.get(port, "Serviço desconhecido")
					else:
						banner = f"{SERVICE_BANNERS.get(port, 'Serviço desconhecido')} ({banner[:50]})"
				except:
					banner = SERVICE_BANNERS.get(port, "Serviço desconhecido")

				return (port, banner)
	except Exception:
		pass
	return None

def port_scan(target: str, ports: List[int], threads: int = 100, timeout: float = 1.0) -> List[Tuple[int, str]]:
	open_ports = []

	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
		future_to_port = {executor.submit(scan_port, target, port, timeout): port for port in ports}

		for future in concurrent.futures.as_completed(future_to_port):
			port = future_to_port[future]
			try:
				result = future.result()
				if result:
					open_ports.append(result)
			except Exception as e:
				print(f"{Colors.RED}[!] Erro ao escanear porta {port}: {e}{Colors.RESET}")

	return sorted(open_ports, key=lambda x: x[0])

def parse_ports(port_str: str) -> List[int]:
	ports = []
	port_ranges = port_str.split(',')

	for port_range in port_ranges:
		if '-' in port_range:
			start, end = map(int, port_range.split('-'))
			ports.extend(range(start, end + 1))
		else:
			ports.append(int(port_range))

	return list(set(ports))

def print_results(target: str, ports: List[int], open_ports: List[Tuple[int, str]], scan_time: float):
	print(f"\n{Colors.BOLD}{Colors.CYAN}Resultados da varredura para {target}:{Colors.RESET}")
	print(f"{Colors.BLUE}Tempo total: {scan_time:.2f} segundos{Colors.RESET}")
	print(f"{Colors.BLUE}Portas escaneadas: {len(ports)}{Colors.RESET}")
	print(f"{Colors.GREEN}Portas abertas: {len(open_ports)}{Colors.RESET}\n")

	if open_ports:
		print(f"{Colors.BOLD}{Colors.WHITE}PORTA\tSERVIÇO{Colors.RESET}")
		print(f"{Colors.BOLD}{Colors.WHITE}-----\t-------{Colors.RESET}")
		for port, banner in open_ports:
			print(f"{Colors.GREEN}{port}\t{banner}{Colors.RESET}")
	else:
		print(f"{Colors.YELLOW}Nenhuma porta aberta encontrada.{Colors.RESET}")

def main():
	parser = argparse.ArgumentParser(
		description="GateKeeper",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=f"""{Colors.BOLD}Exemplos:{Colors.RESET}
  {Colors.CYAN}Escaneamento básico:{Colors.RESET}
	{sys.argv[0]} 192.168.1.1 -p 80,443,22

  {Colors.CYAN}Intervalo de portas:{Colors.RESET}
	{sys.argv[0]} 192.168.1.1 -p 1-1024

  {Colors.CYAN}Múltiplas portas e intervalos:{Colors.RESET}
	{sys.argv[0]} 192.168.1.1 -p 20-25,80,443,3306

  {Colors.CYAN}Usando mais threads para velocidade:{Colors.RESET}
	{sys.argv[0]} 192.168.1.1 -p 1-65535 -t 500
"""
	)

	parser.add_argument("target", help="Endereço IP ou hostname do alvo")
	parser.add_argument("-p", "--ports", default="1-1024",
					   help="Portas para escanear (padrão: 1-1024, ex: 80,443,1000-2000)")
	parser.add_argument("-t", "--threads", type=int, default=100,
					   help="Número de threads (padrão: 100)")
	parser.add_argument("-T", "--timeout", type=float, default=1.0,
					   help="Timeout de conexão em segundos (padrão: 1.0)")

	args = parser.parse_args()

	# Validação do alvo
	if not validate_ip(args.target):
		try:
			args.target = socket.gethostbyname(args.target)
		except socket.gaierror:
			print(f"{Colors.RED}[!] Endereço IP ou hostname inválido: {args.target}{Colors.RESET}")
			sys.exit(1)

	try:
		ports = parse_ports(args.ports)
	except ValueError:
		print(f"{Colors.RED}[!] Formato de portas inválido. Use o formato: 80,443,1000-2000{Colors.RESET}")
		sys.exit(1)

	print(f"{Colors.BOLD}{Colors.BLUE}[*] Iniciando varredura em {args.target}...{Colors.RESET}")
	print(f"{Colors.BLUE}[*] Escaneando {len(ports)} portas com {args.threads} threads{Colors.RESET}")

	start_time = datetime.now()
	open_ports = port_scan(args.target, ports, args.threads, args.timeout)
	end_time = datetime.now()

	scan_time = (end_time - start_time).total_seconds()
	print_results(args.target, ports, open_ports, scan_time)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print(f"\n{Colors.RED}[!] Varredura interrompida pelo usuário.{Colors.RESET}")
		sys.exit(0)
	except Exception as e:
		print(f"{Colors.RED}[!] Erro inesperado: {e}{Colors.RESET}")
		sys.exit(1)