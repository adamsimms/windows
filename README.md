# windows

Raspberry Pi servo controller driven by live weather data from SmartAtlantic.

## Requirements

- Raspberry Pi with GPIO access
- Python 3.10 or newer
- Raspberry Pi OS Bookworm (or another distro with Python 3.10+)

## Setup on the Pi

Install Python 3.11 if your system Python is older than 3.10:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

Clone the repo, create a fresh virtual environment, and install dependencies:

```bash
git pull
cd ~/windows
chmod +x setup.sh start.sh
./setup.sh
```

Run the controller:

```bash
./start.sh
```

If you previously used the old Python 3.7 virtual environment, `setup.sh` removes it and recreates `venv/` with a supported Python version.

## Docker

Build for the Pi (64-bit OS):

```bash
docker build --platform linux/arm64 -t windows .
```

Build for 32-bit Raspberry Pi OS:

```bash
docker build --platform linux/arm/v7 -t windows .
```

GPIO access requires running the container in privileged mode or passing the GPIO device:

```bash
docker run --rm --privileged windows
```

## Weather data

`weather_data.py` fetches data in the background and writes it to `data.txt`. `main.py` reads that file to drive the servo.
