MAX_CODE_LINES = 40

class CodeGenerator:
    def __init__(self):
        pass

    def generate_code(self, nlp_data):
        # Replace this with your code generation logic.
        code = ""
        if "create" in nlp_data["verb"]:
            if "button" in nlp_data["noun"]:
                code = """
from kivy.uix.button import Button
button = Button(text='Hello from Kivy')
self.add_widget(button)
"""
            elif "label" in nlp_data["noun"]:
                code = """
from kivy.uix.label import Label
label = Label(text='Hello from
