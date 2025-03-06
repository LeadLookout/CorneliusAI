app/modules/personality.py
# FILE: cornelius_os/app/modules/personality.py

class Personality:
    def __init__(self, openness=0.5, conscientiousness=0.5, extraversion=0.5, agreeableness=0.5, neuroticism=0.5):
        self.traits = {
            "openness": openness,
            "conscientiousness": conscientiousness,
            "extraversion": extraversion,
            "agreeableness": agreeableness,
            "neuroticism": neuroticism,
        }

    def get_trait(self, trait_name):
        return self.traits.get(trait_name, None)

    def set_trait(self, trait_name, value):
        if trait_name in self.traits:
            if 0.0 <= value <= 1.0:
                self.traits[trait_name] = value
            else:
                print(f"Error: Trait value for {trait_name} must be between 0.0 and 1.0")
        else:
            print(f"Error: Invalid trait name: {trait_name}")

    def adjust_trait(self, trait_name, adjustment_factor, feedback_type):
        """
        Adjusts a personality trait based on feedback, within bounds.
        """
        if trait_name not in self.traits:
            print(f"Error: Invalid trait name: {trait_name}")
            return

        current_value = self.traits[trait_name]
        if feedback_type == 'positive':
          new_value = min(1.0, current_value + adjustment_factor)
        elif feedback_type == 'negative':
            new_value = max(0.0, current_value - adjustment_factor)
        else:
            print("Error: Invalid feedback type.")
            return

        self.traits[trait_name] = new_value
        print(f"Personality trait '{trait_name}' adjusted to: {new_value:.2f}")

    def describe_personality(self):
        descriptions = []
        for trait, value in self.traits.items():
            descriptions.append(f"{trait}: {value:.2f}")
        return ", ".join(descriptions)