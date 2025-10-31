import tkinter as tk
import time
import random

sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a great programming language for beginners.",
    "Speed typing test applications help improve accuracy.",
    "Tkinter makes GUI development easy and fun."
]


def start_test():
    global start_time, target_text
    start_time = time.time()
    target_text.set(random.choice(sample_texts))
    user_entry.config(state="normal")
    user_entry.delete(0, tk.END)
    user_entry.focus()
    start_btn.config(state="disabled")
    result_label.config(text="")


def calculate_speed():
    global start_time
    end_time = time.time()
    elapsed_time = end_time - start_time
    typed_text = user_entry.get()

    words_typed = len(typed_text.split())
    speed = words_typed / (elapsed_time / 60)  # Words per minute (WPM)

    accuracy = sum(1 for a, b in zip(typed_text, target_text.get()) if a == b) / max(len(target_text.get()), 1) * 100
    result_label.config(text=f"Speed: {speed:.2f} WPM\nAccuracy: {accuracy:.2f}%")
    start_btn.config(state="normal")
    user_entry.config(state="disabled")


# Initialize Tkinter window
root = tk.Tk()
root.title("Typing Speed Test")
root.geometry("500x300")

instructions = tk.Label(root, text="Type the following text as quickly and accurately as possible:")
instructions.pack(pady=5)

target_text = tk.StringVar()
target_label = tk.Label(root, textvariable=target_text, wraplength=400, font=("Arial", 12))
target_label.pack(pady=5)

user_entry = tk.Entry(root, width=50, font=("Arial", 12))
user_entry.pack(pady=5)
user_entry.config(state="disabled")

start_btn = tk.Button(root, text="Start Test", command=start_test)
start_btn.pack(pady=5)

submit_btn = tk.Button(root, text="Submit", command=calculate_speed)
submit_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

start_time = 0
root.mainloop()
