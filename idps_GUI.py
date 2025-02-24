import tkinter as tk
from tkinter import simpledialog
from tkinter import scrolledtext, messagebox
import threading
import os
import hashlib
from idps import main as start_idps

class IDPSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("IDPS - Intrusion Detection and Prevention System")
        self.root.geometry("600x400")
        
        # Authentication
        if not self.authenticate():
            messagebox.showerror("Access Denied", "Invalid password. Exiting.")
            root.destroy()
            return
        
        # Log Display
        self.log_display = scrolledtext.ScrolledText(root, width=70, height=15)
        self.log_display.pack(pady=10)
        
        # Control Buttons
        self.start_button = tk.Button(root, text="Start Monitoring", command=self.start_idps)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop Monitoring", command=self.stop_idps, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.clear_button = tk.Button(root, text="Clear Logs", command=self.clear_logs)
        self.clear_button.pack(pady=5)
        
        # Thread for IDPS
        self.idps_thread = None
        self.monitoring = False
        
    def authenticate(self):
        password = "secure123"  # This should be securely stored or hashed
        user_input = tk.simpledialog.askstring("Authentication", "Enter Password:", show='*')
        return hashlib.sha256(user_input.encode()).hexdigest() == hashlib.sha256(password.encode()).hexdigest()

    def start_idps(self):
        if not self.monitoring:
            self.idps_thread = threading.Thread(target=start_idps, daemon=True)
            self.idps_thread.start()
            self.monitoring = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.log_display.insert(tk.END, "\nIDPS Started...\n")

    def stop_idps(self):
        if self.monitoring:
            os._exit(0)
            self.monitoring = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.log_display.insert(tk.END, "\nIDPS Stopped.\n")

    def clear_logs(self):
        open("./logs/file_log.txt", "w").close()
        open("./logs/network_connections_log.txt", "w").close()
        open("./logs/processes_log.txt", "w").close()
        self.log_display.insert(tk.END, "\nLogs Cleared.\n")
        messagebox.showinfo("Logs Cleared", "All logs have been cleared successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = IDPSGUI(root)
    root.mainloop()
