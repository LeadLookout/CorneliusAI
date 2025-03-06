from app import modules, self_improver


app/modules/self_improver.py
# FILE: cornelius_os/app/modules/self_improver.py

import app
from app.modules.knowledge_base import knowledge_base #Importing like this prevents circular
from app.modules.developer_mode import developer_mode
import os
import ast
import shutil

BACKUP_FILE = "cornelius_backup.py"

class SelfImprover:
    def __init__(self):
      pass

    def analyze_feedback(self):
        """Analyzes user feedback and suggests improvements."""
        proposals = []
        feedback_data = knowledge_base.data.get("feedback", [])

        # Example 1:  Identify frequently rejected code patterns.
        rejected_snippets = [f for f in feedback_data if f["status"] == "rejected"]
        # (In a real system, you'd use more sophisticated analysis here,
        #  potentially involving NLP and code parsing.)
        if len(rejected_snippets) > 3:  # Arbitrary threshold
            proposals.append({
                "type": "code_generation",
                "target": "code_generator",  # The module to modify
                "description": "I've noticed that code snippets related to file saving have been frequently rejected.  I propose adjusting the `save_file` template.",
                "suggested_change": "# TODO:  Detailed code change suggestion (using diffs or AST manipulation)", #To be implemented
                "priority": "medium",
            })

        # Example 2: Detect error patterns
        error_history = knowledge_base.data.get("error_history", [])
        # (Analyze error messages and stack traces to identify common errors)

        return proposals

    def analyze_interactions(self):
      """Analyzes user interaction patterns."""
      proposals = []
      interaction_data = knowledge_base.data.get("interaction_history", [])

      #Example: Detect user preference for short explanations
      explanation_lengths = []
      for interaction in interaction_data:
          if "explanation_length" in interaction:
              explanation_lengths.append(interaction["explanation_length"])

      if explanation_lengths:  # Ensure list isn't empty before calculating average
          average_length = sum(explanation_lengths) / len(explanation_lengths)
          if average_length < 50:  # Example Threshold
              proposals.append({
                "type": "personality",
                "target": "personality",
                "description": "The user seems to prefer concise responses, reducing extraversion.",
                "suggested_change": "Adjust extraversion down by 0.1",
                "priority": "low"
              })
      return proposals;

    def propose_improvements(self):
        """Generates a list of improvement proposals."""
        proposals = []
        proposals.extend(self.analyze_feedback())
        proposals.extend(self.analyze_interactions())
        # Add other analysis methods here (e.g., analyzing code style)

        return proposals
    def apply_change(self, proposal):
      """Applies the approved self modification"""

      # --- Backup Key files ---
      try:
        shutil.copyfile("app/modules/code_generator.py", "app/modules/code_generator_backup.py")
        print(f"Backup created: app/modules/code_generator_backup.py.py")
        shutil.copyfile("app/modules/personality.py", "app/modules/personality_backup.py")
        print(f"Backup created: app/modules/personality_backup.py")
        shutil.copyfile("app/modules/nlp_engine.py", "app/modules/nlp_engine_backup.py")
        print(f"Backup created: app/modules/nlp_engine_backup.py")
        #Add other files here
      except Exception as e:
        print(f"Backup failed: {e}.  Proceeding without backup.")

      # --- Apply Changes ---
      if proposal["type"] == "code_generation":
          # Load the code_generator module
          with open("app/modules/code_generator.py", "r") as f:
              code = f.read()

          # Very basic change - Find and replace text.  Safer than ast.
          if proposal["target"] == "code_generator": #Ensure correct module
            new_code = code.replace("# TODO:  Detailed code change suggestion (using diffs or AST manipulation)", proposal["suggested_change"]) # Replace placeholder
            try:
                with open("app/modules/code_generator.py", "w") as f:
                    f.write(new_code)
                    print("Code change applied.")
            except Exception as e:
                print(f"Error modifying self: {e}")

      elif proposal["type"] == "personality":
          from app.modules.personality import personality
          if proposal["suggested_change"] == "Adjust extraversion down by 0.1":
            personality.adjust_trait("extraversion", 0.1, "negative")
          #Add more changes


      # Add other self modification types.
      else:
          print(f"Error: Unknown change type: {proposal['type']}")

    def run_self_improvement(self):
      """Runs the self improvement cycle."""
      #Check developer mode
      if not developer_mode.check_access():
          return

      print("Running self-improvement analysis...")
      proposals = self.propose_improvements()

      if not proposals:
          print("No improvement proposals found.")
          return

      for proposal in proposals:
          print("\n--- Self-Improvement Proposal ---")
          print(f"Type: {proposal['type']}")
          print(f"Description: {proposal['description']}")
          print(f"Suggested Change: {proposal['suggested_change']}")
          while True:
            approval = input("Approve this change? (yes/no/view): ").lower()
            if approval == 'yes':
                self.apply_change(proposal)
                break
            elif approval == 'no':
                print("Change rejected.")
                break
            elif approval == 'view':
                #Add view option
                if proposal["type"] == 'code_generation':
                    print("-" * 20)
                    with open("app/modules/code_generator.py", 'r') as file:
                        print(file.read())
                    print("-" * 20)
                elif proposal['type'] == 'personality':
                    from app.modules.personality import personality
                    print("-" * 20)
                    print