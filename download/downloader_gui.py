import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests
import os
from urllib.parse import urlparse

# Example download list: (label, url, target_directory)
downloads = [
    ("File A", "https://example.com/files/fileA.zip", "downloads/"),
    ("File B", "https://example.com/files/fileB.zip", "downloads/"),
    ("File C", "https://example.com/others/fileC.txt", "downloads/texts/"),
]

class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-file Downloader")

        self.check_vars = []

        # UI: Checklist
        for label, _, _ in downloads:
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(self.root, text=label, variable=var)
            cb.pack(anchor="w")
            self.check_vars.append(var)

        # UI: Download button
        self.download_btn = ttk.Button(self.root, text="Start Download", command=self.start_download)
        self.download_btn.pack(pady=10)

    def start_download(self):
        selected = [(url, dir_) for var, (_, url, dir_) in zip(self.check_vars, downloads) if var.get()]
        if not selected:
            messagebox.showinfo("No selection", "Please select at least one file to download.")
            return
        self.download_btn.config(state="disabled")
        threading.Thread(target=self.download_files, args=(selected,), daemon=True).start()

    def download_files(self, selected):
        for url, directory in selected:
            try:
                # Extract filename from URL
                filename = os.path.basename(urlparse(url).path)
                full_path = os.path.join(directory, filename)

                # Ensure directory exists
                os.makedirs(directory, exist_ok=True)

                # Download
                response = requests.get(url, stream=True)
                response.raise_for_status()
                with open(full_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download from {url}:\n{e}")
        messagebox.showinfo("Download complete", "Selected files have been downloaded.")
        self.download_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")  # Set default size to 400x300 pixels
    app = DownloadApp(root)
    root.mainloop()

