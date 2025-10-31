import pyautogui
import time
from PIL import ImageGrab, Image
import keyboard  # For emergency stop

# Coordinates for the game area (adjust based on your screen resolution)
# Use a tool like `pyautogui.mouseInfo()` to find the correct coordinates
GAME_REGION = (400, 400, 1000, 500)  # (left, top, right, bottom)

# Color of the obstacle (black in this case)
OBSTACLE_COLOR = (83, 83, 83)

# Debugging: Set to True to visualize the game region and obstacle detection
DEBUG = True

# Function to check for obstacles
def detect_obstacle():
    # Capture the game region
    screenshot = ImageGrab.grab(bbox=GAME_REGION)
    if DEBUG:
        screenshot.save("debug_screenshot.png")  # Save screenshot for debugging

    pixels = screenshot.load()

    # Check a specific line for obstacles (adjust the Y coordinate as needed)
    for x in range(GAME_REGION[2] - GAME_REGION[0]):
        if pixels[x, 50] == OBSTACLE_COLOR:  # Check if pixel is black (obstacle)
            if DEBUG:
                print(f"Obstacle detected at x={x}")
            return True
    return False

# Function to jump
def jump():
    pyautogui.press('space')
    time.sleep(0.1)  # Small delay to avoid double jumps

# Main game loop
def play_game():
    print("Starting the game in 3 seconds...")
    time.sleep(3)

    # Press space to start the game
    jump()

    while True:
        if detect_obstacle():
            jump()
            print("Jumped!")

        # Emergency stop (press 'q' to quit)
        if keyboard.is_pressed('q'):
            print("Game stopped.")
            break

# Run the game
if __name__ == "__main__":

    print("Move your mouse to the top-left corner of the game area and press Enter.")
    input()
    top_left = pyautogui.position()
    print("Move your mouse to the bottom-right corner of the game area and press Enter.")
    input()
    bottom_right = pyautogui.position()
    print(f"GAME_REGION = ({top_left.x}, {top_left.y}, {bottom_right.x}, {bottom_right.y})")
    play_game()