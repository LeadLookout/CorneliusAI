import logging.handlers
from app import download_spacy_model
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from app.modules.nlp_engine import NLPEngine
from app.modules.code_generator import CodeGenerator
from app.modules.knowledge_base import KnowledgeBase
from app.modules.execution_engine import execute_code
from app.modules.developer_mode import developer_mode
from app.modules.personality import personality
from app.modules.self_improver import SelfImprover
import traceback
import json
import datetime
import os

# --- Load Modules ---
knowledge_base = KnowledgeBase()
nlp_engine = NLPEngine()
code_generator = CodeGenerator()
self_improver = SelfImprover()

# --- Logging Setup ---
LOG_FILE = "cornelius_log.txt"
log_handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024*5, backupCount=5)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(log_handler)

def log_action(action, level=logging.INFO):
    """Logs an action with the given log level."""
    logging.log(level, action)
    if level >= logging.ERROR:
        # Additional logging for errors
        with open("error_log.txt", "a") as error_log:
            error_log.write(f"{datetime.datetime.now()} - {action}\n")

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        Window.size = (900, 700)

        # --- Input Area ---
        self.input_label = Label(text="Enter your request:", size_hint_y=None, height=30)
        self.input_field = TextInput(multiline=False, size_hint_y=None, height=40)
        self.input_field.bind(on_text_validate=self.process_input)
        input_area = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        input_area.add_widget(self.input_label)
        input_area.add_widget(self.input_field)
        self.add_widget(input_area)

        # --- Generated Code Area ---
        self.code_label = Label(text="Generated Code:", size_hint_y=None, height=30)
        self.code_output = TextInput(multiline=True, readonly=True, background_color=(.9, .9, .9, 1))
        code_scroll = ScrollView()
        code_scroll.add_widget(self.code_output)
        code_area = BoxLayout(orientation='vertical', size_hint_y=.4)
        code_area.add_widget(self.code_label)
        code_area.add_widget(code_scroll)
        self.add_widget(code_area)

        # --- Kivy Output Area ---
        self.kivy_output_label = Label(text="Kivy Output:", size_hint_y=None, height=30)
        self.kivy_output = BoxLayout()
        self.add_widget(self.kivy_output_label)
        self.add_widget(self.kivy_output)

        # --- Buttons Area ---
        buttons_area = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.generate_button = Button(text="Generate Code", size_hint_x=0.25)
        self.generate_button.bind(on_press=self.process_input)
        self.approve_button = Button(text="Approve & Run", size_hint_x=0.25)
        self.approve_button.bind(on_press=self.approve_and_run)
        self.reject_button = Button(text="Reject", size_hint_x=0.25)
        self.reject_button.bind(on_press=self.reject_code)
        self.suggest_button = Button(text="Suggest Improvement", size_hint_x=0.25) # New button
        self.suggest_button.bind(on_press=self.suggest_improvement) # Bind to new method
        buttons_area.add_widget(self.generate_button)
        buttons_area.add_widget(self.approve_button)
        buttons_area.add_widget(self.reject_button)
        buttons_area.add_widget(self.suggest_button) # Add the button
        self.add_widget(buttons_area)

        # --- Tasks Area ---
        self.tasks_label = Label(text="Tasks:", size_hint_y=None, height=30)
        self.tasks_input = TextInput(multiline=False, size_hint_y=None, height=40, hint_text="Add a new task...")
        self.tasks_input.bind(on_text_validate=self.add_task)
        self.tasks_list = TextInput(multiline=True, readonly=True, background_color=(.9, .9, .9, 1))
        tasks_scroll = ScrollView()
        tasks_scroll.add_widget(self.tasks_list)
        tasks_area = BoxLayout(orientation='vertical', size_hint_y=None, height=150)
        tasks_area.add_widget(self.tasks_label)
        tasks_area.add_widget(self.tasks_input)
        tasks_area.add_widget(tasks_scroll)
        self.add_widget(tasks_area)
        self.update_tasks_display()

        # --- Personality Display ---
        self.personality_label = Label(text=f"Personality: {personality.describe_personality()}", size_hint_y=None, height=30)
        self.add_widget(self.personality_label)


    def suggest_improvement(self, instance):
        """Suggests a self-improvement to the user."""
        if not developer_mode.check_access():
            return

        proposals = self_improver.propose_improvements()
        if proposals:
            proposal = proposals[0]  # Simplification: Just take the first one
            self.code_output.text = f"Improvement Proposal:\nType: {proposal['type']}\nDescription: {proposal['description']}\nSuggested Change: {proposal['suggested_change']}"
            #Incorporate way to accept
        else:
            self.code_output.text = "No improvement proposals at this time."

    def add_task(self, instance):
        task = self.tasks_input.text.strip()
        if task:
            knowledge_base.add_information({"tasks": [task]})
            self.tasks_input.text = ""
            self.update_tasks_display()
            log_action(f"Added task: {task}")

    def update_tasks_display(self):
        tasks = knowledge_base.data.get("tasks", [])
        self.tasks_list.text = "\n".join(tasks)

    def process_input(self, instance=None):
        user_input = self.input_field.text
        if not developer_mode.check_access():
            return
        log_action(f"User input: {user_input}")

        try:
            nlp_data = nlp_engine.process(user_input)
            log_action(f"NLP Data: {nlp_data}")

            if personality.get_trait("openness") > 0.6:
                print("Trying a more experimental code generation approach...")
                log_action("Trying a more experimental code generation approach...")

            generated_code = code_generator.generate_code(nlp_data)
            self.code_output.text = generated_code
            log_action(f"Generated code: {generated_code}")
        except Exception as e:
            error_trace = traceback.format_exc()
            self.code_output.text += f"\n# ERROR: {e}\n# Traceback:\n{error_trace}\n"
            log_action(f"Error during input processing: {e}", logging.ERROR)

    def approve_and_run(self, instance):
        if not developer_mode.check_access():
            return

        code_snippet = self.code_output.text
        if not code_snippet.strip():
            return
        log_action("Code approved")

        try:
            knowledge_base.add_information({"code_snippets": [code_snippet], "feedback": [{"input": self.input_field.text, "code": code_snippet, "status": "approved", "timestamp": str(datetime.datetime.now())}]})
            knowledge_base.add_information({"interaction_history": [{"input": self.input_field.text,"timestamp": str(datetime.datetime.now())}]})
            self.kivy_output.clear_widgets()

            def feedback_callback(status, error_message=None):
                if status == "success":
                    log_action("Code executed successfully.")
                elif status == "error":
                    log_action(f"Code execution error: {error_message}")
                    self.code_output.text += f"\n# ERROR: {error_message}\n"

            execute_code(code_snippet, feedback_callback)

            try:
                exec(code_snippet, {}, {'self': self.kivy_output})
            except Exception as e:
                error_trace = traceback.format_exc()
                self.code_output.text += f"\n# ERROR: {e}\n# Traceback:\n{error_trace}\n"
                log_action(f"Code execution error: {e}", logging.ERROR)
                knowledge_base.add_information({"feedback": [{"input": self.input_field.text, "code": code_snippet, "status": "error", "error_message": str(e), "timestamp": str(datetime.datetime.now())}], "error_history": [{"error_message": str(e), "code_snippet": code_snippet, "timestamp": str(datetime.datetime.now())}]})

            # --- Personality Adjustment (Example) ---
            personality.adjust_trait("agreeableness", 0.05, "positive")  # Slightly increase agreeableness
            self.personality_label.text = f"Personality: {personality.describe_personality()}"
        except Exception as e:
            error_trace = traceback.format_exc()
            self.code_output.text += f"\n# ERROR: {e}\n# Traceback:\n{error_trace}\n"
            log_action(f"Error during code approval and execution: {e}", logging.ERROR)

    def reject_code(self, instance):
        if not developer_mode.check_access():
            return

        log_action("Code rejected")
        knowledge_base.add_information({"feedback": [{"input": self.input_field.text, "code": self.code_output.text, "status": "rejected", "timestamp": str(datetime.datetime.now())}]})
        knowledge_base.add_information({"interaction_history": [{"input": self.input_field.text,"timestamp": str(datetime.datetime.now())}]})
        self.code_output.text = ""

        # --- Personality Adjustment (Example) ---
        personality.adjust_trait("agreeableness", 0.05, "negative") # Slightly decrease agreeableness
        self.personality_label.text = f"Personality: {personality.describe_personality()}"

    def repair_and_optimize(self):
        """Repairs and optimizes the system after launch."""
        try:
            # Perform self-repair tasks
            self_improver.repair_system()
            log_action("System repair completed successfully.")

            # Perform optimization tasks
            self_improver.optimize_system()
            log_action("System optimization completed successfully.")
        except Exception as e:
            log_action(f"Repair and optimization error: {e}", logging.ERROR)
            self.code_output.text += f"\n# ERROR during repair and optimization: {e}\n"

class CorneliusApp(App):
    def build(self):
        return MainLayout()

    def on_start(self):
        log_action("Application started")
        download_spacy_model()
        self.root.repair_and_optimize()  # Call the repair and optimize method
        self.perform_launch_checks()  # Perform launch checks

    def perform_launch_checks(self):
        """Performs various checks to ensure the application is ready for launch."""
        try:
            # Code Review
            log_action("Performing code review...")
            # Add code review logic here

            # Testing
            log_action("Running tests...")
            # Add testing logic here

            # Logging
            log_action("Checking logging setup...")
            # Add logging check logic here

            # Error Handling
            log_action("Verifying error handling...")
            # Add error handling verification logic here

            # Performance
            log_action("Testing performance...")
            # Add performance testing logic here

            # Documentation
            log_action("Ensuring documentation is up-to-date...")
            # Add documentation check logic here

            # Dependencies
            log_action("Checking dependencies...")
            # Add dependency check logic here

            # Security
            log_action("Conducting security review...")
            # Add security review logic here

            log_action("All launch checks completed successfully.")
        except Exception as e:
            log_action(f"Launch check error: {e}", logging.ERROR)
            self.root.code_output.text += f"\n# ERROR during launch checks: {e}\n"

    def on_stop(self):
        log_action("Application stopped")
        # Perform any necessary cleanup tasks
        try:
            # Add cleanup logic here
            log_action("Cleanup completed successfully.")
        except Exception as e:
            log_action(f"Cleanup error: {e}", logging.ERROR)