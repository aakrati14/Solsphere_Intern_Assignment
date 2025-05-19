import json

state = {
    "disk_encryption": False,
    "os_update": "Might be outdated",
    "antivirus": "Antivirus running",
    "sleep_settings": "Sleep disabled"
}

with open("state.json", "w") as f:
    json.dump(state, f, indent=4)
