# cards.py
# Card data for Cluedo: suspect names, weapons, rooms, and helper classes.

# The six classic suspects (plain strings used for solution selection and menus)
CHARACTERS = [
    "Miss Scarlett",
    "Colonel Mustard",
    "Mrs. White",
    "Mr. Green",
    "Mrs. Peacock",
    "Professor Plum",
]

# Alias used by the notebook and other modules that need the name list
CHARACTERS_NAMES = CHARACTERS

# Each suspect's canonical starting room (used for character selection)
CHARACTER_STARTING_ROOMS = {
    "Miss Scarlett":   "Hall",
    "Colonel Mustard": "Lounge",
    "Mrs. White":      "Kitchen",
    "Mr. Green":       "Billiard Room",
    "Mrs. Peacock":    "Library",
    "Professor Plum":  "Study",
}

# The six murder weapons
WEAPONS = [
    "Candlestick",
    "Revolver",
    "Rope",
    "Lead Pipe",
    "Knife",
    "Wrench",
]

# The nine rooms in the mansion
ROOMS = [
    "Kitchen",
    "Ballroom",
    "Conservatory",
    "Dining Room",
    "Billiard Room",
    "Library",
    "Lounge",
    "Hall",
    "Study",
]


class Character:
    """A suspect NPC placed in the mansion (holds a Room object as starting_room)."""

    def __init__(self, name, starting_room):
        self.name = name
        self.starting_room = starting_room  # Room object

    def __str__(self):
        return f"{self.name} (starts in {self.starting_room.name})"


class Weapon:
    """A murder weapon placed in a room at game start."""

    def __init__(self, name, room):
        self.name = name
        self.room = room  # Room object

    def __str__(self):
        return f"{self.name} (in {self.room.name})"
