# mansion.py
# Defines the Room and Mansion classes that model the game board.


class Room:
    """A single room in the mansion with a list of directly connected rooms."""

    def __init__(self, name):
        self.name = name
        self._connected = []  # list of Room objects

    def connect(self, other_room):
        """Create a two-way connection between this room and another."""
        if other_room not in self._connected:
            self._connected.append(other_room)
            other_room._connected.append(self)

    def get_connections(self):
        """Return a sorted list of connected room names."""
        return sorted(r.name for r in self._connected)

    def __str__(self):
        return self.name


class Mansion:
    """
    The full nine-room mansion.

    Layout (roughly follows the classic Clue board):

        [Kitchen]  ---  [Ballroom]  ---  [Conservatory]
            |                                   |
        [Dining Room]              [Billiard Room]
            |                           |
        [Lounge]  ---  [Hall]  ---  [Library]
                          |               |
                        [Study] ----------+

    Secret passages (diagonal shortcuts on the classic board):
        Kitchen  <-->  Study
        Lounge   <-->  Conservatory
    """

    def __init__(self):
        self.rooms = {}
        self._build_rooms()
        self._build_connections()

    # ------------------------------------------------------------------
    # Internal setup helpers
    # ------------------------------------------------------------------

    def _build_rooms(self):
        names = [
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
        for name in names:
            self.rooms[name] = Room(name)

    def _build_connections(self):
        adjacencies = [
            # Top row
            ("Kitchen", "Ballroom"),
            ("Ballroom", "Conservatory"),
            # Left column
            ("Kitchen", "Dining Room"),
            # Right column
            ("Conservatory", "Billiard Room"),
            ("Billiard Room", "Library"),
            ("Billiard Room", "Hall"),
            # Bottom row
            ("Dining Room", "Lounge"),
            ("Lounge", "Hall"),
            ("Hall", "Study"),
            ("Library", "Study"),
            # Secret passages (corner shortcuts)
            ("Kitchen", "Study"),
            ("Lounge", "Conservatory"),
        ]
        for a, b in adjacencies:
            self.rooms[a].connect(self.rooms[b])

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_room(self, name):
        """Return the Room object for the given name, or None if not found."""
        return self.rooms.get(name)

    def display_map(self, current_room=None):
        """Print the mansion as a fixed ASCII grid, marking the current room."""

        def tag(name, abbrev):
            if name == current_room:
                return f"[*{abbrev:<8}]"   # 11 chars, star marker
            return f"[ {abbrev:<8}]"        # 11 chars, space filler

        K  = tag("Kitchen",       "Kitchen")
        Ba = tag("Ballroom",      "Ballroom")
        Co = tag("Conservatory",  "Conserv.")
        Di = tag("Dining Room",   "DiningRm")
        Bi = tag("Billiard Room", "Billiard")
        Lo = tag("Lounge",        "Lounge  ")
        Ha = tag("Hall",          "  Hall  ")
        Li = tag("Library",       "Library ")
        St = tag("Study",         " Study  ")

        print("\n  BLACKWELL MANOR -- FLOOR PLAN")
        print("  " + "=" * 54)
        print(f"  {K}---{Ba}---{Co}")
        print(f"      |                              |")
        print(f"  {Di}                    {Bi}")
        print(f"      |                         |   |")
        print(f"  {Lo}---{Ha}---+  {Li}")
        print(f"                       |               |")
        print(f"                   {St}----------+")
        print()
        print("  Secret passages:  Kitchen <~~> Study")
        print("                    Lounge  <~~> Conservatory")
        if current_room:
            print(f"  (*) = {current_room}")
        print("  " + "=" * 54)
