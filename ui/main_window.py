import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from vertex_ai_client import VertexAIClient
from requirements_parser import RequirementsParser

class RequirementsExtractorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Requirements Extractor")
        self.root.geometry("1000x700")
        
        self.ai_client = VertexAIClient()
        self.parser = RequirementsParser()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # File selection
        ttk.Label(main_frame, text="JSON File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        self.file_path_var = tk.StringVar()
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state="readonly")
        self.file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        ttk.Button(file_frame, text="Browse", command=self.browse_file).grid(row=0, column=1)
        
        # Extract button
        ttk.Button(main_frame, text="Extract Requirements", command=self.extract_requirements).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Results frame
        results_frame = ttk.Frame(main_frame)
        results_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        results_frame.columnconfigure(0, weight=1)
        results_frame.columnconfigure(1, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Functional requirements
        ttk.Label(results_frame, text="Functional Requirements", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.functional_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=15)
        self.functional_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Non-functional requirements
        ttk.Label(results_frame, text="Non-Functional Requirements", font=("Arial", 12, "bold")).grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        self.non_functional_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, height=15)
        self.non_functional_text.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def extract_requirements(self):
        if not self.file_path_var.get():
            messagebox.showerror("Error", "Please select a JSON file first.")
            return
            
        try:
            self.status_var.set("Loading JSON file...")
            self.root.update()
            
            # Load JSON file
            with open(self.file_path_var.get(), 'r', encoding='utf-8') as file:
                json_data = json.load(file)
            
            self.status_var.set("Extracting requirements using AI...")
            self.root.update()
            
            # Extract requirements using AI
            ai_response = self.ai_client.extract_requirements(json_data)
            
            self.status_var.set("Parsing requirements...")
            self.root.update()
            
            # Parse the response
            requirements = self.parser.parse_requirements(ai_response)
            
            # Display results
            self.display_requirements(requirements)
            
            self.status_var.set("Requirements extracted successfully!")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            self.status_var.set("Error: File not found")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file.")
            self.status_var.set("Error: Invalid JSON file")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set(f"Error: {str(e)}")
            
    def display_requirements(self, requirements):
        # Clear previous results
        self.functional_text.delete(1.0, tk.END)
        self.non_functional_text.delete(1.0, tk.END)
        
        # Display functional requirements
        for i, req in enumerate(requirements['functional'], 1):
            self.functional_text.insert(tk.END, f"{i}. {req}\n\n")
            
        # Display non-functional requirements
        for i, req in enumerate(requirements['non_functional'], 1):
            self.non_functional_text.insert(tk.END, f"{i}. {req}\n\n")

def main():
    root = tk.Tk()
    app = RequirementsExtractorUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()