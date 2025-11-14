import logging
import sys
from flask import Flask, jsonify

# --- Logger Setup ---
# This sets up our logging system
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Set the 'floor' for logging level

# Create a handler to write logs to the console (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Define the format for our log messages
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# Add the handler to our logger
logger.addHandler(handler)

# --- Flask App ---
app = Flask(__name__)

@app.route('/')
def index():
    # This is a "normal" log message
    logger.info("Homepage was visited.")
    return "Hello! This is the homepage."

@app.route('/data')
def get_data():
    # This is also a "normal" log message
    logger.info("Data endpoint was requested.")
    return jsonify({"id": 1, "name": "testdata"})

@app.route('/error')
def trigger_error():
    # This is an "abnormal" or "error" log we want to catch
    logger.error("An intentional error was triggered!")
    return "Oops, something went wrong!", 500

if __name__ == '__main__':
    logger.info("Application starting up...")
    app.run(debug=True, host='0.0.0.0', port=5000)