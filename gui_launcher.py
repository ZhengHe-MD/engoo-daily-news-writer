#!/usr/bin/env python3
"""
Engoo Daily News Writer - GUI Launcher
A simple graphical interface for non-technical users.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import sys
import subprocess
import threading
import webbrowser
from pathlib import Path

class EngooGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Engoo Daily News Writer")
        self.root.geometry("800x600")
        
        # Check if setup is complete
        self.setup_complete = self.check_setup()
        
        self.create_widgets()
        
    def check_setup(self):
        """Check if the tool is properly set up."""
        env_file = Path(".env")
        venv_dir = Path(".venv")
        
        if not env_file.exists() or not venv_dir.exists():
            return False
            
        # Check if API keys are in .env
        try:
            with open(".env") as f:
                content = f.read()
                return "OPENAI_API_KEY=" in content and "GITHUB_TOKEN=" in content
        except:
            return False
    
    def create_widgets(self):
        """Create the main GUI widgets."""
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="📚 Engoo Daily News Writer", 
            font=("Arial", 20, "bold"),
            fg="#2E8B57"
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            self.root, 
            text="Transform any article into professional ESL lessons",
            font=("Arial", 12),
            fg="#666666"
        )
        subtitle_label.pack(pady=(0, 30))
        
        if not self.setup_complete:
            self.create_setup_widgets()
        else:
            self.create_main_widgets()
    
    def create_setup_widgets(self):
        """Create setup widgets for first-time users."""
        
        setup_frame = ttk.LabelFrame(self.root, text="First Time Setup", padding=20)
        setup_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        info_text = """
Welcome! To get started, you need to set up two API keys:

1. OpenAI API Key - For AI-powered article processing
2. GitHub Token - For sharing lessons online

The setup will:
✓ Install all required components
✓ Help you get your API keys
✓ Test everything works correctly
        """
        
        info_label = tk.Label(setup_frame, text=info_text, justify="left", font=("Arial", 11))
        info_label.pack(pady=20)
        
        # Setup buttons
        button_frame = tk.Frame(setup_frame)
        button_frame.pack(pady=20)
        
        setup_btn = tk.Button(
            button_frame,
            text="🚀 Run Easy Setup",
            command=self.run_setup,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        setup_btn.pack(side="left", padx=10)
        
        help_btn = tk.Button(
            button_frame,
            text="📖 View Setup Guide",
            command=self.open_setup_guide,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            padx=20,
            pady=10
        )
        help_btn.pack(side="left", padx=10)
    
    def create_main_widgets(self):
        """Create main application widgets."""
        
        # URL input frame
        url_frame = ttk.LabelFrame(self.root, text="Convert Article", padding=15)
        url_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(url_frame, text="Article URL:", font=("Arial", 11)).pack(anchor="w")
        
        url_input_frame = tk.Frame(url_frame)
        url_input_frame.pack(fill="x", pady=(5, 10))
        
        self.url_entry = tk.Entry(url_input_frame, font=("Arial", 11))
        self.url_entry.pack(side="left", fill="x", expand=True)
        
        convert_btn = tk.Button(
            url_input_frame,
            text="Convert",
            command=self.convert_article,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15
        )
        convert_btn.pack(side="right", padx=(10, 0))
        
        # Options
        options_frame = tk.Frame(url_frame)
        options_frame.pack(fill="x")
        
        self.share_online = tk.BooleanVar(value=True)
        share_check = tk.Checkbutton(
            options_frame,
            text="Share online (create shareable link)",
            variable=self.share_online,
            font=("Arial", 10)
        )
        share_check.pack(anchor="w")
        
        # Gist management frame
        gist_frame = ttk.LabelFrame(self.root, text="Manage Shared Lessons", padding=15)
        gist_frame.pack(padx=20, pady=10, fill="x")
        
        gist_btn_frame = tk.Frame(gist_frame)
        gist_btn_frame.pack(fill="x")
        
        list_btn = tk.Button(
            gist_btn_frame,
            text="📋 List Lessons",
            command=self.list_gists,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10),
            padx=15
        )
        list_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = tk.Button(
            gist_btn_frame,
            text="🔄 Refresh",
            command=self.refresh_gui,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10),
            padx=15
        )
        refresh_btn.pack(side="right")
        
        # Output frame
        output_frame = ttk.LabelFrame(self.root, text="Output", padding=15)
        output_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=15,
            font=("Monaco", 10),
            bg="#f8f8f8"
        )
        self.output_text.pack(fill="both", expand=True)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready to convert articles!",
            relief="sunken",
            anchor="w",
            font=("Arial", 9),
            bg="#f0f0f0"
        )
        self.status_bar.pack(side="bottom", fill="x")
    
    def run_setup(self):
        """Run the easy setup script."""
        def setup_thread():
            try:
                self.log_output("Starting setup process...\n")
                
                if sys.platform == "win32":
                    result = subprocess.run(
                        ["easy_install.bat"], 
                        capture_output=True, 
                        text=True,
                        shell=True
                    )
                else:
                    result = subprocess.run(
                        ["./easy_install.sh"], 
                        capture_output=True, 
                        text=True
                    )
                
                if result.returncode == 0:
                    self.log_output("Setup completed successfully!\n")
                    self.log_output("Please restart the application.\n")
                    messagebox.showinfo(
                        "Setup Complete", 
                        "Setup completed successfully!\nPlease restart the application."
                    )
                else:
                    self.log_output(f"Setup failed:\n{result.stderr}\n")
                    messagebox.showerror("Setup Error", "Setup failed. Check the output for details.")
                    
            except Exception as e:
                self.log_output(f"Setup error: {str(e)}\n")
                messagebox.showerror("Setup Error", f"Setup failed: {str(e)}")
        
        threading.Thread(target=setup_thread, daemon=True).start()
    
    def convert_article(self):
        """Convert an article using the CLI tool."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Input Error", "Please enter an article URL.")
            return
        
        def convert_thread():
            try:
                self.log_output(f"Converting article: {url}\n")
                self.update_status("Converting article...")
                
                # Build command
                if sys.platform == "win32":
                    cmd = ["engoo-writer.bat", "convert", url]
                else:
                    cmd = ["./engoo-writer", "convert", url]
                
                if self.share_online.get():
                    cmd.append("--gist")
                
                # Run command
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    cwd=os.getcwd()
                )
                
                if result.returncode == 0:
                    self.log_output("✅ Conversion completed successfully!\n")
                    self.log_output(result.stdout)
                    
                    if self.share_online.get():
                        self.log_output("\n🌐 Lesson shared online!\n")
                    
                    self.update_status("Ready")
                    messagebox.showinfo("Success", "Article converted successfully!")
                else:
                    self.log_output(f"❌ Conversion failed:\n{result.stderr}\n")
                    self.update_status("Error")
                    messagebox.showerror("Error", "Conversion failed. Check the output for details.")
                    
            except Exception as e:
                self.log_output(f"Error: {str(e)}\n")
                self.update_status("Error")
                messagebox.showerror("Error", f"Conversion failed: {str(e)}")
        
        threading.Thread(target=convert_thread, daemon=True).start()
    
    def list_gists(self):
        """List all shared lessons."""
        def list_thread():
            try:
                self.log_output("Fetching your shared lessons...\n")
                self.update_status("Fetching lessons...")
                
                if sys.platform == "win32":
                    cmd = ["engoo-writer.bat", "gist", "list"]
                else:
                    cmd = ["./engoo-writer", "gist", "list"]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_output(result.stdout)
                    self.update_status("Ready")
                else:
                    self.log_output(f"Failed to fetch lessons:\n{result.stderr}\n")
                    self.update_status("Error")
                    
            except Exception as e:
                self.log_output(f"Error: {str(e)}\n")
                self.update_status("Error")
        
        threading.Thread(target=list_thread, daemon=True).start()
    
    def open_setup_guide(self):
        """Open the setup guide in a web browser."""
        readme_path = Path("README_EDUCATORS.md")
        if readme_path.exists():
            webbrowser.open(f"file://{readme_path.absolute()}")
        else:
            webbrowser.open("https://github.com/ZhengHe-MD/engoo-daily-news-writer")
    
    def refresh_gui(self):
        """Refresh the GUI to check setup status."""
        self.setup_complete = self.check_setup()
        
        # Clear and recreate widgets
        for widget in self.root.winfo_children():
            if widget != self.status_bar:  # Keep status bar
                widget.destroy()
        
        self.create_widgets()
    
    def log_output(self, text):
        """Add text to the output area."""
        if hasattr(self, 'output_text'):
            self.output_text.insert(tk.END, text)
            self.output_text.see(tk.END)
            self.root.update_idletasks()
    
    def update_status(self, text):
        """Update the status bar."""
        if hasattr(self, 'status_bar'):
            self.status_bar.config(text=text)
            self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = EngooGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
