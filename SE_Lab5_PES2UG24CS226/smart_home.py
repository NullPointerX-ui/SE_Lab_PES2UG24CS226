"""Smart home device controller.

Keeps a register of smart devices, switches them on and off, sets the
thermostat within a safe range, lists devices by room, reports power use
and saves the home state to a JSON file.

Cleaned up for Lab 5 (Static Code Analysis) by Khush Bhardwaj,
SRN PES2UG24CS226.
"""

import json
import os
import subprocess
from pathlib import Path

HUB_HOST = "127.0.0.1"
HUB_PORT = 8080
POWER_USAGE = {"light": 10, "fan": 60, "thermostat": 1500, "tv": 120}
HUB_AUTH_ENV = "SMARTHOME_HUB_PASSWORD"
SCENES_DIR = Path(__file__).resolve().parent / "scenes"
MIN_TEMPERATURE = 16
MAX_TEMPERATURE = 30

devices = {}


def hub_password():
    """Return the hub password from the environment, or None if unset."""
    return os.environ.get(HUB_AUTH_ENV)


def add_device(device_name, kind, room="Living Room", settings=None):
    """Register a device and return its record.

    `settings` defaults to None so that every device gets a fresh
    dictionary of its own.
    """
    devices[device_name] = {
        "kind": kind,
        "room": room,
        "on": False,
        "settings": dict(settings) if settings else {},
    }
    return devices[device_name]


def toggle_device(device_name):
    """Flip a device on or off and return its new state, or None if unknown."""
    if device_name not in devices:
        print("Device not found:", device_name)
        return None
    devices[device_name]["on"] = not devices[device_name]["on"]
    return devices[device_name]["on"]


def set_temperature(device_name, value):
    """Set a thermostat to `value`, clamped to the safe range.

    Returns True on success and False if the device is unknown or is not
    a thermostat.
    """
    device = devices.get(device_name)
    if device is None:
        print("Device not found:", device_name)
        return False
    if device["kind"] != "thermostat":
        print(device_name, "is not a thermostat")
        return False
    device["settings"]["temperature"] = min(
        max(value, MIN_TEMPERATURE), MAX_TEMPERATURE
    )
    return True


def devices_in_room(room):
    """Return the names of every device registered in `room`."""
    return [name for name, info in devices.items() if info["room"] == room]


def power_usage():
    """Return the total power draw, in watts, of the devices switched on."""
    active = [info for info in devices.values() if info["on"]]
    return sum(POWER_USAGE.get(info["kind"], 0) for info in active)


def save_state(file_name="home_state.json"):
    """Write the current device register to `file_name` as JSON."""
    with open(file_name, "w", encoding="utf-8") as handle:
        json.dump(devices, handle, indent=2)


def hub_address():
    """Return the hub address as 'host:port'."""
    return f"{HUB_HOST}:{HUB_PORT}"


def run_scene(scene_script):
    """Run a scene script from the scenes directory.

    The script name is resolved inside SCENES_DIR and the command is run
    without a shell, so a crafted name cannot inject extra commands.
    """
    script_path = (SCENES_DIR / scene_script).resolve()
    if SCENES_DIR not in script_path.parents or not script_path.is_file():
        print("Unknown scene:", scene_script)
        return False
    subprocess.run(["/bin/bash", str(script_path)], check=False, shell=False)
    return True


def main():
    """Run a short demonstration of the controller."""
    add_device("Ceiling Light", "light")
    add_device("Bedroom Fan", "fan", "Bedroom")
    add_device("Thermostat", "thermostat", "Bedroom")
    add_device("Smart TV", "tv")
    toggle_device("Ceiling Light")
    toggle_device("Thermostat")
    toggle_device("Garage Door")
    set_temperature("Thermostat", 35)
    set_temperature("Ceiling Light", 20)
    print("Bedroom devices:", devices_in_room("Bedroom"))
    print("Current power use (W):", power_usage())
    print("Hub address:", hub_address())  # for app setup
    print("Light settings:", devices["Ceiling Light"]["settings"])
    print("Thermostat settings:", devices["Thermostat"]["settings"])
    print(
        "Devices on:",
        [name for name, info in devices.items() if info["on"]],
    )
    save_state()


if __name__ == "__main__":
    main()
