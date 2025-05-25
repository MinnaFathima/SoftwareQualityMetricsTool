# gui_code.py
import tkinter as tk
from tkinter import filedialog, Text
from complexity_model import process_uploaded_file

# Function to handle file upload
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        trend_predictions = process_uploaded_file(file_path)
        display_results(trend_predictions)

# Function to display the results in the text area
def display_results(predictions):
    result_text.delete("1.0", "end")
    result_text.insert("end", "Function Complexity Trend Prediction:\n")
    for func_name, predicted_complexity in predictions.items():
        result_text.insert("end", f"Function '{func_name}': Predicted next complexity = {predicted_complexity:.2f}\n")

# Main GUI setup
root = tk.Tk()
root.title("Function Complexity Trend Predictor")
root.geometry("600x400")

tk.Label(root, text="Upload a Python file to analyze Function Complexity Trend", font=("Helvetica", 14)).pack(pady=10)

tk.Button(root, text="Upload Python File", command=upload_file, font=("Helvetica", 12)).pack(pady=10)

result_text = Text(root, wrap="word", font=("Helvetica", 12))
result_text.pack(pady=10, fill="both", expand=True)

root.mainloop()
