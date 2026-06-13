import pyautogui
import os
from PIL import Image, ImageChops
import io

last_screenshot = None

def screen_changed(threshold=0.02):
    global last_screenshot
    
    # Take current screenshot
    current = pyautogui.screenshot()
    current = current.resize((640, 360))
    
    # First run — always scan
    if last_screenshot is None:
        last_screenshot = current
        return True
    
    # Compare current vs last screenshot
    diff = ImageChops.difference(current, last_screenshot)
    pixels = list(diff.getdata())
    total_pixels = len(pixels)
    changed_pixels = sum(1 for p in pixels if sum(p) > 30)
    change_ratio = changed_pixels / total_pixels
    
    print(f"Screen change: {change_ratio:.2%}")
    
    if change_ratio > threshold:
        last_screenshot = current
        return True
    
    return False

if __name__ == "__main__":
    import time
    print("Watching for screen changes... (move your mouse or open something)")
    while True:
        if screen_changed():
            print("Screen changed! Would trigger scan.")
        else:
            print("No change. Skipping scan.")
        time.sleep(5)
