#!/usr/bin/env python3
"""
NetInv - Network Inventory Tool
Full CLI network scanner with blue aesthetics
"""

import sys
import os
import socket
import subprocess
import ipaddress
import threading
import time
import json
import csv
import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── ANSI COLOR CODES ────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

# Blues palette
B1      = "\033[38;5;27m"   # Deep blue
B2      = "\033[38;5;33m"   # Medium blue
B3      = "\033[38;5;39m"   # Bright blue
B4      = "\033[38;5;45m"   # Cyan-blue
B5      = "\033[38;5;51m"   # Light cyan
BG      = "\033[48;5;17m"   # Dark blue background

WHITE   = "\033[97m"
GRAY    = "\033[38;5;244m"
GREEN   = "\033[38;5;82m"
RED     = "\033[38;5;196m"
YELLOW  = "\033[38;5;220m"
ORANGE  = "\033[38;5;208m"

# ─── ASCII ART ───────────────────────────────────────────────────────────────
BANNER = f"""
{B1}╔═══════════════════════════════════════════════════════════════════════╗{RESET}
{B1}║{B2}  ███╗   ██╗███████╗████████╗██╗███╗   ██╗██╗   ██╗{B3}  ██╗   ██╗ ██╗{B1}  ║{RESET}
{B1}║{B2}  ████╗  ██║██╔════╝╚══██╔══╝██║████╗  ██║██║   ██║{B3}  ██║   ██║███║{B1}  ║{RESET}
{B1}║{B2}  ██╔██╗ ██║█████╗     ██║   ██║██╔██╗ ██║██║   ██║{B3}  ██║   ██║╚██║{B1}  ║{RESET}
{B1}║{B2}  ██║╚██╗██║██╔══╝     ██║   ██║██║╚██╗██║╚██╗ ██╔╝{B3}  ╚██╗ ██╔╝ ██║{B1}  ║{RESET}
{B1}║{B2}  ██║ ╚████║███████╗   ██║   ██║██║ ╚████║ ╚████╔╝{B3}    ╚████╔╝  ██║{B1}  ║{RESET}
{B1}║{B2}  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝  ╚═══╝{B3}      ╚═══╝   ╚═╝{B1}  ║{RESET}
{B1}║{GRAY}                  Network Inventory System v1.0                        {B1}║{RESET}
{B1}╚═══════════════════════════════════════════════════════════════════════╝{RESET}
"""

MINI_BANNER = f"""
{B2}┌─────────────────────────────────────────────┐{RESET}
{B2}│  {B4}NetInv{RESET} {GRAY}·{RESET} {WHITE}Network Inventory System v1.0{RESET}  {B2}│{RESET}
{B2}└─────────────────────────────────────────────┘{RESET}
"""

# ─── COMMON PORTS ────────────────────────────────────────────────────────────
COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 27017: "MongoDB", 6379: "Redis",
}

# ─── SPINNER / ANIMATION ─────────────────────────────────────────────────────
class Spinner:
    def __init__(self, message="Scanning"):
        self.message = message
        self.running = False
        self.thread = None
        self.frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]

    def _spin(self):
        i = 0
        while self.running:
            frame = self.frames[i % len(self.frames)]
            sys.stdout.write(f"\r  {B3}{frame}{RESET} {B2}{self.message}{RESET}   ")
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self, msg=""):
        self.running = False
        if self.thread:
            self.thread.join()
        if msg:
            sys.stdout.write(f"\r  {GREEN}✔{RESET} {msg}   \n")
        else:
            sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()

def progress_bar(current, total, width=40, label=""):
    if total == 0:
        return
    pct = current / total
    filled = int(width * pct)
    bar = f"{B3}{'█' * filled}{B1}{'░' * (width - filled)}{RESET}"
    pct_str = f"{B4}{pct*100:5.1f}%{RESET}"
    sys.stdout.write(f"\r  [{bar}] {pct_str}  {GRAY}{label}{RESET}  ")
    sys.stdout.flush()

# ─── SEPARATOR / UI HELPERS ──────────────────────────────────────────────────
def sep(char="─", width=73, color=B1):
    print(f"{color}{char * width}{RESET}")

def header(title):
    print()
    sep("═")
    print(f"  {B4}{BOLD}{title}{RESET}")
    sep("─")

def info(msg):
    print(f"  {B3}ℹ{RESET}  {msg}")

def ok(msg):
    print(f"  {GREEN}✔{RESET}  {msg}")

def warn(msg):
    print(f"  {YELLOW}⚠{RESET}  {WHITE}{msg}{RESET}")

def err(msg):
    print(f"  {RED}✖{RESET}  {RED}{msg}{RESET}")

def prompt(msg, default=None):
    if default is not None:
        text = f"  {B4}»{RESET} {WHITE}{msg}{RESET} {GRAY}[{default}]{RESET}: "
    else:
        text = f"  {B4}»{RESET} {WHITE}{msg}{RESET}: "
    return input(text).strip()

def menu_item(num, title, desc=""):
    n = f"{B3}[{B4}{num}{B3}]{RESET}"
    t = f"{WHITE}{title}{RESET}"
    d = f"{GRAY}  {desc}{RESET}" if desc else ""
    print(f"  {n}  {t}{d}")

# ─── NETWORK SCANNING ────────────────────────────────────────────────────────

def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "—"

def ping_host(ip, timeout=1):
    """Ping a host using socket (cross-platform fallback)."""
    try:
        # Try ICMP via subprocess
        param = "-n" if os.name == "nt" else "-c"
        result = subprocess.run(
            ["ping", param, "1", "-W", str(timeout), str(ip)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=timeout + 1
        )
        return result.returncode == 0
    except:
        pass
    # Fallback: TCP connect to port 80 or 443
    for port in [80, 443, 22, 445]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            if sock.connect_ex((str(ip), port)) == 0:
                sock.close()
                return True
            sock.close()
        except:
            pass
    return False

def scan_port(ip, port, timeout=0.8):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((str(ip), port))
        s.close()
        return port if result == 0 else None
    except:
        return None

def scan_ports(ip, ports=None, timeout=0.8, max_workers=50):
    if ports is None:
        ports = list(COMMON_PORTS.keys())
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(scan_port, ip, p, timeout): p for p in ports}
        for f in as_completed(futures):
            r = f.result()
            if r is not None:
                open_ports.append(r)
    return sorted(open_ports)

def scan_network(cidr, ping_timeout=1, workers=100, on_progress=None):
    """Scan all hosts in a CIDR network."""
    try:
        net = ipaddress.ip_network(cidr, strict=False)
    except ValueError as e:
        raise ValueError(f"CIDR inválido: {e}")

    hosts = list(net.hosts())
    results = []
    lock = threading.Lock()
    completed = [0]

    def check_host(ip):
        alive = ping_host(ip, ping_timeout)
        hostname = resolve_hostname(str(ip)) if alive else "—"
        with lock:
            completed[0] += 1
            if on_progress:
                on_progress(completed[0], len(hosts), str(ip))
        if alive:
            return {"ip": str(ip), "hostname": hostname, "status": "Online"}
        return None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(check_host, ip): ip for ip in hosts}
        for f in as_completed(futures):
            r = f.result()
            if r:
                with lock:
                    results.append(r)

    return sorted(results, key=lambda x: ipaddress.ip_address(x["ip"]))

# ─── REPORT GENERATION ───────────────────────────────────────────────────────

def report_json(results, cidr, filename=None):
    data = {
        "scan_time": datetime.datetime.now().isoformat(),
        "network": cidr,
        "total_hosts": len(results),
        "hosts": results,
    }
    fn = filename or f"netinv_{cidr.replace('/', '_')}_{timestamp()}.json"
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return fn

def report_csv(results, cidr, filename=None):
    fn = filename or f"netinv_{cidr.replace('/', '_')}_{timestamp()}.csv"
    with open(fn, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["ip", "hostname", "status", "open_ports"])
        w.writeheader()
        for host in results:
            row = dict(host)
            if "open_ports" in row and isinstance(row["open_ports"], list):
                row["open_ports"] = ", ".join(str(p) for p in row["open_ports"])
            else:
                row.setdefault("open_ports", "")
            w.writerow(row)
    return fn

def report_txt(results, cidr, filename=None):
    fn = filename or f"netinv_{cidr.replace('/', '_')}_{timestamp()}.txt"
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        "=" * 70,
        f"  NETINV - RELATÓRIO DE INVENTÁRIO DE REDE",
        f"  Rede escaneada : {cidr}",
        f"  Data/Hora      : {now}",
        f"  Hosts online   : {len(results)}",
        "=" * 70,
        "",
        f"{'IP':<18} {'Hostname':<30} {'Status':<10} {'Portas Abertas'}",
        "-" * 70,
    ]
    for h in results:
        ports = h.get("open_ports", [])
        port_str = ", ".join(
            f"{p}({COMMON_PORTS.get(p, '?')})" for p in ports
        ) if ports else "—"
        lines.append(f"{h['ip']:<18} {h['hostname']:<30} {h['status']:<10} {port_str}")
    lines += ["", "=" * 70, f"  Total de dispositivos online: {len(results)}", "=" * 70]
    with open(fn, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return fn

def timestamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ─── DISPLAY TABLE ───────────────────────────────────────────────────────────

def print_results_table(results):
    if not results:
        warn("Nenhum host encontrado na rede.")
        return
    print()
    print(f"  {B1}┌{'─'*18}┬{'─'*30}┬{'─'*9}┬{'─'*12}┐{RESET}")
    print(f"  {B1}│{RESET} {B4}{'IP':<17}{RESET}{B1}│{RESET} {B4}{'Hostname':<29}{RESET}{B1}│{RESET} {B4}{'Status':<8}{RESET}{B1}│{RESET} {B4}{'Portas':<11}{RESET}{B1}│{RESET}")
    print(f"  {B1}├{'─'*18}┼{'─'*30}┼{'─'*9}┼{'─'*12}┤{RESET}")
    for h in results:
        ip    = h["ip"]
        host  = h["hostname"][:28]
        stat  = h["status"]
        ports = h.get("open_ports", [])
        port_s = str(len(ports)) + " abertas" if ports else "—"
        color  = GREEN if stat == "Online" else RED
        print(f"  {B1}│{RESET} {WHITE}{ip:<17}{RESET}{B1}│{RESET} {GRAY}{host:<29}{RESET}{B1}│{RESET} {color}{stat:<8}{RESET}{B1}│{RESET} {B3}{port_s:<11}{RESET}{B1}│{RESET}")
    print(f"  {B1}└{'─'*18}┴{'─'*30}┴{'─'*9}┴{'─'*12}┘{RESET}")
    print(f"\n  {B4}Total online:{RESET} {GREEN}{BOLD}{len(results)}{RESET} {WHITE}dispositivo(s){RESET}\n")

def print_port_detail(host):
    ports = host.get("open_ports", [])
    print(f"\n  {B4}Host:{RESET} {WHITE}{host['ip']}{RESET}  {GRAY}{host['hostname']}{RESET}")
    if not ports:
        print(f"  {GRAY}Nenhuma porta aberta detectada.{RESET}")
        return
    print(f"  {B1}┌{'─'*8}┬{'─'*18}┐{RESET}")
    print(f"  {B1}│{RESET} {B4}{'Porta':<7}{RESET}{B1}│{RESET} {B4}{'Serviço':<17}{RESET}{B1}│{RESET}")
    print(f"  {B1}├{'─'*8}┼{'─'*18}┤{RESET}")
    for p in ports:
        svc = COMMON_PORTS.get(p, "Desconhecido")
        print(f"  {B1}│{RESET} {GREEN}{str(p):<7}{RESET}{B1}│{RESET} {WHITE}{svc:<17}{RESET}{B1}│{RESET}")
    print(f"  {B1}└{'─'*8}┴{'─'*18}┘{RESET}")

# ─── SCREENS / FLOWS ─────────────────────────────────────────────────────────

def screen_scan():
    header("ESCANEAMENTO DE REDE")
    cidr = prompt("Endereço de rede (ex: 192.168.1.0/24)")
    if not cidr:
        err("Endereço inválido.")
        return None, None

    # Validate
    try:
        net = ipaddress.ip_network(cidr, strict=False)
        total_hosts = net.num_addresses - 2
        if total_hosts <= 0:
            total_hosts = 1
    except ValueError as e:
        err(str(e))
        return None, None

    scan_ports_opt = prompt("Escanear portas dos hosts encontrados? (s/n)", "s").lower()
    do_ports = scan_ports_opt in ("s", "sim", "y", "yes")

    print()
    info(f"Rede: {B4}{cidr}{RESET}  ({total_hosts} hosts possíveis)")
    info(f"Scan de portas: {'Sim' if do_ports else 'Não'}")
    print()

    # Host discovery
    results = []
    start_time = time.time()

    def on_progress(done, total, current_ip):
        progress_bar(done, total, label=f"{current_ip}")

    print(f"  {B2}Fase 1: Descoberta de hosts...{RESET}")
    print()
    try:
        results = scan_network(cidr, on_progress=on_progress)
    except ValueError as e:
        err(str(e))
        return None, None

    progress_bar(total_hosts, total_hosts, label="Concluído")
    print(f"\n  {GREEN}✔{RESET} {len(results)} host(s) online encontrado(s)\n")

    # Port scanning
    if do_ports and results:
        print(f"  {B2}Fase 2: Escaneamento de portas...{RESET}\n")
        for i, host in enumerate(results):
            spin = Spinner(f"Portas em {host['ip']} ({i+1}/{len(results)})")
            spin.start()
            ports = scan_ports(host["ip"])
            spin.stop(f"{host['ip']} → {GREEN}{len(ports)} porta(s) aberta(s){RESET}")
            host["open_ports"] = ports
        print()

    elapsed = time.time() - start_time
    ok(f"Scan concluído em {elapsed:.1f}s")
    print()

    print_results_table(results)

    if do_ports and results:
        show_ports = prompt("Ver detalhe de portas por host? (s/n)", "n").lower()
        if show_ports in ("s", "sim", "y"):
            for h in results:
                if h.get("open_ports"):
                    print_port_detail(h)

    return results, cidr


def screen_reports(results, cidr):
    if not results:
        err("Nenhum dado de scan disponível. Execute um escaneamento primeiro.")
        return

    header("GERAR RELATÓRIO")
    print()
    menu_item(1, "JSON", "relatório estruturado em JSON")
    menu_item(2, "CSV",  "planilha compatível com Excel")
    menu_item(3, "TXT",  "relatório em texto puro")
    menu_item(4, "Todos os formatos")
    menu_item(0, "Voltar")
    print()

    choice = prompt("Escolha o formato")

    formats = {
        "1": [("json", report_json)],
        "2": [("csv",  report_csv)],
        "3": [("txt",  report_txt)],
        "4": [("json", report_json), ("csv", report_csv), ("txt", report_txt)],
    }

    if choice == "0":
        return

    selected = formats.get(choice)
    if not selected:
        err("Opção inválida.")
        return

    print()
    for fmt, fn in selected:
        spin = Spinner(f"Gerando {fmt.upper()}...")
        spin.start()
        try:
            path = fn(results, cidr)
            spin.stop(f"{fmt.upper()} salvo → {B4}{path}{RESET}")
        except Exception as e:
            spin.stop()
            err(f"Erro ao gerar {fmt}: {e}")


def screen_live_monitor(cidr):
    """Simple live host monitor — pings every N seconds."""
    header("MONITOR EM TEMPO REAL")
    if not cidr:
        cidr = prompt("Endereço de rede (ex: 192.168.1.0/24)", "192.168.1.0/24")

    interval = prompt("Intervalo de atualização (segundos)", "10")
    try:
        interval = int(interval)
    except:
        interval = 10

    info(f"Monitorando {B4}{cidr}{RESET} a cada {interval}s — {YELLOW}Ctrl+C para parar{RESET}")
    print()

    iteration = 0
    try:
        while True:
            iteration += 1
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"  {B1}[{ts}]{RESET} {B2}Ciclo #{iteration}{RESET}")

            def on_prog(done, total, ip):
                pass  # silent

            results = scan_network(cidr, ping_timeout=1, workers=100, on_progress=on_prog)

            print(f"  {B4}Hosts online: {GREEN}{BOLD}{len(results)}{RESET}")
            for h in results:
                print(f"    {B3}●{RESET} {WHITE}{h['ip']:<18}{RESET} {GRAY}{h['hostname']}{RESET}")

            sep("─", 50, B1)
            print(f"  {GRAY}Próxima verificação em {interval}s...{RESET}\n")
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n  {YELLOW}Monitor encerrado.{RESET}")


def screen_port_scan():
    header("SCAN DE PORTAS — HOST ÚNICO")
    ip = prompt("Endereço IP do host")
    if not ip:
        return

    port_opt = prompt("Portas: (1) Comuns  (2) Personalizada", "1")
    if port_opt == "2":
        raw = prompt("Portas separadas por vírgula (ex: 22,80,443)")
        try:
            ports = [int(p.strip()) for p in raw.split(",") if p.strip().isdigit()]
        except:
            err("Entrada inválida.")
            return
    else:
        ports = list(COMMON_PORTS.keys())

    print()
    spin = Spinner(f"Escaneando {ip}...")
    spin.start()
    open_ports = scan_ports(ip, ports)
    hostname = resolve_hostname(ip)
    spin.stop(f"Scan concluído — {len(open_ports)} porta(s) aberta(s)")

    host = {"ip": ip, "hostname": hostname, "status": "Online", "open_ports": open_ports}
    print_port_detail(host)


def screen_about():
    print()
    sep()
    print(f"""
  {B4}{BOLD}NetInv v1.0{RESET} — Network Inventory System

  {GRAY}Criado para escaneamento e inventário de redes corporativas.

  Funcionalidades:{RESET}
    {B3}●{RESET} Descoberta de hosts via ICMP/TCP
    {B3}●{RESET} Resolução de hostnames
    {B3}●{RESET} Scan de portas comuns (21 portas)
    {B3}●{RESET} Relatórios: JSON, CSV, TXT
    {B3}●{RESET} Monitor em tempo real
    {B3}●{RESET} Scan de host único

  {GRAY}Tecnologias: Python, socket, subprocess, threading{RESET}
  {GRAY}Licença: MIT{RESET}
    """)
    sep()

# ─── MAIN MENU ───────────────────────────────────────────────────────────────

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)

    last_results = None
    last_cidr = None

    while True:
        print(f"\n{B1}  ╔══════════════════════════════╗{RESET}")
        print(f"{B1}  ║{RESET}  {B4}{BOLD}MENU PRINCIPAL{RESET}               {B1}║{RESET}")
        print(f"{B1}  ╠══════════════════════════════╣{RESET}")
        menu_item(1, "Escanear Rede",         "descobre hosts e portas")
        menu_item(2, "Gerar Relatório",        "JSON / CSV / TXT")
        menu_item(3, "Monitor em Tempo Real",  "ping cíclico na rede")
        menu_item(4, "Scan de Host Único",     "portas de um IP específico")
        menu_item(5, "Sobre",                  "informações da ferramenta")
        menu_item(0, "Sair")
        print(f"{B1}  ╚══════════════════════════════╝{RESET}\n")

        if last_results:
            info(f"Último scan: {B4}{last_cidr}{RESET} — {GREEN}{len(last_results)} host(s){RESET}")
        print()

        choice = prompt("Escolha uma opção")

        if choice == "1":
            res, cidr = screen_scan()
            if res is not None:
                last_results = res
                last_cidr = cidr

        elif choice == "2":
            screen_reports(last_results, last_cidr)

        elif choice == "3":
            screen_live_monitor(last_cidr)

        elif choice == "4":
            screen_port_scan()

        elif choice == "5":
            screen_about()

        elif choice == "0":
            print(f"\n  {B4}Encerrando NetInv...{RESET}\n")
            sys.exit(0)

        else:
            err("Opção inválida. Tente novamente.")

        input(f"\n  {GRAY}Pressione Enter para continuar...{RESET}")
        os.system("cls" if os.name == "nt" else "clear")
        print(MINI_BANNER)


if __name__ == "__main__":
    main()
