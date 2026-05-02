#!/usr/bin/env bash
# setup.sh — Run this once after cloning to prepare your environment.
# After setup, launch netsploit with: python3 netsploit.py

set -e  # Exit on error

# Colors for output (using ANSI codes, no external dependency)
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
NC=$'\033[0m'  # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Helper functions
print_header() {
    echo "${BLUE}═══════════════════════════════════════${NC}"
    echo "${BLUE}$1${NC}"
    echo "${BLUE}═══════════════════════════════════════${NC}"
}

print_ok() {
    echo "${GREEN}[✓]${NC} $1"
}

print_warn() {
    echo "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo "${RED}[✗]${NC} $1"
}

# Check Python installation
check_python() {
    print_header "Checking Python Installation"

    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_ok "Python 3 found: $PYTHON_VERSION"
        return 0
    else
        print_error "Python 3 is not installed"
        echo "Please install Python 3.8 or higher:"
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-venv"
        echo "  Fedora:        sudo dnf install python3 python3-pip"
        echo "  macOS:         brew install python3"
        echo "  Windows:       https://www.python.org/downloads/"
        return 1
    fi
}

# Check system dependencies (nmap, hping3)
check_system_deps() {
    print_header "Checking System Dependencies"

    local missing_deps=()

    # Check nmap (required for most scanning modules)
    if command -v nmap &> /dev/null; then
        NMAP_VERSION=$(nmap --version 2>&1 | head -1)
        print_ok "nmap found: $NMAP_VERSION"
    else
        print_warn "nmap is not installed (required for all scan modules)"
        missing_deps+=("nmap")
    fi

    # Check hping3 (only used by the DoS module; Linux/macOS only)
    if command -v hping3 &> /dev/null; then
        print_ok "hping3 found"
    else
        print_warn "hping3 is not installed (only needed for the DoS module — Linux/macOS only)"
        missing_deps+=("hping3")
    fi

    # Report missing deps with platform-appropriate install instructions
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        print_warn "Missing system dependencies: ${missing_deps[*]}"
        echo ""
        echo "Installation instructions:"
        echo "  Ubuntu/Debian: sudo apt-get install nmap hping3"
        echo "  Fedora:        sudo dnf install nmap hping3"
        echo "  macOS:         brew install nmap hping3"
        echo "  Windows:       https://nmap.org/download.html  (hping3 not available on Windows)"
        echo ""
        read -p "Continue setup without these tools? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi

    return 0
}

# Setup Python virtual environment
setup_venv() {
    print_header "Setting Up Python Virtual Environment"

    if [ -d "$SCRIPT_DIR/.venv" ]; then
        print_ok "Virtual environment already exists"
    else
        print_warn "Creating virtual environment..."
        python3 -m venv "$SCRIPT_DIR/.venv"
        print_ok "Virtual environment created"
    fi

    source "$SCRIPT_DIR/.venv/bin/activate"
    print_ok "Virtual environment activated"
    return 0
}

# Install pip dependencies
install_pip_deps() {
    print_header "Installing Python Dependencies"

    if [ ! -f "$SCRIPT_DIR/requirements.txt" ]; then
        print_error "requirements.txt not found"
        return 1
    fi

    print_warn "Installing dependencies from requirements.txt..."
    python3 -m pip install --upgrade pip > /dev/null 2>&1 || true
    python3 -m pip install -r "$SCRIPT_DIR/requirements.txt"
    print_ok "Python dependencies installed"
    return 0
}

# Create log directories
setup_log_dirs() {
    print_header "Setting Up Log Directories"

    LOG_DIR="$SCRIPT_DIR/logs"

    if [ ! -d "$LOG_DIR" ]; then
        mkdir -p "$LOG_DIR"
        print_ok "Created logs directory: $LOG_DIR"
    else
        print_ok "Logs directory already exists: $LOG_DIR"
    fi

    local module_dirs=(
        "device-info"
        "os-guesser"
        "port-scanner"
        "network-scanner"
        "ping"
        "oui-lookup"
        "vuln-scanner"
        "dos"
    )

    for module_dir in "${module_dirs[@]}"; do
        mkdir -p "$LOG_DIR/$module_dir"
    done

    print_ok "Log subdirectories are ready"
    return 0
}

# Main execution
main() {
    echo ""
    print_header "NetSploit Setup"
    echo ""

    if ! check_python; then
        return 1
    fi
    echo ""

    if ! check_system_deps; then
        return 1
    fi
    echo ""

    if ! setup_venv; then
        return 1
    fi
    echo ""

    if ! install_pip_deps; then
        return 1
    fi
    echo ""

    if ! setup_log_dirs; then
        return 1
    fi

    echo ""
    print_header "Setup Complete"
    echo ""
    echo "  ${GREEN}To run netsploit:${NC}"
    echo ""
    echo "    ${YELLOW}source .venv/bin/activate${NC}"
    echo "    ${YELLOW}python3 netsploit.py${NC}"
    echo ""
}

main
