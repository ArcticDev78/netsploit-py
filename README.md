# 📡 Netsploit

###### Also known as `netsploit-py`

> A CLI wrapper for popular network security and pentesting tools — making `nmap`, `hping3`, and `ping` easy to use through an interactive prompt.

![Screenshot](resources/screenshot.png)

---

## 📑 Table of Contents

- [How it works](#-how-it-works)
- [Modules](#-modules)
- [Platform Support](#-platform-support)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Netsploit](#running-netsploit)
- [Usage](#-usage)
- [Credits](#-credits)

---

## 🤔 How it works

- Netsploit is an interactive CLI wrapper around tools like `nmap`, `hping3`, and `ping`.
- Features are organised as **modules** — each module runs a specific network function and lets you configure it through prompts.
- After a module finishes, you can choose whether to save the output to a log file.
- You only need to run `netsploit.py` — no need to touch the source code.

> [!NOTE]
> This is a work-in-progress project. If you run into any bugs or unexpected behaviour, feel free to [open an issue](../../issues).

---

## 📋 Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | `network-scanner` | Find all devices connected to the local network |
| 2 | `device-info` | Gather detailed information about a target device |
| 3 | `os-guesser` | Guess the operating system running on a target device |
| 4 | `port-scanner` | Scan a target device for open ports and services |
| 5 | `vuln-scanner` | Scan a target for known vulnerabilities |
| 6 | `oui-lookup` | Look up a device manufacturer by MAC OUI |
| 7 | `ping` | Check if a target is reachable and measure latency |
| 8 | `dos` | Run a Denial-of-Service attack on a target *(Linux/macOS only)* |

---

## 🖥️ Platform Support

| Platform | Supported | Notes |
|----------|-----------|-------|
| Linux | ✅ Full support | All modules work |
| macOS | ✅ Full support | All modules work |
| Windows | ⚠️ Partial | DoS module unavailable (`hping3` not on Windows) |

Modules that require elevated privileges (network scan, OS detection, device info) run with `sudo` automatically on Linux and macOS. On Windows, run your terminal as **Administrator** before launching Netsploit.

---

## ✅ Getting Started

### Prerequisites

Make sure the following are installed on your system before running setup:

| Tool | Required for | Install |
|------|-------------|---------|
| [Python 3.8+](https://www.python.org/downloads/) | Running Netsploit | [python.org](https://www.python.org/downloads/) |
| [nmap](https://nmap.org/) | All scan modules | `apt install nmap` / `brew install nmap` |
| [hping3](https://github.com/antirez/hping) | DoS module *(Linux/macOS only)* | `apt install hping3` / `brew install hping3` |

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/ArcticDev78/netsploit-py.git
cd netsploit-py
```

> Alternatively, download the ZIP from `Code > Download ZIP` on this page — but note that you won't be able to pull future updates that way.

**2. Run the setup script**

```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Check for Python and system dependencies (`nmap`, `hping3`)
- Create and activate a Python virtual environment (`.venv`)
- Install all Python dependencies from `requirements.txt`
- Create the log directory structure

### Running Netsploit

Activate the virtual environment and launch:

```bash
source .venv/bin/activate
python3 netsploit.py
```

> On macOS/Linux you can also just re-run `./setup.sh` any time — it's safe to run multiple times and won't recreate things that already exist.

---

## 🖱️ Usage

Once inside the Netsploit prompt:

| Command | Description |
|---------|-------------|
| `use <module>` | Load and run a module (e.g. `use port-scanner`) |
| `auto` | Automated mode — scan the network then run a chosen module on a target |
| `modules` | List all available modules |
| `shell` | Run an arbitrary shell command without leaving Netsploit |
| `help` | Show help information |
| `clear` | Clear the screen |
| `exit` | Exit Netsploit |

**Example workflow:**

```
netsploit > use network-scanner     # find devices on the network
netsploit > use port-scanner        # scan a specific target for open ports
netsploit > use vuln-scanner        # check that target for vulnerabilities
```

Or use `auto` to do all of the above in a guided flow.

---

## 📄 Credits

- `oui.txt` (OUI Lookup Database) — sourced from the [Wireshark project](https://www.wireshark.org/download/automated/data/manuf). Not created by or owned by this project.
