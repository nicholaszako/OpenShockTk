# OpenShockTk

A small tkinter-based Python app for controlling your OpenShock devices

## Features

### Controller

Send stop, vibrate, and shock signals with varying duration and intensity.

### Patterns

Want to send multiple control messages with one click? Use JSON to create your own pattern in the patterns directory. Each file will show up as a button on the app.

Here's an example pattern:
```json
[
    {
        "request": {
            "id": "123",
            "type_": "Vibrate",
            "intensity": 20,
            "duration": 1000
        },
        "sleep": 2000
    },
    {
        "request": {
            "id": "123",
            "type_": "Vibrate",
            "intensity": 30,
            "duration": 1000
        },
        "sleep": 2000
    },
    {
        "request": {
            "id": "123",
            "type_": "Vibrate",
            "intensity": 50,
            "duration": 1000
        },
        "sleep": 2000
    }
]
```
This pattern will vibrate device `123` every 2 seconds at an increasing intensity

**Values**
- `id`: your device ID
- `type_`: `Stop`, `Shock`, or `Vibrate`
- `intensity`: 0 - 100
- `duration`: 300 - 65536 ms
- `sleep`: ms until next message is sent

## Requirements
- Python3
- Tk

## Installation

### Linux

```
git clone https://github.com/nicholaszako/OpenShockTk
cd OpenShockTk
chmod +x ./start.sh
./start.sh
```

### Windows

```
git clone https://github.com/nicholaszako/OpenShockTk
cd OpenShockTk
python3 .venv venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python -m main
```
