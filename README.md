# windows

Raspberry Pi servo controller driven by live weather data from [SmartAtlantic](https://www.smartatlantic.ca/).

## Quick start

On the Pi, after cloning or pulling this repo:

```bash
cd ~/windows
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

See [docs/SETUP.md](docs/SETUP.md) for full setup, upgrade, and troubleshooting instructions.

## Requirements

- Raspberry Pi with GPIO access
- Python 3.10 or newer
- Raspberry Pi OS Bookworm (or another distro with Python 3.10+)

## Project layout

| File | Purpose |
|------|---------|
| `main.py` | Reads weather data and drives the servo via GPIO |
| `weather_data.py` | Fetches weather from SmartAtlantic and writes `data.txt` |
| `setup.sh` | Creates a Python 3.10+ virtualenv and installs dependencies |
| `start.sh` | Activates the virtualenv and runs `main.py` |
| `requirements.txt` | Pinned Python dependencies |
| `Dockerfile` | Container image for Pi deployments |

## Docker

Build for 64-bit Raspberry Pi OS:

```bash
docker build --platform linux/arm64 -t windows .
```

Build for 32-bit Raspberry Pi OS:

```bash
docker build --platform linux/arm/v7 -t windows .
```

GPIO access requires privileged mode or passing the GPIO device:

```bash
docker run --rm --privileged windows
```

## Dependencies

Security-sensitive HTTP libraries (`requests`, `urllib3`, `certifi`, `idna`) are pinned to current releases and require Python 3.10+. Run `./setup.sh` after pulling dependency updates to refresh your local `venv/`.
