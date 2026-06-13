from core.capture import take_screenshot
from core.analyzer import analyze_screenshot
from core.database import init_db, save_scan
from core.alerts import send_alert
from core.trigger import screen_changed
import time

def run_scan():
    print("\n--- Running scan ---")
    image_path = take_screenshot()
    result = analyze_screenshot(image_path)
    save_scan(image_path, result)
    send_alert(result["threat_level"], result["description"])
    print("Scan complete!")
    return result

if __name__ == "__main__":
    init_db()
    print("SentinelEye started! Press Ctrl+C to stop.")
    while True:
        if screen_changed():
            run_scan()
        else:
            print("No change detected. Skipping scan.")
        time.sleep(10)
