import json
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

signals ={
    "0": {
        "freq": 1800,
        "bandwidth": 20,
        "power": 70.0,
        "signal_type": "smooth",
        "mod": "None",
        "bearing": 105,
        "text": ".. ^ .. ^ .. ^ ..",
        "source": "RLC",
        "X": "10",
        "Y": "12",
	    "distance": 0.5
    },
    "1": {
        "freq": 1850,
        "bandwidth": 20.200,
        "power": 65.0,
        "signal_type": "ragged",
        "mod": "am",
        "bearing": 120,
        "text": ".. ^ .. ^ .. ^ ..",
        "source": "radio",
        "X": "10",
        "Y": "12",
	    "distance": 1
    }
}

scale = 1
draw_path=True


def plot_polar_graph(image_path = "img/image.jpg", data=signals):
    
    # Load map image
    img = Image.open(image_path)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
    ax.set_xlim(0, 1 * np.pi * scale)
    ax.set_ylim(0, 1)
    
    # Hide axis
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    
    # Plot the background image
    ax.imshow(img, extent=[0, 2 * np.pi, 0, 1], aspect='auto')
    
    # Define center point
    center_r = 0  # Origin in polar
    center_theta = 0  # Angle irrelevant for center
    ax.plot(center_theta, center_r, 'ro', markersize=8, label="Center")
    
    last_theta, last_r = None, None
    
    for key in data:
        entry = data[key]
        theta = np.radians(entry["bearing"])  # Convert bearing to radians
        r = entry["distance"] / scale  # Scale distance
        
        # Keep points within bounds (max radius is 1)
        if r > 1:
            r = 1  # Move to the edge of the map
        
        ax.plot(theta, r, 'bo', markersize=6)  # Plot point
        last_theta, last_r = theta, r
    
    # Draw path from center to last point if required
    if draw_path and last_theta is not None:
        ax.plot([0, last_theta], [0, last_r], 'r-', linewidth=2)
        ax.text(last_theta, last_r, f"{np.degrees(last_theta):.1f}°", 
                fontsize=12, color='red', ha='left', va='bottom')
    
    plt.show()

def clear_signals(signals):
    signals = {}
    plot_polar_graph()

def change_scale(scale_changed):
    scale = scale_changed
    plot_polar_graph()

def change_draw_path():
    if draw_path == True:
        draw_path = False
    else:
        draw_path = True
    plot_polar_graph()

# Example usage
change_scale(1)
change_scale(2)
change_scale(5)
