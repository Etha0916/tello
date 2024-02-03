import cv2
import numpy as np
from djitellopy import Tello
import keyboard

# Initialize Tello
tello = Tello()
tello.connect()
tello.streamon()

# Set the keyboard control mapping
key_mapping = {
    'w': (0, 40, 0, 0),    # Move forward at speed 20
    's': (0, -40, 0, 0),   # Move backward at speed 20
    'a': (-20, 0, 0, 0),   # Move left at speed 20
    'd': (20, 0, 0, 0),    # Move right at speed 20
    'q': (0, 0, 0, 80),    # Rotate counter-clockwise at speed 20
    'e': (0, 0, 0, -80),   # Rotate clockwise at speed 20
    'up': (0, 0, 20, 0),   # Fly up at speed 20
    'down': (0, 0, -20, 0), # Fly down at speed 20
    'left': (0, -20, 0, 0), # Fly left at speed 20
    'right': (0, 20, 0, 0), # Fly right at speed 20
    'z': (0, 0, 0, 0),  # Hover in place
    'l': 'altitude',       # Set altitude to 60cm
    'k': 'land',           # Land
    'x': 'stop',           # Stop flying
    'y': 'auto',           # Enable obstacle avoidance mode
}

# Obstacle detection distance threshold (in cm)
obstacle_distance_threshold = 50

# Flag to indicate if the obstacle avoidance mode is enabled
obstacle_avoidance_enabled = False

# Flag to indicate if the drone is in the air
is_flying = False

# Keyboard control loop
while True:
    key = keyboard.read_key()

    # If the key is in the key mapping
    if key in key_mapping:
        # If it's a movement command
        if isinstance(key_mapping[key], tuple):
            dx, dy, dz, dr = key_mapping[key]
            if not obstacle_avoidance_enabled and is_flying:
                tello.send_rc_control(dx, dy, dz, dr)
        # If it's a special command (e.g., takeoff, land, stop, auto)
        else:
            command = key_mapping[key]
            if command == 'altitude':
                if not is_flying:
                    tello.takeoff()
                    is_flying = True
                    tello.move_up(60)
            elif command == 'land':
                tello.land()
                is_flying = False
            elif command == 'stop':
                tello.send_rc_control(0, 0, 0, 0)
            elif command == 'auto':
                obstacle_avoidance_enabled = True

    # If the obstacle avoidance mode is enabled
    if obstacle_avoidance_enabled:
        # Read the current frame from Tello
        frame = tello.get_frame_read().frame

        # Perform obstacle detection (using your own obstacle detection code)
        # ...

        # If an obstacle is detected within the threshold distance
        if obstacle_detected:
            # Turn around
            tello.rotate_clockwise(180)

            # Continue flying straight until another obstacle is encountered
            while True:
                # Read the current frame from Tello
                frame = tello.get_frame_read().frame

                # Perform obstacle detection (using your own obstacle detection code)
                # ...

                # If another obstacle is detected, break the loop
                if obstacle_detected:
                    break

                # Fly forward
                tello.move_forward(20)

            # Turn around again
            tello.rotate_clockwise(180)

        # Fly forward
        tello.move_forward(20)

    # If the 'x' key is pressed, stop flying
    if key == 'x':
        tello.send_rc_control(0, 0, 0, 0)
        is_flying = False

    # If the 'y' key is pressed, enable obstacle avoidance mode
    if key == 'y':
        obstacle_avoidance_enabled = True

    # If the 'Esc' key is pressed, exit the loop
    if key == 'esc':
        break

# Close all windows and disconnect from Tello
cv2.destroyAllWindows()
tello.streamoff()
tello.disconnect()
