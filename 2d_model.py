import cv2
import numpy as np
import random
from matplotlib import pyplot as plt

def show_image(img, title="Image"):
    plt.figure(figsize=(12, 7))
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def add_text(img, text, position, font_scale=0.7, color=(0, 0, 0), thickness=2):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, text, position, font, font_scale, color, thickness, cv2.LINE_AA)

def bend_image(image, bend_factor, direction='down'):
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
    return bent_img

def add_layer(image, current_height, thickness, last_color, colors):
    color = random.choice([c for c in colors if c != last_color])
    start_y = max(0, current_height - thickness)
    cv2.rectangle(image, (0, start_y), (width, current_height), color, -1)
    cv2.rectangle(image, (0, start_y), (width, current_height), (0, 0, 0), 1)
    return start_y, color

def add_fault(image, angle, offset, current_height):
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (width, height))
    split = width // 2
    rotated[:, split:] = np.roll(rotated[:, split:], offset, axis=0)
    cv2.line(rotated, (split, 0), (split, height), (0, 0, 0), 2)
    matrix = cv2.getRotationMatrix2D(center, -angle, 1.0)
    faulted = cv2.warpAffine(rotated, matrix, (width, height))
    return faulted, offset

def apply_rotation(image, current_height, rotation_occurred):
    if rotation_occurred:
        return image, 0, rotation_occurred
    angle = random.choice([random.uniform(15, 25), random.uniform(25, 35)])
    center = (width // 2, height // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (width, height))
    rotation_occurred = True
    y_adjustment = 100 if 15 <= angle < 25 else 150
    return rotated, y_adjustment, rotation_occurred

def add_intrusion(image, current_height):
    buffer_width = random.randint(25, 50)
    intrusion_start_x = random.randint(350, 650)
    cv2.line(image, (intrusion_start_x, height), (intrusion_start_x, current_height), (0, 0, 255), 3)
    left_limit = max(0, intrusion_start_x - buffer_width)
    right_limit = min(width, intrusion_start_x + buffer_width)
    buffer_color = (0, 0, 255)  # Red color for intrusion
    cv2.rectangle(image, (left_limit, current_height), (right_limit, height), buffer_color, cv2.FILLED)
    extended_left = max(0, left_limit - 10)
    extended_right = min(width, right_limit + 10)
    for y in range(current_height, height, 25):
        cv2.line(image, (extended_left, y), (extended_right, y), buffer_color, 1)
    return image

def draw_intrusion_symbol(image, x, y, width, height):
    buffer_color = (0, 0, 255)  # Red color for intrusion
    symbol_width = height // 2  # Half width of the height
    x_center = x + (width - symbol_width) // 2  # Center the symbol horizontally
    
    # Draw the main rectangle
    cv2.rectangle(image, (x_center, y), (x_center + symbol_width, y + height), buffer_color, cv2.FILLED)
    cv2.rectangle(image, (x_center, y), (x_center + symbol_width, y + height), (0, 0, 0), 1)  # Black border
    
    # Add red horizontal lines
    line_spacing = height // 5
    line_width = symbol_width * 2  # Twice the symbol width
    line_x_start = x_center - (line_width - symbol_width) // 2  # Center the lines
    for i in range(1, 5):
        cv2.line(image, (line_x_start, y + i * line_spacing), 
                 (line_x_start + line_width, y + i * line_spacing), 
                 buffer_color, 1)

# Initialize the image and colors
height, width = 1000, 1000
image = np.zeros((height, width, 3), dtype=np.uint8)
colors = [(150, 111, 214), (0, 255, 0), (0, 255, 255), (255, 255, 0)]  # Pink, Green, Cyan, Yellow

color_to_rock = {
    (255, 255, 0): "limestone",    # Yellow
    (0, 255, 255): "sandstone",    # Cyan
    (0, 255, 0): "siltstone",      # Green
    (150, 111, 214): "breccia"  # Pink
}

current_height = height
last_color = None
bend_occurred = False
fault_occurred = False
rotation_occurred = False
events = []

# Apply first layer
first_layer_thickness = random.randint(270, 300)
current_height, last_color = add_layer(image, current_height, first_layer_thickness, last_color, colors)
events.append(f"Added first layer of {color_to_rock[last_color]} with thickness {first_layer_thickness}")

# Main simulation loop
layer_count = 1
while current_height > 300:
    thickness = random.randint(25, 75)
    if current_height - thickness < 300:
        thickness = current_height - 300
    current_height, last_color = add_layer(image, current_height, thickness, last_color, colors)
    layer_count += 1
    events.append(f"Added layer of {color_to_rock[last_color]} with thickness {thickness}")

    if not bend_occurred and random.random() < 0.1:
        bend_factor = random.uniform(0.1, 0.3)
        direction = 'up' if random.choice([True, False]) else 'down'
        image = bend_image(image, bend_factor, direction)
        bend_occurred = True
        current_height += 50 if direction == 'up' else +75
        events.append(f"Applied {direction}ward bend with factor {bend_factor:.2f}")

    if random.random() < 0.1:
        angle = random.choice([random.uniform(15, 35), random.uniform(325, 345)])
        offset = random.randint(15, 50)
        image, offset_adjustment = add_fault(image, angle, offset, current_height)
        current_height += offset_adjustment
        events.append(f"Added fault with angle {angle:.2f} and offset {offset}")

    if not rotation_occurred and random.random() < 0.1:
        image, rotation_adjustment, rotation_occurred = apply_rotation(image, current_height, rotation_occurred)
        current_height += rotation_adjustment
        events.append(f"Applied rotation with adjustment {rotation_adjustment}")

    if 300 < current_height < 700 and random.random() < 0.05:
        image = add_intrusion(image, current_height)
        events.append(f"Added intrusion at height {current_height}")

# Add the last layer
if current_height >= 270:
    last_layer_thickness = random.randint(270, 300)
    current_height, last_color = add_layer(image, current_height, last_layer_thickness, last_color, colors)
    events.append(f"Added final layer of {color_to_rock[last_color]} with thickness {last_layer_thickness}")

# Show only the final 500x500 central section
center_x, center_y = width // 2, height // 2
final_image = image[center_y - 250:center_y + 250, center_x - 250:center_x + 250]

# Create a new white image of size 1024x576
final_output = np.ones((576, 1024, 3), dtype=np.uint8) * 255

# Place the 500x500 image on the left side
y_offset = (576 - 500) // 2
final_output[y_offset:y_offset+500, 76:76+500] = final_image

# Add legend
legend_start_x = 600
legend_start_y = 100
legend_square_size = 30
spacing = 50

for i, (color, rock_type) in enumerate(color_to_rock.items()):
    # Draw color square
    cv2.rectangle(final_output, 
                  (legend_start_x, legend_start_y + i*spacing), 
                  (legend_start_x + legend_square_size, legend_start_y + legend_square_size + i*spacing), 
                  color, -1)
    cv2.rectangle(final_output, 
                  (legend_start_x, legend_start_y + i*spacing), 
                  (legend_start_x + legend_square_size, legend_start_y + legend_square_size + i*spacing), 
                  (0, 0, 0), 1)  # Add black border
    
    # Add rock type text
    add_text(final_output, rock_type, 
             (legend_start_x + legend_square_size + 10, legend_start_y + 25 + i*spacing))

# Add intrusion to legend
intrusion_width = legend_square_size // 2
intrusion_height = legend_square_size
draw_intrusion_symbol(final_output, 
                      legend_start_x, 
                      legend_start_y + 4*spacing, 
                      legend_square_size, 
                      intrusion_height)
add_text(final_output, "intrusion", 
         (legend_start_x + legend_square_size + 10, legend_start_y + 25 + 4*spacing))

# Show the final output
show_image(final_output, "Final Geological Profile with Legend")

# Optionally, save the image
cv2.imwrite("geological_profile_with_legend.png", cv2.cvtColor(final_output, cv2.COLOR_RGB2BGR))

# Print the list of events
print("Events that occurred during the simulation:")
for i, event in enumerate(events, 1):
    print(f"{i}. {event}")

# Expand the edges of the final image
def expand_edge(edge, orientation):
    if orientation == 'horizontal':
        return np.tile(edge, (500, 1, 1))
    else:
        return np.tile(edge, (1, 500, 1))

# Extract edges from the final 500x500 image
top_edge = final_image[0:1, :]
bottom_edge = final_image[-1:, :]
left_edge = final_image[:, 0:1]
right_edge = final_image[:, -1:]

# Expand each edge to 500x500
expanded_top = expand_edge(top_edge, 'horizontal')
expanded_bottom = expand_edge(bottom_edge, 'horizontal')
expanded_left = expand_edge(left_edge, 'vertical')
expanded_right = expand_edge(right_edge, 'vertical')

