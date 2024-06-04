import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
from input_handler import get_input

def show_image(img, title="Image", show=True):
    """Utility function to display an image with matplotlib if show is True."""
    if show:
        plt.figure(figsize=(8, 8))
        plt.imshow(cv2.cvtColor(img, cv8.COLOR_BGR2RGB))
        plt.title(title)
        plt.axis('off')
        plt.show()

def bend_image(image, bend_factor, direction='down', show_steps=True):
    """Applies an upward or downward bending effect to the image."""
    height, width, _ = image.shape
    bent_img = np.zeros_like(image)
    for y in range(height):
        for x in range(width):
            if direction == 'down':
                new_y = int(y + bend_factor * x * (width - x) / width)
            else:
                new_y = int(y - bend_factor * x * (width - x) / width)
            if 0 <= new_y < height:
                bent_img[new_y, x] = image[y, x]
    show_image(bent_img, f"Bent {'upward' if direction == 'up' else 'downward'} with factor {bend_factor}", show_steps)
    return bent_img

def add_layer(image, current_height, thickness, last_color, colors, show_steps=True):
    """Adds a colored layer with a 1-pixel black border and shows the image."""
    color = random.choice([c for c in colors if c != last_color])
    start_y = max(0, current_height - thickness)
    cv2.rectangle(image, (0, start_y), (width, current_height), color, -1)
    cv2.rectangle(image, (0, start_y), (width, current_height), (0, 0, 0), 1)
    show_image(image, f"Added layer from {start_y} to {current_height} with color {color}", show_steps)
    return start_y, color

def apply_rotation(image, current_height, show_steps=True):
    """Applies a rotation without reverting and adjusts y based on the rotation."""
    angle = random.choice([random.uniform(15, 25), random.uniform(25, 35)])
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (width, height))
    show_image(rotated, f"Rotated permanently by {angle} degrees", show_steps)
    if 15 <= angle < 25:
        y_adjustment = 100
    else:
        y_adjustment = 150
    return rotated, y_adjustment

def add_fault(image, angle, offset, current_height, show_steps=True):
    """Simulates a geological fault in the image."""
    center = (width // 2, current_height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    faulted = cv2.warpAffine(image, matrix, (width, current_height))
    show_image(faulted, f"Applied fault at angle {angle} degrees with offset {offset}", show_steps)
    if angle < 180:
        return faulted, offset
    else:
        return faulted, -offset

def create_image(display_mode):
    global width, height  # Define these as global if they are modified or used across functions
    height, width = 1000, 1000
    image = np.zeros((height, width, 3), dtype=np.uint8)
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
    current_height = height
    last_color = None
    bend_occurred = False
    fault_occurred = False

    first_layer_thickness = random.randint(270, 300)
    current_height, last_color = add_layer(image, current_height, first_layer_thickness, last_color, colors, display_mode == 1)

    while current_height > 300:
        thickness = random.randint(25, 75)
        if current_height - thickness < 300:
            thickness = current_height - 300
        current_height, last_color = add_layer(image, current_height, thickness, last_color, colors, display_mode == 1)

        if not bend_occurred and random.random() < 0.1:
            bend_factor = random.uniform(0.1, 0.3)
            direction = 'up' if random.choice([True, False]) else 'down'
            image = bend_image(image, bend_factor, direction, display_mode == 1)
            bend_occurred = True

        if not fault_occurred and random.random() < 0.1:
            angle = random.choice([random.uniform(15, 35), random.uniform(325, 345)])
            offset = random.randint(15, 50)
            image, offset_adjustment = add_fault(image, angle, offset, current_height, display_mode == 1)
            current_height += offset_adjustment
            fault_occurred = True

        if random.random() < 0.1:
            image, rotation_adjustment = apply_rotation(image, current_height, display_mode == 1)
            current_height += rotation_adjustment

    if display_mode == 2:
        # Crop to 500x500 at the center
        center_x, center_y = width // 2, height // 2
        cropped_img = image[center_y-250:center_y+250, center_x-250:center_x+250]
        show_image(cropped_img, "Final Cropped Image", True)

if __name__ == "__main__":
    display_mode = get_input()
    create_image(display_mode)
