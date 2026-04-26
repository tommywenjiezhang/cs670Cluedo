# game.py
# Core game logic: setup, menu loop, dice movement, suggestions,
# accusation (the only win/loss path), and notebook management.

import random

from mansion import Mansion
from player import Player
from cards import (
    CHARACTERS, CHARACTERS_NAMES, WEAPONS, ROOMS,
    CHARACTER_STARTING_ROOMS, Character, Weapon,
)
from notebook import Notebook
from dice import DiceRoll
from story import (
    ROOM_DESCRIPTIONS, SUGGESTION_FLAVOUR,
    dramatic_print, WIN_TEXT, LOSE_TEXT,
)


class Game:
    """
    Orchestrates one play-through of the enhanced Cluedo game.

    Key additions over Part 1 baseline:
      - Character selection (player chooses a suspect identity)
      - Dice-based movement with step counting
      - First-visit room descriptions
      - Detective notebook with auto-marking
      - Accusation as the only win/lose path (suggestions gather clues)
      - Win and lose story endings
    """

    def __init__(self, player_name, character_name):
        self.mansion    = Mansion()
        self.solution   = self._select_solution()
        self.characters = self._place_characters()
        self.weapons    = self._place_weapons()

        # Player starts in their chosen character's canonical room
        start_room = self.mansion.get_room(
            CHARACTER_STARTING_ROOMS[character_name]
        )
        self.player    = Player(player_name, start_room)
        self.character_name = character_name

        self.notebook  = Notebook(CHARACTERS_NAMES, WEAPONS, ROOMS)
        self.turn      = 0
        self.solved    = False   # loop exit flag
        self.won       = False   # True = player won, False = lost

        # Show the description of the starting room immediately
        print(f"\n  You begin your investigation in the {start_room.name}.")
        print(f"  {ROOM_DESCRIPTIONS.get(start_room.name, '')}")

    # ------------------------------------------------------------------
    # Setup helpers
    # ------------------------------------------------------------------

    def _select_solution(self):
        return {
            "character": random.choice(CHARACTERS),
            "weapon":    random.choice(WEAPONS),
            "room":      random.choice(ROOMS),
        }

    def _place_characters(self):
        result = []
        for name in CHARACTERS:
            room = self.mansion.get_room(CHARACTER_STARTING_ROOMS[name])
            result.append(Character(name, room))
        return result

    def _place_weapons(self):
        room_list = list(self.mansion.rooms.values())
        random.shuffle(room_list)
        result = []
        for i, name in enumerate(WEAPONS):
            result.append(Weapon(name, room_list[i % len(room_list)]))
        return result

    # ------------------------------------------------------------------
    # Display helpers
    # ------------------------------------------------------------------

    def _print_header(self, title):
        width = 52
        print("\n" + "=" * width)
        print(f"  {title}")
        print(f"  Turn {self.turn}  |  Playing as: {self.character_name}")
        print("=" * width)

    def _show_characters(self):
        self._print_header("SUSPECTS IN THE MANOR")
        for i, char in enumerate(self.characters, 1):
            print(f"  {i}. {char.name:<22} (starts in {char.starting_room.name})")

    def _show_weapons(self):
        self._print_header("MURDER WEAPONS")
        for i, weapon in enumerate(self.weapons, 1):
            print(f"  {i}. {weapon.name}")

    def _show_notebook(self):
        self.notebook.display()

    def _show_room_description(self):
        room_name = self.player.get_location()
        desc = ROOM_DESCRIPTIONS.get(room_name, "")
        print(f"\n  -- {room_name} --")
        if desc:
            print(f"  {desc}")
        else:
            print(f"  You look around. Nothing unusual catches your eye.")

    # ------------------------------------------------------------------
    # Input helpers
    # ------------------------------------------------------------------

    def _read_int(self, prompt, lo, hi):
        """Read an integer in [lo, hi]; return None if 0 or invalid."""
        raw = input(prompt).strip()
        if raw == "0":
            print("  Cancelled.")
            return None
        try:
            value = int(raw)
        except ValueError:
            print("  Invalid input -- please enter a number.")
            return None
        if not (lo <= value <= hi):
            print(f"  Please enter a number between {lo} and {hi} (or 0 to cancel).")
            return None
        return value

    def _read_yes_no(self, prompt):
        """Loop until the user enters y or n; return the boolean."""
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("  Please type 'y' or 'n'.")

    # ------------------------------------------------------------------
    # Movement (dice-based)
    # ------------------------------------------------------------------

    def _move(self):
        """
        Roll 2d6 and let the player spend steps to hop between rooms.
        Each hop costs 1 step. Secret passages are free.
        The player can stop early by entering 0.
        """
        dice = DiceRoll.roll()
        dice.display()
        self.turn += 1

        visited_this_turn = {self.player.get_location()}

        while dice.steps_remaining > 0:
            current = self.player.get_location()

            # Build exit list excluding rooms already visited this turn
            all_exits = self.player.current_room.get_connections()
            exits = [r for r in all_exits if r not in visited_this_turn]

            # Secret passage detection
            SECRET_PASSAGES = {
                "Kitchen": "Study",
                "Study":   "Kitchen",
                "Lounge":  "Conservatory",
                "Conservatory": "Lounge",
            }
            passage_dest = SECRET_PASSAGES.get(current)
            has_passage  = (
                passage_dest is not None
                and passage_dest not in visited_this_turn
            )

            if not exits and not has_passage:
                print("  No accessible rooms remain. Remaining steps forfeit.")
                break

            print(f"\n  Steps remaining: {dice.steps_remaining}")
            print("  Where would you like to go?")
            for i, room_name in enumerate(exits, 1):
                print(f"    {i}. {room_name}")
            if has_passage:
                print(f"    P. Take secret passage to {passage_dest}  (free -- no step cost)")
            print("    0. Stop moving")

            choice = input("  Enter choice: ").strip().lower()

            if choice == "0":
                break

            if choice == "p" and has_passage:
                dest_room = self.mansion.get_room(passage_dest)
                is_new = passage_dest not in self.player.visited_rooms
                visited_this_turn.add(passage_dest)
                self.player.move_to(dest_room)
                print(f"\n  You slip through the secret passage to the {passage_dest}.")
                if is_new:
                    print(f"\n  {ROOM_DESCRIPTIONS.get(passage_dest, '')}")
                if dice.steps_remaining == 0:
                    break
                if not self._read_yes_no("  Continue moving? (y/n): "):
                    break
                continue

            try:
                idx = int(choice) - 1
            except ValueError:
                print("  Invalid choice -- enter a number, 'P' for passage, or 0 to stop.")
                continue

            if not (0 <= idx < len(exits)):
                print(f"  Please enter a number between 1 and {len(exits)}.")
                continue

            dest_name = exits[idx]
            dest_room = self.mansion.get_room(dest_name)
            is_new    = dest_name not in self.player.visited_rooms
            visited_this_turn.add(dest_name)
            self.player.move_to(dest_room)
            dice.use_step()
            print(f"\n  You move to the {dest_name}.")
            if is_new:
                print(f"\n  {ROOM_DESCRIPTIONS.get(dest_name, '')}")

            if dice.steps_remaining == 0:
                print("  You have used all your steps.")
                break
            if not self._read_yes_no("  Continue moving? (y/n): "):
                break

    # ------------------------------------------------------------------
    # Suggestions
    # ------------------------------------------------------------------

    def _make_suggestion(self):
        """
        The player names a suspect and weapon; the room is fixed to the
        current location. Feedback uses flavour text and auto-updates the
        notebook. Suggestions can NEVER win the game -- use Accuse for that.
        """
        current_room = self.player.get_location()
        self._print_header("MAKE A SUGGESTION")
        print(f"  Room: {current_room}  (fixed to your current location)\n")

        print("  Choose a suspect:")
        for i, name in enumerate(CHARACTERS, 1):
            print(f"    {i}. {name}")
        print("    0. Cancel")
        char_idx = self._read_int("  Suspect number: ", 1, len(CHARACTERS))
        if char_idx is None:
            return
        chosen_char = CHARACTERS[char_idx - 1]

        print("\n  Choose a weapon:")
        for i, name in enumerate(WEAPONS, 1):
            print(f"    {i}. {name}")
        print("    0. Cancel")
        weapon_idx = self._read_int("  Weapon number: ", 1, len(WEAPONS))
        if weapon_idx is None:
            return
        chosen_weapon = WEAPONS[weapon_idx - 1]

        print(
            f"\n  >> I suggest it was {chosen_char} "
            f"with the {chosen_weapon} in the {current_room}."
        )

        sol          = self.solution
        char_match   = chosen_char   == sol["character"]
        weapon_match = chosen_weapon == sol["weapon"]
        room_match   = current_room  == sol["room"]
        wrong        = []

        if not char_match:
            wrong.append("suspect")
            self.notebook.mark_suspect(chosen_char)
        if not weapon_match:
            wrong.append("weapon")
            self.notebook.mark_weapon(chosen_weapon)
        if not room_match:
            wrong.append("room")
            self.notebook.mark_room(current_room)

        print()
        if not wrong:
            # All three match -- clue confirmed in notebook, but no win yet
            print(f"  {SUGGESTION_FLAVOUR['match']}")
            print("  Record it in your notebook and make your Accusation to close the case.")
            self.notebook.mark_suspect(chosen_char,   "!")
            self.notebook.mark_weapon(chosen_weapon,  "!")
            self.notebook.mark_room(current_room,     "!")
        elif len(wrong) == 3:
            print(f"  {SUGGESTION_FLAVOUR['all']}")
            self.notebook.add_note(
                f"Turn {self.turn}: {chosen_char}, {chosen_weapon}, {current_room} -- all wrong."
            )
        else:
            for element in wrong:
                print(f"  {SUGGESTION_FLAVOUR[element]}")
            self.notebook.add_note(
                f"Turn {self.turn}: {chosen_char}, {chosen_weapon}, {current_room}"
                f" -- {', '.join(wrong)} wrong."
            )

    # ------------------------------------------------------------------
    # Accusation (the only win/lose path)
    # ------------------------------------------------------------------

    def _make_accusation(self):
        """
        Final accusation: the player names suspect, weapon, AND room.
        Correct = WIN story. Incorrect = LOSE story. Game ends either way.
        """
        self._print_header("FINAL ACCUSATION")
        print("\n  WARNING: You only get ONE accusation.")
        print("  If you are wrong, the investigation is over.\n")

        if not self._read_yes_no("  Are you ready to make your accusation? (y/n): "):
            print("  Wise. Keep gathering evidence.")
            return

        print("\n  Choose the suspect:")
        for i, name in enumerate(CHARACTERS, 1):
            print(f"    {i}. {name}")
        print("    0. Cancel")
        char_idx = self._read_int("  Suspect number: ", 1, len(CHARACTERS))
        if char_idx is None:
            return
        chosen_char = CHARACTERS[char_idx - 1]

        print("\n  Choose the weapon:")
        for i, name in enumerate(WEAPONS, 1):
            print(f"    {i}. {name}")
        print("    0. Cancel")
        weapon_idx = self._read_int("  Weapon number: ", 1, len(WEAPONS))
        if weapon_idx is None:
            return
        chosen_weapon = WEAPONS[weapon_idx - 1]

        print("\n  Choose the room:")
        for i, name in enumerate(ROOMS, 1):
            print(f"    {i}. {name}")
        print("    0. Cancel")
        room_idx = self._read_int("  Room number: ", 1, len(ROOMS))
        if room_idx is None:
            return
        chosen_room = ROOMS[room_idx - 1]

        print(
            f"\n  You accuse: {chosen_char} with the {chosen_weapon}"
            f" in the {chosen_room}."
        )
        print()

        sol = self.solution
        if (chosen_char   == sol["character"] and
                chosen_weapon == sol["weapon"] and
                chosen_room   == sol["room"]):
            dramatic_print(WIN_TEXT)
            self.solved = True
            self.won    = True
        else:
            print(
                f"  The truth: it was {sol['character']}"
                f" with the {sol['weapon']}"
                f" in the {sol['room']}."
            )
            print()
            dramatic_print(LOSE_TEXT)
            self.solved = True
            self.won    = False

    # ------------------------------------------------------------------
    # Quit
    # ------------------------------------------------------------------

    def _quit(self):
        sol = self.solution
        print(
            f"\n  The solution was: {sol['character']}"
            f" with the {sol['weapon']}"
            f" in the {sol['room']}."
        )
        print("  Thanks for playing!")
        self.solved = True

    # ------------------------------------------------------------------
    # Main game loop
    # ------------------------------------------------------------------

    def run(self):
        self._print_header("BLACKWELL MANOR -- Investigation Begins")
        print(f"\n  Detective : {self.player.name}")
        print(f"  Identity  : {self.character_name}")
        print("  Gather clues with Suggestions.")
        print("  You have ONE Accusation -- make it count.\n")

        while not self.solved:
            self.player.show_location()
            self._print_header("WHAT WILL YOU DO?")
            print("  1. Move  (roll dice)")
            print("  2. Make a Suggestion  (current room)")
            print("  3. Make an Accusation  [one chance -- win or lose!]")
            print("  4. View Detective's Notebook")
            print("  5. View Room Description")
            print("  6. View Mansion Map")
            print("  7. View Characters")
            print("  8. View Weapons")
            print("  9. Quit")

            choice = input("\n  Your choice (1-9): ").strip()

            if choice == "1":
                self._move()
            elif choice == "2":
                self._make_suggestion()
            elif choice == "3":
                self._make_accusation()
            elif choice == "4":
                self._show_notebook()
            elif choice == "5":
                self._show_room_description()
            elif choice == "6":
                self.mansion.display_map(self.player.get_location())
            elif choice == "7":
                self._show_characters()
            elif choice == "8":
                self._show_weapons()
            elif choice == "9":
                self._quit()
            else:
                print("  Invalid choice -- please enter a number from 1 to 9.")
