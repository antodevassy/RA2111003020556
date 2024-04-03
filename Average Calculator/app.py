from flask import Flask, jsonify, render_template
import requests
from collections import deque
import time

app = Flask(__name__)

window_size = 10
numbers_window = deque(maxlen=window_size)

def fetch_numbers(number_type):
    url = f"http://20.244.56.144/test/{number_type}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("numbers", [])
        else:
            return []
    except requests.exceptions.RequestException:
        return []

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

@app.route('/numbers/<numberid>')
def get_numbers_and_average(numberid):
    global numbers_window
    start_time = time.time()

    numbers = fetch_numbers(numberid)
    
    if time.time() - start_time > 0.5:
        return jsonify({"error": "Request timed out"}), 500

    if numbers:
        numbers_set = set(numbers)
        numbers_window.extend(numbers_set)
    
    avg = calculate_average(numbers_window)

    response = {
        "windowPrevState": list(numbers_window),
        "windowCurrState": list(numbers_window),
        "numbers": list(numbers_set),
        "avg": avg
    }

    return jsonify(response)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=9876)
