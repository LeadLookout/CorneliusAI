# FILE: cornelius_os/run.py
from app import download_spacy_model, create_app
import os
from app.modules.developer_mode import DeveloperMode
from app.modules.personality import Personality
from app.gui import CorneliusApp  # Import Kivy app

# --- Developer Mode Setup ---
DEVELOPER_PASSWORD = "MySuperSecretPassword"  # !!! CHANGE THIS !!! AND DO NOT COMMIT TO VERSION CONTROL
developer_mode = DeveloperMode(DEVELOPER_PASSWORD)

# --- Personality Setup ---
personality = Personality() #Instantiate personality.

def main():
    # --- First-run check and spaCy model download ---
    if not os.path.exists('venv/Lib/site-packages/en_core_web_sm'): # Adapt if not using venv
        download_spacy_model()

    # --- Developer Authentication (Example) ---
    while not developer_mode.is_enabled:
        password = input("Enter developer password (or type 'exit' to run in normal mode): ")
        if password.lower() == 'exit':
            break
        developer_mode.authenticate(password)

    if developer_mode.check_access():
        print("Running in developer mode.")
    else:
        print("Running in normal mode.")

    # --- Run the Kivy App ---
    CorneliusApp().run() #Runs kivy app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)