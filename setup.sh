#!/bin/sh
set -e

cd "$(dirname "$0")"

for candidate in python3.12 python3.11 python3.10 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
        PYTHON="$candidate"
        break
    fi
done

if [ -z "$PYTHON" ]; then
    echo "Python 3.10+ is required but was not found."
    echo "On Raspberry Pi OS, install it with:"
    echo "  sudo apt update"
    echo "  sudo apt install python3.11 python3.11-venv python3-pip"
    exit 1
fi

"$PYTHON" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' || {
    echo "$PYTHON is $( "$PYTHON" --version ). Python 3.10+ is required."
    exit 1
}

echo "Using $("$PYTHON" --version)"

rm -rf venv
"$PYTHON" -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. Run ./start.sh to start."
echo "See docs/SETUP.md for troubleshooting and optional systemd setup."
