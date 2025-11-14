import logging
import sys
from flask import Flask, jsonify

# --- Logger Setup ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

# Create a formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 1. Handler for the console (stdout)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

# 2. Handler for the log file (this is the new part)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler) # <-- This is new

# --- Flask App ---
app = Flask(__name__)

@app.route('/')
def index():
    logger.info("Homepage was visited.")
    return "Hello! This is the homepage."

@app.route('/data')
def get_data():
    logger.info("Data endpoint was requested.")
    return jsonify({"id": 1, "name": "testdata"})

@app.route('/error')
def trigger_error():
    logger.error("An intentional error was triggered!")
    return "Oops, something went wrong!", 500

if __name__ == '__main__':
    logger.info("Application starting up...")
    app.run(debug=True, host='0.0.0.0', port=5000)