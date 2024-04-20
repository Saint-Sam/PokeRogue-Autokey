#!/usr/bin/env python
# coding: utf-8

# In[4]:


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
        
        ttk.Label(root, text="Enter keys or start recording:").grid(row=0, column=0, padx=10, pady=10)
        self.keys_entry = ttk.Entry(root, width=50)
        self.keys_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Button(root, text="Save Keys", command=self.save_keys).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(root, text="Load Keys", command=self.load_keys).grid(row=0, column=3, padx=10, pady=10)
        
        ttk.Label(root, text="Add delay between inputs (in seconds, e.g., 1, 3, 5):").grid(row=1, column=0, padx=10, pady=10)
        self.delay_entry = ttk.Entry(root, width=50)
        self.delay_entry.insert(0, "1")
        self.delay_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(root, text="Enter number of cycles:").grid(row=2, column=0, padx=10, pady=10)
        self.reps_entry = ttk.Entry(root, width=50)
        self.reps_entry.insert(0, "1")
        self.reps_entry.grid(row=2, column=1, padx=10, pady=10)

        self.run_button = ttk.Button(root, text="Run Autokeys", command=self.start_thread)
        self.run_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

        self.record_button = ttk.Button(root, text="Start Recording Keys", command=self.start_recording)
        self.record_button.grid(row=4, column=0, padx=10, pady=10)

        self.stop_record_button = ttk.Button(root, text="Stop Recording Keys", command=self.stop_recording)
        self.stop_record_button.grid(row=4, column=1, padx=10, pady=10)

        self.clear_keys_button = ttk.Button(root, text="Clear Keys", command=self.clear_keys)
        self.clear_keys_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.cancel_button = ttk.Button(root, text="Cancel Autokeys", command=self.stop_thread)
        self.cancel_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        self.log_text = tk.Text(root, height=10, width=75)
        self.log_text.grid(row=7, column=0, columnspan=4, padx=10, pady=10)
        self.log_text.config(state='disabled')

        root.bind("<Escape>", self.stop_thread)
        self.running = threading.Event()
        self.recording = False
        self.recorded_keys = []

        self.debug_window_titles_button = ttk.Button(root, text="Debug Window Titles", command=self.debug_window_titles)
        self.debug_window_titles_button.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

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


    def update_log(self, message, error=False):
        self.log_text.config(state='normal')
        if error:
            message = "Error: " + message
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state='disabled')
        self.log_text.yview(tk.END)

    def focus_browser_window(self, title_part):
        try:
            windows = gw.getWindowsWithTitle(title_part)
            target_window = next((win for win in windows if title_part in win.title), None)
            if target_window:
                target_window.activate()
                target_window.maximize()
                return f"Focused on: {target_window.title}"
            else:
                return "No window with specified title part found."
        except Exception as e:
            return f"Error focusing window: {str(e)}"

    def run_simulation(self):
        try:
            input_keys = self.keys_entry.get()
            delay = float(self.delay_entry.get())
            repetitions = int(self.reps_entry.get())
            self.running.set()

            focus_message = self.focus_browser_window("PokéRogue")
            self.update_log(focus_message)

            if "Focused on" not in focus_message:
                self.update_log("Unable to focus on the game window. Stopping simulation.")
                return

            for cycle in range(repetitions):
                if not self.running.is_set():
                    break
                self.update_log(f"Starting cycle {cycle + 1} of {repetitions}...")
                time.sleep(5)  # Increased initial delay for better window focus stability

                for key in input_keys.split(','):
                    for char in key.strip():
                        if not self.running.is_set():
                            break
                        pydirectinput.press(char)
                        time.sleep(delay)  # Consider increasing this if keys are not being registered
                        self.update_log(f"Pressed '{char}' with a delay of {delay} seconds.")
                if self.running.is_set():
                    self.update_log("Cycle completed.")
            self.update_log("Autokeys stopped.")
        except Exception as e:
            self.update_log(str(e), error=True)



    def start_thread(self, event=None):
        self.running.clear()
        threading.Thread(target=self.run_simulation, daemon=True).start()

    def stop_thread(self, event=None):
        self.running.clear()
        self.recording = False
        self.update_log("Stopping Autokeys...")

    def start_recording(self):
        if self.recording:
            self.update_log("Already recording.")
            return

        self.recording = True
        self.recorded_keys.clear()
        self.update_log("Started recording keys...")

        def on_press(key):
            try:
                self.recorded_keys.append(key.char)
                self.update_log(f"Recorded key: {key.char}")
            except AttributeError:
                pass 

        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.start()

    def stop_recording(self, event=None):
        if not self.recording:
            self.update_log("Not currently recording.")
            return
        self.listener.stop()

        self.recording = False
        formatted_keys = ','.join(self.recorded_keys)
        self.keys_entry.delete(0, tk.END)
        self.keys_entry.insert(0, formatted_keys)
        self.update_log("Stopped recording. Keys loaded into input.")

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
            self.update_log("No saved keys found.")

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




