# Setup guide

This project runs on a Raspberry Pi and controls a servo using live weather data.

## Prerequisites

- Raspberry Pi with GPIO header wired to your servo
- Raspberry Pi OS Bookworm (or another Linux distro with Python 3.10+)
- Network access for weather data fetches

## 1. Install Python 3.10+

Check your current version:

```bash
python3 --version
```

If the version is below 3.10, install Python 3.11 on Raspberry Pi OS:

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

## 2. Get the code

Clone the repository (first time):

```bash
git clone https://github.com/adamsimms/windows.git ~/windows
```

Or pull the latest changes:

```bash
cd ~/windows
git pull
```

## 3. Create the virtual environment

From the project directory:

```bash
cd ~/windows
chmod +x setup.sh start.sh
./setup.sh
```

`setup.sh` will:

1. Find the newest available Python 3.10+ interpreter
2. Remove any existing `venv/` directory
3. Create a fresh virtual environment
4. Install dependencies from `requirements.txt`

## 4. Run the application

```bash
./start.sh
```

`start.sh` activates `venv/` and runs `main.py`.

To fetch weather data separately:

```bash
source venv/bin/activate
python weather_data.py
```

## Upgrading an existing install

After pulling new changes:

```bash
cd ~/windows
git pull
./setup.sh
```

Run `./setup.sh` whenever `requirements.txt` changes so your virtualenv stays in sync.

## Docker setup

Build the image on the Pi or cross-build from another machine:

```bash
# 64-bit Pi OS
docker build --platform linux/arm64 -t windows .

# 32-bit Pi OS
docker build --platform linux/arm/v7 -t windows .
```

Run with GPIO access:

```bash
docker run --rm --privileged windows
```

## Troubleshooting

### `Python 3.10+ is required but was not found`

Install a newer Python as shown in step 1, then rerun `./setup.sh`.

### `Virtual environment not found`

Run `./setup.sh` before `./start.sh`.

### `No module named 'RPi'`

Dependencies were not installed in the active environment. Run `./setup.sh` again from the project root.

### `pip install` fails on `RPi.GPIO`

`RPi.GPIO` must be installed on the Raspberry Pi itself. It does not build on non-Pi architectures.

### Permission errors on GPIO

Run as a user in the `gpio` group, or use `sudo` only if required by your OS configuration:

```bash
sudo usermod -aG gpio "$USER"
# log out and back in
```

## Systemd service (optional)

To run at boot, create `/etc/systemd/system/windows.service`:

```ini
[Unit]
Description=Windows weather servo controller
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/windows
ExecStart=/home/pi/windows/start.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable windows
sudo systemctl start windows
```
