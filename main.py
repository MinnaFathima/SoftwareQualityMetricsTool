# complexity_model.py
import os
import json
from datetime import datetime
from radon.complexity import cc_visit
from sklearn.linear_model import LinearRegression
import numpy as np

# Analyze Function Complexity
def analyze_uploaded_file(file_path):
    with open(file_path, 'r') as f:
        source_code = f.read()
    complexities = {func.name: func.complexity for func in cc_visit(source_code)}
    return complexities

# Store Complexity Data in JSON
def store_complexity_data(file_name, complexities, storage_file='complexity_data.json'):
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    timestamp = datetime.now().isoformat()
    data[timestamp] = {'file_name': file_name, 'complexities': complexities}

    with open(storage_file, 'w') as f:
        json.dump(data, f)

# Predict Complexity Trend Using Linear Regression
def predict_trend(data):
    predictions = {}
    for func_name, complexities in data.items():
        timestamps = np.arange(len(complexities)).reshape(-1, 1)
        y = np.array(complexities)

        # Train model
        model = LinearRegression().fit(timestamps, y)

        # Predict the next complexity value
        next_timestamp = np.array([[len(complexities)]])
        future_complexity = model.predict(next_timestamp)

        predictions[func_name] = future_complexity[0]
    return predictions

# Process the Uploaded File and Get Predictions
def process_uploaded_file(file_path, storage_file='complexity_data.json'):
    complexities = analyze_uploaded_file(file_path)
    store_complexity_data(file_path, complexities, storage_file)

    with open(storage_file, 'r') as f:
        data = json.load(f)

    trend_data = {}
    for timestamp, info in data.items():
        for func_name, complexity in info['complexities'].items():
            if func_name not in trend_data:
                trend_data[func_name] = []
            trend_data[func_name].append(complexity)

    trend_predictions = predict_trend(trend_data)
    return trend_predictions
