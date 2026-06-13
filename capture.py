import pyautogui
import os
from datetime import datetime

def take_screenshot():
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/screenshot_{timestamp}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")
    return filename

if __name__ == "__main__":
    path = take_screenshot()
    print(f"Success! File saved at: {path}")
