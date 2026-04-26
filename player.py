# player.py
# Defines the Player class that tracks the detective's location in the mansion.


class Player:
    """
    Represents the human player moving through the mansion.

    Attributes:
        name          : display name entered at game start
        current_room  : the Room object the player currently occupies
        visited_rooms : set of room names the player has entered at least once
    """

    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.visited_rooms = {starting_room.name}

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def can_move_to(self, room_name):
        """Return True if room_name is directly connected to the current room."""
        return room_name in self.current_room.get_connections()

    def move_to(self, room):
        """Move the player to a new Room object and record the visit."""
        self.current_room = room
        self.visited_rooms.add(room.name)

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def get_location(self):
        """Return the name of the player's current room."""
        return self.current_room.name

    def show_location(self):
        """Print the current room and the list of connected rooms."""
        print(f"\n  Location : {self.current_room.name}")
        neighbours = self.current_room.get_connections()
        print(f"  Exits    : {', '.join(neighbours)}")

    def __str__(self):
        return f"{self.name} in {self.current_room.name}"
