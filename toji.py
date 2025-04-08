class Toji:
    def __init__(self):
        """
        Initialize Toji with a default skill.
        """
        self.skill = "Heavenly Restriction"

    def infiltrate(self, target=None):
        """
        Use Toji's Heavenly Restriction skill to infiltrate.

        Parameters:
        target (str, optional): The target to infiltrate.

        Returns:
        str: A message indicating the infiltration action.
        """
        try:
            if target is not None and not isinstance(target, str):
                raise ValueError("Target must be a string.")
            
            if target:
                message = f"Toji uses Heavenly Restriction to infiltrate {target}!"
            else:
                message = "Toji uses Heavenly Restriction to infiltrate!"
            
            print(message)
            return message
        except Exception as e:
            print(f"Error in infiltrate method: {e}")
            return None

    def change_skill(self, new_skill):
        """
        Change Toji's skill.

        Parameters:
        new_skill (str): The new skill to be used by Toji.

        Returns:
        str: A message indicating the skill change.
        """
        try:
            if not isinstance(new_skill, str) or not new_skill:
                raise ValueError("Skill must be a non-empty string.")
            self.skill = new_skill
            message = f"Toji's skill changed to {self.skill}."
            print(message)
            return message
        except Exception as e:
            print(f"Error in change_skill method: {e}")
            return None

if __name__ == "__main__":
    toji = Toji()
    toji.infiltrate()
    toji.infiltrate("target_system")
    toji.change_skill("Cursed Energy Manipulation")
    toji.infiltrate("target_system")