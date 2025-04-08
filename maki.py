class Maki:
    def __init__(self):
        """
        Initialize Maki with a default weapon.
        """
        self.weapon = "Cursed Tools"

    def combat(self):
        """
        Engage in combat using Maki's weapon.
        """
        try:
            print(f"Maki engages in combat with {self.weapon}!")
        except Exception as e:
            print(f"Error in combat method: {e}")

    def change_weapon(self, new_weapon):
        """
        Change Maki's weapon.

        Parameters:
        new_weapon (str): The new weapon to be used by Maki.
        """
        try:
            if not isinstance(new_weapon, str) or not new_weapon:
                raise ValueError("Weapon must be a non-empty string.")
            self.weapon = new_weapon
            print(f"Maki's weapon changed to {self.weapon}.")
        except Exception as e:
            print(f"Error in change_weapon method: {e}")

if __name__ == "__main__":
    maki = Maki()
    maki.combat()
    maki.change_weapon("Dragon Bone")
    maki.combat()