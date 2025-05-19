import requests
import platform
import subprocess
import json
import os
import schedule
import time

STATE_FILE = 'state.json'

def check_disk_encryption():
    system = platform.system()
    if system == "Windows":
        try:
            result = subprocess.getoutput('manage-bde -status')
            if "Percentage Encrypted" in result:
                return True
            else:
                return False
        except Exception as e:
            return f"Error: {e}"
    return "Not implemented"

def check_os_update_status():
    system = platform.system()
    if system == "Windows":
        try:
            result = subprocess.getoutput(
                'powershell -Command "(New-Object -ComObject Microsoft.Update.AutoUpdate).Results"'
            )
            if "Succeeded" in result or "NotStarted" in result:
                return "Up to date"
            elif "InProgress" in result:
                return "Updates in progress"
            else:
                return "Might be outdated"
        except Exception as e:
            return f"Error: {e}"
    return "Not implemented"

def check_antivirus_status():
    system = platform.system()
    if system == "Windows":
        try:
            result = subprocess.getoutput(
                'powershell -Command "Get-MpComputerStatus | Select-Object -Property AMServiceEnabled, RealTimeProtectionEnabled"'
            )
            if "True" in result:
                return "Antivirus running"
            else:
                return "Antivirus not active"
        except Exception as e:
            return f"Error: {e}"
    return "Not implemented"

def check_sleep_settings():
    system = platform.system()
    if system == "Windows":
        try:
            # Get the sleep timeout for AC power
            result = subprocess.getoutput(
                'powershell -Command "powercfg -query SCHEME_CURRENT SUB_SLEEP STANDBYIDLE"'
            )

            # Extract value using regex or simple parse
            for line in result.splitlines():
                if "Power Setting Index" in line:
                    try:
                        hex_value = line.strip().split()[-1]
                        minutes = int(hex_value, 16) // 60  # convert from seconds to minutes
                        if minutes <= 10:
                            return f"Sleep OK ({minutes} min)"
                        else:
                            return f"Sleep exceeds 10 min ({minutes} min)"
                    except:
                        return "Could not parse sleep value"
            return "Sleep setting not found"
        except Exception as e:
            return f"Error: {e}"
    return "Not implemented"


def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_current_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=4)

def states_differ(old_state, new_state):
    return old_state != new_state

def main():
    current_state = {
        "disk_encryption": check_disk_encryption(),
        "os_update": check_os_update_status(),
        "antivirus": check_antivirus_status(),
        "sleep_settings": check_sleep_settings()
    }

    # Send to backend (inside main and after current_state creation)
    try:
        payload = {
            "device_id": "device_001",  
            **current_state
        }
        print("Payload to send:", payload)

        response = requests.post("http://127.0.0.1:5000/report", json=payload)
        if response.status_code == 200:
            print("✅ Report sent to backend successfully.")
        else:
            print(f"❌ Failed to send report. Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Error sending report: {e}")

    previous_state = load_previous_state()

    if states_differ(previous_state, current_state):
        print("⚠️ Change detected! (This is where you'd send the report)")
        save_current_state(current_state)
    else:
        print("✅ No change detected.")

    print("\nCurrent System State:")
    for key, value in current_state.items():
        print(f"{key}: {value}")
        
def job():
    print("\n🕒 Running scheduled system health check...")
    main()

if __name__ == "__main__":
    main()
    # Schedule the job every 15 minutes
    schedule.every(15).minutes.do(job)

    print("Scheduler started. Running every 15 minutes...")

    while True:
        schedule.run_pending()
        time.sleep(1)
