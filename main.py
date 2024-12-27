import webbrowser
import time
import pyautogui
from PIL import ImageGrab
import numpy as np
import cv2  # Import OpenCV
# Import OpenCV
# Configuration (Adjust these values as needed)
CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"  # Windows Chrome path
GAME_URL = "https://elgoog.im/dinosaur-game/"
OBSTACLE_THRESHOLD = 20  # Lower values detect more obstacles
BIRD_THRESHOLD = 15 # Lower values detect more birds
OBSTACLE_AREA = (100, 300, 900, 600)  # (left, top, right, bottom) - Adjust for your screen
OBSTACLE_ROI = (400, 100, 200, 100) # (x, y, width, height) Region of Interest for obstacles
BIRD_ROI = (400, 50, 200, 100) # (x, y, width, height) Region of Interest for birds

def open_game():
    """Opens the Dinosaur game in the browser."""
    try:
        webbrowser.get(CHROME_PATH).open(GAME_URL)
    except webbrowser.Error:
        print("Chrome path not found. Trying default browser...")
        webbrowser.open(GAME_URL)
    time.sleep(5)  # Wait for the game to load
    pyautogui.press("space")  # Start the game
    print("Game started. Ready to detect obstacles...")

def detect_obstacles():
    """Continuously captures screenshots and detects obstacles."""
    try:
        while True:
            # Capture the screen (using configured area)
            screen = ImageGrab.grab(bbox=OBSTACLE_AREA)
            screen_np = np.array(screen)
            gray = cv2.cvtColor(screen_np, cv2.COLOR_BGR2GRAY) #convert to grayscale

            # Detect obstacles (cacti)
            obstacle_x, obstacle_y, obstacle_w, obstacle_h = OBSTACLE_ROI
            obstacle_area = gray[obstacle_y:obstacle_y+obstacle_h, obstacle_x:obstacle_x+obstacle_w]
            if (obstacle_area < OBSTACLE_THRESHOLD).any():
                pyautogui.press("space")
                print("Obstacle detected: Jump!")

            # Detect birds
            bird_x, bird_y, bird_w, bird_h = BIRD_ROI
            bird_area = gray[bird_y:bird_y+bird_h, bird_x:bird_x+bird_w]
            if (bird_area < BIRD_THRESHOLD).any():
                pyautogui.press("down")  # Duck (or any other action)
                print("Bird detected: Duck!")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("Exiting the game bot gracefully.")

if __name__ == "__main__":
    open_game()
    detect_obstacles()