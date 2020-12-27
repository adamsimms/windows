FROM hypriot/rpi-python


COPY main.py ./
COPY weather_data.py ./
COPY requirements.txt ./
RUN pip install -r requirements.txt

