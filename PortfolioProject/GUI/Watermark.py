import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont


def upload_image():
    global img, img_display
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not file_path:
        return
    img = Image.open(file_path)
    img.thumbnail((400, 400))  # Resize for display
    img_display = ImageTk.PhotoImage(img)
    canvas.create_image(200, 200, image=img_display)


def add_watermark():
    global img
    if img is None:
        messagebox.showerror("Error", "Please upload an image first.")
        return

    watermark_text = watermark_entry.get()
    if not watermark_text:
        messagebox.showerror("Error", "Please enter watermark text.")
        return

    img_with_watermark = img.copy()
    draw = ImageDraw.Draw(img_with_watermark)
    font = ImageFont.load_default()
    text_position = (10, 10)
    text_color = (255, 255, 255)
    draw.text(text_position, watermark_text, fill=text_color, font=font)

    img_with_watermark.thumbnail((400, 400))  # Resize for display
    img_display_watermarked = ImageTk.PhotoImage(img_with_watermark)
    canvas.create_image(200, 200, image=img_display_watermarked)
    canvas.image = img_display_watermarked  # Prevent garbage collection


def save_image():
    if img is None:
        messagebox.showerror("Error", "No image to save.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"),
                                                        ("All Files", "*.*")])
    if not file_path:
        return
    img.save(file_path)
    messagebox.showinfo("Success", "Image saved successfully!")


# Initialize Tkinter window
root = tk.Tk()
root.title("Watermark Application")
root.geometry("500x600")

canvas = tk.Canvas(root, width=400, height=400, bg="gray")
canvas.pack(pady=10)

upload_btn = tk.Button(root, text="Upload Image", command=upload_image)
upload_btn.pack(pady=5)

watermark_entry = tk.Entry(root)
watermark_entry.pack(pady=5)

add_watermark_btn = tk.Button(root, text="Add Watermark", command=add_watermark)
add_watermark_btn.pack(pady=5)

save_btn = tk.Button(root, text="Save Image", command=save_image)
save_btn.pack(pady=5)

img = None

root.mainloop()
