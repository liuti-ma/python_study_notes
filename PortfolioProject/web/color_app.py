from flask import Flask, render_template, request, redirect, url_for
import os
from PIL import Image
import numpy as np
from collections import defaultdict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def get_top_colors(image_path, top_n=10):
    # Open the image and convert to RGB
    image = Image.open(image_path).convert('RGB')
    image = image.resize((150, 150))  # Resize for faster processing
    pixels = np.array(image)

    # Flatten the image into a list of RGB values
    pixels = pixels.reshape(-1, 3)

    # Count the frequency of each color
    color_counts = defaultdict(int)
    for pixel in pixels:
        color_counts[tuple(pixel)] += 1

    # Sort colors by frequency and get the top N
    sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    top_colors = [color for color, count in sorted_colors]

    return top_colors

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'image' not in request.files:
            return redirect(request.url)

        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            # Get the top 10 colors
            top_colors = get_top_colors(filepath)
            hex_colors = [rgb_to_hex(color) for color in top_colors]

            # Render the result
            return render_template('color_index.html', colors=hex_colors, image_url=filepath)

    return render_template('color_index.html', colors=None, image_url=None)

if __name__ == '__main__':
    app.run(debug=True)