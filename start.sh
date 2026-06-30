#!/bin/sh
set -e

cd "$(dirname "$0")"

if [ ! -d venv ]; then
    echo "Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

. venv/bin/activate
python main.py
