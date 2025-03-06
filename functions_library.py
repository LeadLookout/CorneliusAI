def example_function(param1, param2):
    """An example function that adds two numbers."""
    return param1 + param2

def another_utility_function(data):
    """Processes the input data and returns the result."""
    # Perform some processing on the data
    processed_data = [item * 2 for item in data]
    return processed_data

def log_message(message):
    """Logs a message to the console or a log file."""
    print(f"LOG: {message}")

def validate_input(input_data):
    """Validates the input data and returns True if valid, False otherwise."""
    return isinstance(input_data, (int, float)) and input_data >= 0

# Add more utility functions as needed for the application.