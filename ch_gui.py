# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from change_proneness import analyze_code

class ChangePronenessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Change Proneness Analyzer")
        self.root.geometry("600x400")
        
        # Upload Button
        self.upload_button = tk.Button(
            root, text="Upload Python File", command=self.upload_file
        )
        self.upload_button.pack(pady=20)
        
        # Result Text Area
        self.result_text = tk.Text(root, wrap="word", height=15, width=70)
        self.result_text.pack(pady=10)
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py")]
        )
        if file_path:
            try:
                metrics = analyze_code(file_path)
                self.display_metrics(metrics)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to analyze file: {str(e)}")
    
    def display_metrics(self, metrics):
        self.result_text.delete(1.0, tk.END)
        output = "Change Proneness Metrics:\n\n"
        
        # Cyclomatic Complexity
        output += "Cyclomatic Complexity:\n"
        for item in metrics['cyclomatic_complexity']:
            output += f"  - {item['name']}: {item['complexity']}\n"
        
        # Maintainability Index
        output += f"\nMaintainability Index: {metrics['maintainability_index']}\n"
        
        # Halstead Metrics
        output += "\nHalstead Metrics:\n"
        for metric in metrics['halstead_metrics']:
            output += "  - Halstead Metric:\n"
            if hasattr(metric, 'h1'):
                output += f"    - h1 (Unique Operators): {metric.h1}\n"
                output += f"    - h2 (Unique Operands): {metric.h2}\n"
                output += f"    - N1 (Total Operators): {metric.N1}\n"
                output += f"    - N2 (Total Operands): {metric.N2}\n"
                output += f"    - Vocabulary: {metric.vocabulary}\n"
                output += f"    - Length: {metric.length}\n"
                output += f"    - Calculated Length: {metric.calculated_length}\n"
                output += f"    - Volume: {metric.volume}\n"
                output += f"    - Difficulty: {metric.difficulty}\n"
                output += f"    - Effort: {metric.effort}\n"
            else:
                output += "    - No Halstead metrics available for this item.\n"
        
        # Raw Metrics
        output += "\nRaw Metrics:\n"
        for key, value in metrics['raw_metrics'].items():
            output += f"  - {key}: {value}\n"
        
        self.result_text.insert(tk.END, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChangePronenessGUI(root)
    root.mainloop()
