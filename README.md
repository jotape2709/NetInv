
<div align="center">

```
╔═══════════════════════════════════════════════════════════════════════╗
║  ███╗   ██╗███████╗████████╗██╗███╗   ██╗██╗   ██╗  ██╗   ██╗ ██╗  ║
║  ████╗  ██║██╔════╝╚══██╔══╝██║████╗  ██║██║   ██║  ██║   ██║███║  ║
║  ██╔██╗ ██║█████╗     ██║   ██║██╔██╗ ██║██║   ██║  ██║   ██║╚██║  ║
║  ██║╚██╗██║██╔══╝     ██║   ██║██║╚██╗██║╚██╗ ██╔╝  ╚██╗ ██╔╝ ██║  ║
║  ██║ ╚████║███████╗   ██║   ██║██║ ╚████║ ╚████╔╝    ╚████╔╝  ██║  ║
║  ╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝╚═╝  ╚═══╝  ╚═══╝      ╚═══╝   ╚═╝  ║
║                  Network Inventory System v1.0                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

**Ferramenta CLI de inventário de rede — 100% Python, zero dependências externas.**

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?style=flat-square&logo=python&logoColor=white)
![Plataforma](https://img.shields.io/badge/Plataforma-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=flat-square)
![Licença](https://img.shields.io/badge/Licença-MIT-blue?style=flat-square)
![Dependências](https://img.shields.io/badge/Dependências-Nenhuma-brightgreen?style=flat-square)
![Arquivo único](https://img.shields.io/badge/Arquivo-Único-blue?style=flat-square)

</div>

---

## 📋 Índice

- [O que é o NetInv?](#-o-que-é-o-netinv)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como usar](#-como-usar)
- [Funcionalidades](#-funcionalidades)
- [Relatórios](#-relatórios)
- [Portas escaneadas](#-portas-escaneadas)
- [Dúvidas frequentes](#-dúvidas-frequentes)
- [Observações de segurança](#-observações-de-segurança)

---

## 🔍 O que é o NetInv?

O **NetInv** é uma ferramenta de linha de comando (CLI) feita em Python puro para realizar **inventário de redes corporativas ou domésticas**. Ele resolve um problema comum: empresas e administradores muitas vezes não sabem quais dispositivos estão conectados, quais IPs estão ativos ou quais portas estão abertas.

Com o NetInv você descobre tudo isso de forma rápida, com uma interface visual agradável e relatórios prontos para uso.

```
  ╔══════════════════════════════╗
  ║  MENU PRINCIPAL              ║
  ╠══════════════════════════════╣
  [1]  Escanear Rede         descobre hosts e portas
  [2]  Gerar Relatório        JSON / CSV / TXT
  [3]  Monitor em Tempo Real  ping cíclico na rede
  [4]  Scan de Host Único     portas de um IP específico
  [5]  Sobre                  informações da ferramenta
  [0]  Sair
  ╚══════════════════════════════╝
```

---

## ✅ Pré-requisitos

### Python

O NetInv requer **Python 3.7 ou superior**. Verifique sua versão:

```bash
python3 --version
```

Se o comando acima retornar algo como `Python 3.8.10` ou maior, você já está pronto. Caso contrário, veja como instalar:

<details>
<summary><strong>🐧 Linux (Ubuntu / Debian)</strong></summary>

```bash
sudo apt update
sudo apt install python3
```

</details>

<details>
<summary><strong>🍎 macOS</strong></summary>

```bash
# Com Homebrew (recomendado)
brew install python3

# Ou baixe o instalador oficial em:
# https://www.python.org/downloads/
```

</details>

<details>
<summary><strong>🪟 Windows</strong></summary>

1. Acesse [python.org/downloads](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python 3
3. **Durante a instalação, marque a opção "Add Python to PATH"**
4. Conclua a instalação

Para verificar:
```cmd
python --version
```

</details>

### Bibliotecas externas

> **Nenhuma.** O NetInv utiliza apenas bibliotecas que já vêm com o Python (chamadas de *stdlib*):

| Biblioteca | Para que serve no NetInv |
|------------|--------------------------|
| `socket` | Conexões TCP para detectar portas abertas |
| `subprocess` | Executar o comando `ping` do sistema |
| `ipaddress` | Validar e iterar sobre endereços de rede (ex: `192.168.1.0/24`) |
| `threading` | Executar múltiplos scans ao mesmo tempo (paralelismo) |
| `concurrent.futures` | Gerenciar o pool de threads para scans rápidos |
| `json` | Gerar relatórios no formato JSON |
| `csv` | Gerar relatórios no formato CSV |
| `datetime` | Registrar data e hora nos relatórios |
| `os`, `sys`, `time` | Utilitários gerais do sistema |

**Você não precisa rodar `pip install` de nada.**

---

## 📦 Instalação

Por ser um arquivo único, a "instalação" é simplesmente baixar o arquivo. Escolha o método que preferir:

### Opção 1 — Clonar o repositório (recomendado)

```bash
git clone https://github.com/seu-usuario/netinv.git
cd netinv
```

### Opção 2 — Baixar somente o arquivo

```bash
# Com curl
curl -O https://raw.githubusercontent.com/seu-usuario/netinv/main/netinv.py

# Com wget
wget https://raw.githubusercontent.com/seu-usuario/netinv/main/netinv.py
```

### Opção 3 — Download manual

Clique em **`netinv.py`** neste repositório → botão **Download raw file** (ícone de seta para baixo).

---

## 🚀 Como usar

### Iniciando a ferramenta

```bash
# Linux / macOS
python3 netinv.py

# Windows
python netinv.py
```

> **Dica no Linux/macOS:** Você pode tornar o arquivo executável diretamente:
> ```bash
> chmod +x netinv.py
> ./netinv.py
> ```

### Exemplo de sessão completa

**1. Escaneando uma rede:**
```
  » Endereço de rede (ex: 192.168.1.0/24): 192.168.1.0/24
  » Escanear portas dos hosts encontrados? (s/n) [s]: s

  ℹ  Rede: 192.168.1.0/24  (254 hosts possíveis)

  Fase 1: Descoberta de hosts...
  [████████████████████████░░░░░░░░░░░░░░░░]  62.0%  192.168.1.158
  ✔ 3 host(s) online encontrado(s)

  Fase 2: Escaneamento de portas...
  ✔ 192.168.1.1   → 2 porta(s) aberta(s)
  ✔ 192.168.1.10  → 1 porta(s) aberta(s)
  ✔ 192.168.1.20  → 1 porta(s) aberta(s)

  ┌──────────────────┬──────────────────────────────┬─────────┬────────────┐
  │ IP               │ Hostname                     │ Status  │ Portas     │
  ├──────────────────┼──────────────────────────────┼─────────┼────────────┤
  │ 192.168.1.1      │ router.local                 │ Online  │ 2 abertas  │
  │ 192.168.1.10     │ notebook.local               │ Online  │ 1 abertas  │
  │ 192.168.1.20     │ impressora.local             │ Online  │ 1 abertas  │
  └──────────────────┴──────────────────────────────┴─────────┴────────────┘

  Total online: 3 dispositivo(s)
```

**2. Entendendo o formato de rede `/24` (CIDR):**

Ao inserir o endereço de rede, você usa a notação **CIDR**. Veja os mais comuns:

| Notação | Equivalente | Hosts escaneados |
|---------|-------------|-----------------|
| `192.168.1.0/24` | 192.168.1.1 até .254 | 254 hosts |
| `192.168.0.0/23` | 192.168.0.1 até 192.168.1.254 | 510 hosts |
| `10.0.0.0/8` | 10.0.0.1 até 10.255.255.254 | ~16 milhões (não recomendado) |
| `192.168.1.100/32` | Apenas 192.168.1.100 | 1 host |

> **Como saber minha rede?**
> - Linux/macOS: `ip route` ou `ifconfig`
> - Windows: `ipconfig`
>
> Procure pelo campo **"default via"** ou **"Gateway Padrão"**. Se seu gateway é `192.168.1.1`, sua rede provavelmente é `192.168.1.0/24`.

---

## ⚙️ Funcionalidades

### `[1]` Escanear Rede

Descobre todos os dispositivos ativos em uma faixa de IPs.

- **Fase 1 — Descoberta de hosts:** Testa cada IP com `ping` via ICMP. Se o ping for bloqueado (firewall), faz fallback automático via TCP nas portas 80, 443, 22 e 445.
- **Fase 2 — Scan de portas** *(opcional)*: Para cada host encontrado, verifica 21 portas comuns em paralelo usando threads.
- Barra de progresso em tempo real durante o scan.
- Exibe tabela com IP, hostname resolvido, status e quantidade de portas abertas.

### `[2]` Gerar Relatório

Exporta os dados do último scan realizado. Formatos disponíveis:

- **JSON** — estruturado, ideal para integrar com outros sistemas
- **CSV** — abre diretamente no Excel / Google Sheets
- **TXT** — relatório em texto legível, pronto para enviar por e-mail
- **Todos** — gera os três formatos de uma vez

Os arquivos são salvos na pasta onde você executou o script, com nome automático incluindo a rede e a data/hora.

### `[3]` Monitor em Tempo Real

Pinga a rede em ciclos repetidos com intervalo configurável. Útil para:
- Detectar quando um dispositivo entra ou sai da rede
- Monitorar disponibilidade de servidores
- Acompanhar mudanças durante manutenções

Use `Ctrl + C` para encerrar o monitor.

### `[4]` Scan de Host Único

Verifica as portas abertas de um IP específico, sem precisar escanear a rede inteira. Permite usar as 21 portas comuns ou informar portas personalizadas.

```
  » Endereço IP do host: 192.168.1.1
  » Portas: (1) Comuns  (2) Personalizada: 1

  ✔ Scan concluído — 2 porta(s) aberta(s)

  ┌────────┬────────────────────┐
  │ Porta  │ Serviço            │
  ├────────┼────────────────────┤
  │ 80     │ HTTP               │
  │ 443    │ HTTPS              │
  └────────┴────────────────────┘
```

---

## 📄 Relatórios

### JSON (`netinv_192.168.1.0_24_20260606_142300.json`)

```json
{
  "scan_time": "2026-06-06T14:23:00",
  "network": "192.168.1.0/24",
  "total_hosts": 3,
  "hosts": [
    {
      "ip": "192.168.1.1",
      "hostname": "router.local",
      "status": "Online",
      "open_ports": [80, 443]
    }
  ]
}
```

### CSV (`netinv_192.168.1.0_24_20260606_142300.csv`)

```
ip,hostname,status,open_ports
192.168.1.1,router.local,Online,"80, 443"
192.168.1.10,notebook.local,Online,22
192.168.1.20,impressora.local,Online,80
```

### TXT (`netinv_192.168.1.0_24_20260606_142300.txt`)

```
======================================================================
  NETINV - RELATÓRIO DE INVENTÁRIO DE REDE
  Rede escaneada : 192.168.1.0/24
  Data/Hora      : 2026-06-06 14:23:00
  Hosts online   : 3
======================================================================

IP                 Hostname                       Status     Portas Abertas
----------------------------------------------------------------------
192.168.1.1        router.local                   Online     80(HTTP), 443(HTTPS)
192.168.1.10       notebook.local                 Online     22(SSH)
192.168.1.20       impressora.local               Online     80(HTTP)

======================================================================
  Total de dispositivos online: 3
======================================================================
```

---

## 🔌 Portas escaneadas

O scan padrão verifica as 21 portas mais comuns em redes corporativas:

| Porta | Serviço | Uso típico |
|-------|---------|------------|
| 21 | FTP | Transferência de arquivos |
| 22 | SSH | Acesso remoto seguro |
| 23 | Telnet | Acesso remoto (legado) |
| 25 | SMTP | Envio de e-mail |
| 53 | DNS | Resolução de nomes |
| 80 | HTTP | Páginas web |
| 110 | POP3 | Recebimento de e-mail |
| 143 | IMAP | Recebimento de e-mail |
| 443 | HTTPS | Páginas web seguras |
| 445 | SMB | Compartilhamento de arquivos (Windows) |
| 3306 | MySQL | Banco de dados |
| 3389 | RDP | Área de trabalho remota (Windows) |
| 5432 | PostgreSQL | Banco de dados |
| 5900 | VNC | Acesso remoto gráfico |
| 6379 | Redis | Banco de dados em memória |
| 8080 | HTTP-Alt | Servidores alternativos |
| 8443 | HTTPS-Alt | Servidores alternativos seguros |
| 27017 | MongoDB | Banco de dados NoSQL |

---

## ❓ Dúvidas frequentes

**O scan está muito lento. O que fazer?**

Redes maiores (`/16`, `/8`) podem ter milhares de IPs. Para redes domésticas e corporativas comuns, `/24` (254 hosts) é o ideal e leva entre 10 e 60 segundos dependendo da sua rede.

---

**Alguns dispositivos online não aparecem no resultado. Por quê?**

Alguns dispositivos bloqueiam ICMP (ping) por firewall. O NetInv tenta automaticamente um fallback via TCP nas portas 80, 443, 22 e 445. Se o dispositivo bloquear tudo, ele não será detectado — comportamento normal para qualquer scanner de rede.

---

**No Linux aparece "Permission denied" ou o ping não funciona. O que fazer?**

O ping padrão do Linux pode exigir permissões especiais para ICMP. Execute com `sudo`:

```bash
sudo python3 netinv.py
```

Alternativamente, o fallback TCP funcionará mesmo sem `sudo` na maioria dos casos.

---

**As cores não aparecem no Windows. Como resolver?**

No Windows 10/11, o terminal moderno (Windows Terminal) suporta cores ANSI nativamente. Se estiver usando o `cmd.exe` antigo, ative o suporte a cores com:

```cmd
reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1
```

Ou use o **Windows Terminal** (disponível na Microsoft Store gratuitamente).

---

**Posso usar o NetInv em redes que não são minhas?**

**Não.** Escanear redes sem autorização é ilegal em muitos países e viola a Lei de Crimes Informáticos (Lei nº 12.737/2012 no Brasil). Use somente em redes que você administra ou tem permissão explícita para testar.

---

## 🔒 Observações de segurança

- Use o NetInv **somente em redes que você administra ou tem autorização** para escanear.
- O scan de portas pode acionar alertas em firewalls e sistemas de detecção de intrusão (IDS).
- Em ambientes corporativos, comunique o time de segurança antes de executar qualquer scan.
- No Brasil, o uso não autorizado desta ferramenta pode configurar crime previsto na **Lei nº 12.737/2012 (Lei Carolina Dieckmann)**.

---

## 📁 Estrutura do projeto

```
netinv/
└── netinv.py       # Arquivo principal — tudo em um só lugar
```

Sem pastas extras, sem arquivos de configuração, sem `requirements.txt`. Um arquivo, tudo dentro.

---

## 🛠️ Tecnologias utilizadas

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| Python | 3.7+ | Linguagem principal |
| `socket` | stdlib | Scan de portas TCP |
| `subprocess` | stdlib | Execução do ping do sistema |
| `ipaddress` | stdlib | Parsing e iteração de CIDRs |
| `threading` / `concurrent.futures` | stdlib | Paralelismo nos scans |
| `json` / `csv` | stdlib | Geração de relatórios |

---

## 📜 Licença

Distribuído sob a licença **MIT**. Veja o arquivo `LICENSE` para mais detalhes.

---

<div align="center">

Feito com Python puro · Sem dependências · Funciona em qualquer lugar

</div>
