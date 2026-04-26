# notebook.py
# The detective's notebook: tracks which suspects, weapons, and rooms
# have been ruled out or confirmed based on suggestion feedback.

class Notebook:
    """
    Maintains the investigation record.

    Status codes:
        "?"  Unknown -- not yet eliminated or confirmed
        "X"  Ruled out -- the element was proven wrong in a suggestion
        "!"  Confirmed -- all three elements of a suggestion matched
    """

    def __init__(self, suspects, weapons, rooms):
        self.suspects = list(suspects)
        self.weapons  = list(weapons)
        self.rooms    = list(rooms)
        self.s_status = {n: "?" for n in suspects}
        self.w_status = {n: "?" for n in weapons}
        self.r_status = {n: "?" for n in rooms}
        self.notes    = []

    # ------------------------------------------------------------------
    # Marking helpers
    # ------------------------------------------------------------------

    def mark_suspect(self, name, status="X"):
        if name in self.s_status:
            self.s_status[name] = status

    def mark_weapon(self, name, status="X"):
        if name in self.w_status:
            self.w_status[name] = status

    def mark_room(self, name, status="X"):
        if name in self.r_status:
            self.r_status[name] = status

    def add_note(self, text):
        self.notes.append(text)

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def display(self):
        width = 56
        print("\n" + "=" * width)
        print("              DETECTIVE'S NOTEBOOK")
        print("=" * width)

        self._print_section("SUSPECTS",  self.suspects,  self.s_status)
        self._print_section("WEAPONS",   self.weapons,   self.w_status)
        self._print_section("ROOMS",     self.rooms,     self.r_status)

        if self.notes:
            print("\n  PERSONAL NOTES:")
            for i, note in enumerate(self.notes, 1):
                print(f"    {i}. {note}")

        print("\n" + "-" * width)
        print("  [?] Unknown   [X] Ruled out   [!] Confirmed")
        print("=" * width)

    def _print_section(self, title, items, status):
        print(f"\n  {title}:")
        # Print in two columns
        for i in range(0, len(items), 2):
            left_name  = items[i]
            left_mark  = status[left_name]
            left_cell  = f"[{left_mark}] {left_name:<20}"
            if i + 1 < len(items):
                right_name = items[i + 1]
                right_mark = status[right_name]
                right_cell = f"[{right_mark}] {right_name}"
            else:
                right_cell = ""
            print(f"    {left_cell}  {right_cell}")
