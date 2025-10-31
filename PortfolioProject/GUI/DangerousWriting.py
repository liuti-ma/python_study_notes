import tkinter as tk
from tkinter import scrolledtext
import threading

# Constants
IDLE_TIME_LIMIT = 5  # Time in seconds before text is deleted

class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("The Dangerous Writing App")
        self.root.geometry("600x400")

        # Text area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Arial", 14))
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # Timer label
        self.timer_label = tk.Label(self.root, text=f"Time left: {IDLE_TIME_LIMIT}", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        # Track last keystroke time
        self.last_keystroke_time = None
        self.timer_running = False

        # Bind keypress event
        self.text_area.bind("<KeyPress>", self.reset_timer)

        # Start the timer thread
        self.start_timer()

    def reset_timer(self, event=None):
        """Reset the timer whenever a key is pressed."""
        self.last_keystroke_time = self.root.after(IDLE_TIME_LIMIT * 1000, self.delete_text)

    def delete_text(self):
        """Delete all text in the text area."""
        self.text_area.delete(1.0, tk.END)
        self.timer_label.config(text="Time's up! All text deleted.")

    def start_timer(self):
        """Start the timer thread."""
        if not self.timer_running:
            self.timer_running = True
            self.last_keystroke_time = self.root.after(IDLE_TIME_LIMIT * 1000, self.delete_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()