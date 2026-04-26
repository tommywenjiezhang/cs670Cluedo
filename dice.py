# dice.py
# Provides the DiceRoll class for the Cluedo movement system.
# Each turn the player rolls 2d6; the total is the number of room-hops available.

import random

# ASCII art for each die face (5 lines, 7 chars wide).
FACES = {
    1: [
        "+-----+",
        "|     |",
        "|  o  |",
        "|     |",
        "+-----+",
    ],
    2: [
        "+-----+",
        "|o    |",
        "|     |",
        "|    o|",
        "+-----+",
    ],
    3: [
        "+-----+",
        "|o    |",
        "|  o  |",
        "|    o|",
        "+-----+",
    ],
    4: [
        "+-----+",
        "|o   o|",
        "|     |",
        "|o   o|",
        "+-----+",
    ],
    5: [
        "+-----+",
        "|o   o|",
        "|  o  |",
        "|o   o|",
        "+-----+",
    ],
    6: [
        "+-----+",
        "|o   o|",
        "|o   o|",
        "|o   o|",
        "+-----+",
    ],
}


class DiceRoll:
    """
    Result of rolling two six-sided dice.

    Attributes:
        die1, die2       : individual die values (1-6)
        total            : die1 + die2
        steps_remaining  : room-hops the player can still make this turn
    """

    def __init__(self, die1, die2):
        self.die1 = die1
        self.die2 = die2
        self.total = die1 + die2
        self.steps_remaining = self.total

    @staticmethod
    def roll():
        """Roll two random d6 and return a DiceRoll instance."""
        return DiceRoll(random.randint(1, 6), random.randint(1, 6))

    def use_step(self):
        """Consume one movement step."""
        if self.steps_remaining > 0:
            self.steps_remaining -= 1

    def display(self):
        """Print both dice side by side with the total."""
        f1 = FACES[self.die1]
        f2 = FACES[self.die2]
        print("\n  Rolling the dice...")
        for l1, l2 in zip(f1, f2):
            print(f"    {l1}   {l2}")
        print(f"\n    {self.die1} + {self.die2} = {self.total}  "
              f"-- You have {self.steps_remaining} step(s) to move.\n")
