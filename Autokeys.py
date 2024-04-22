#!/usr/bin/env python
# coding: utf-8

# In[18]:


import tkinter as tk
from tkinter import ttk
import time
import threading
import pydirectinput
import pygetwindow as gw
from pynput import keyboard

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoKeys")
        
        # Padding for the labels and buttons
        pad_x = 5
        pad_y = 5
        
        # Entry widgets
        ttk.Label(root, text="Enter keys or start recording:").grid(row=0, column=1, padx=pad_x, pady=pad_y)
        self.keys_entry = ttk.Entry(root)
        self.keys_entry.grid(row=0, column=2, padx=pad_x, pady=pad_y)

        ttk.Label(root, text="Enter number of cycles:").grid(row=1, column=1, padx=pad_x, pady=pad_y)
        self.reps_entry = ttk.Entry(root)
        self.reps_entry.insert(0, "1")
        self.reps_entry.grid(row=1, column=2, padx=pad_x, pady=pad_y)

        # Buttons
        ttk.Button(root, text="Save Keys", command=self.save_keys).grid(row=0, column=3, padx=pad_x, pady=pad_y)
        ttk.Button(root, text="Load Keys", command=self.load_keys).grid(row=0, column=4, padx=pad_x, pady=pad_y)

        self.run_button = ttk.Button(root, text="Run Autokeys", command=self.start_thread)
        self.run_button.grid(row=2, column=1, columnspan=2, padx=pad_x, pady=pad_y)

        self.record_button = ttk.Button(root, text="Start Recording Keys", command=self.start_recording)
        self.record_button.grid(row=3, column=1, padx=pad_x, pady=pad_y)

        self.stop_record_button = ttk.Button(root, text="Stop Recording Keys", command=self.stop_recording)
        self.stop_record_button.grid(row=3, column=2, padx=pad_x, pady=pad_y)

        self.clear_keys_button = ttk.Button(root, text="Clear Keys", command=self.clear_keys)
        self.clear_keys_button.grid(row=4, column=1, columnspan=2, padx=pad_x, pady=pad_y)

        self.cancel_button = ttk.Button(root, text="Cancel Autokeys", command=self.stop_thread)
        self.cancel_button.grid(row=5, column=1, columnspan=2, padx=pad_x, pady=pad_y)

        self.log_text = tk.Text(root, height=10)
        self.log_text.grid(row=6, column=0, columnspan=5, padx=pad_x, pady=pad_y)
        self.log_text.config(state='disabled')

        self.debug_window_titles_button = ttk.Button(root, text="Debug Window Titles", command=self.debug_window_titles)
        self.debug_window_titles_button.grid(row=7, column=1, columnspan=2, padx=pad_x, pady=pad_y)


        self.running = threading.Event()
        self.recording = False
        self.recorded_events = []
        self.last_time = None
        self.listener = keyboard.Listener(on_press=self.on_press)
        
        
    def debug_window_titles(self):
        windows = gw.getAllWindows()
        found = False
        for win in windows:
            if "PokéRogue" in win.title:  # adjust as necessary
                self.update_log(f"Trying to focus on: {win.title}")
                win.activate()
                win.maximize()
                found = True
        if not found:
            self.update_log("No window with specified title part found.")

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.recorded_events.clear()
            self.last_time = time.time()
            self.listener.start()
            self.update_log("Recording started...")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.listener.stop()
            formatted_keys = self.format_recorded_events()
            self.keys_entry.delete(0, tk.END)
            self.keys_entry.insert(0, formatted_keys)
            self.update_log("Recording stopped.")

    def on_press(self, key):
        if self.recording:
            try:
                now = time.time()
                delay = round(now - self.last_time, 2)
                self.last_time = now
                if hasattr(key, 'char') and key.char:
                    self.recorded_events.append((key.char, delay))
                    self.update_log(f"Recorded '{key.char}' with a delay of {delay}s.")
            except AttributeError:
                pass

    def format_recorded_events(self):
        formatted_keys = ','.join(f"{key}:{delay}" for key, delay in self.recorded_events)
        return formatted_keys

    def update_log(self, message, error=False):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n" if not error else "Error: " + message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.yview(tk.END)

    def start_thread(self):
        if not self.running.is_set():
            self.running.set()
            thread = threading.Thread(target=self.run_autokeys, daemon=True)
            thread.start()
            self.update_log("Autokeys thread started...")

    def stop_thread(self):
        self.running.clear()
        self.update_log("Autokeys thread stopped...")

    def run_autokeys(self):
        self.update_log("Running autokeys...")
        try:
            while self.running.is_set():
                for key, delay in self.recorded_events:
                    if not self.running.is_set():
                        break
                    pydirectinput.press(key)
                    time.sleep(delay)
                    self.update_log(f"Pressed '{key}' after waiting {delay}s.")
        except Exception as e:
            self.update_log(str(e), True)

    def clear_keys(self):
        self.keys_entry.delete(0, tk.END)
        self.update_log("Keys cleared.")

    def save_keys(self):
        saved_keys = self.keys_entry.get()
        with open("saved_keys.txt", "w") as f:
            f.write(saved_keys)
        self.update_log("Keys saved successfully.")

    def load_keys(self):
        try:
            with open("saved_keys.txt", "r") as f:
                loaded_keys = f.read()
            self.keys_entry.delete(0, tk.END)
            self.keys_entry.insert(0, loaded_keys)
            self.update_log("Keys loaded successfully.")
        except FileNotFoundError:
            self.update_log("No saved keys found.", True)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[74]:





# In[89]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[45]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[60]:





# In[ ]:





# In[92]:





# In[ ]:





# In[ ]:




