app/__init__.py
# FILE: cornelius_os/app/__init__.py
import spacy
import os

app = None #Placeholder

# Function to download the spaCy model if it's not present.
def download_spacy_model():
    model_name = 'en_core_web_sm'
    if not spacy.util.is_package(model_name):
        print(f"Downloading spaCy model: {model_name}...")
        try:
            spacy.cli.download(model_name)
            print(f"Successfully downloaded {model_name}")
        except Exception as e:
             print(f"Error downloading Spacy Model: {model_name} {e}")
             exit() #Exit program if download does not succeed