# main.py
# Entry point for the Cluedo -- Digital Edition.
# Run with:  python main.py

from cards import CHARACTERS, CHARACTER_STARTING_ROOMS
from story import ASCII_BANNER, INTRO_TEXT, CHARACTER_INTROS, dramatic_print
from game import Game


def _pick_int(lo, hi):
    """Read a validated integer in [lo, hi] from stdin (no cancel option)."""
    while True:
        raw = input(f"  Enter a number ({lo}-{hi}): ").strip()
        try:
            value = int(raw)
            if lo <= value <= hi:
                return value
            print(f"  Please enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Please enter a valid number.")


def main():
    # ── Opening story ─────────────────────────────────────────────────
    dramatic_print(INTRO_TEXT)
    print(ASCII_BANNER)

    # ── Detective name ────────────────────────────────────────────────
    name = input("  Enter your detective name: ").strip()
    if not name:
        name = "Detective"

    # ── Character selection ───────────────────────────────────────────
    print("\n  Choose your suspect identity:")
    print("  (You will start the game in that character's canonical room.)\n")
    for i, char_name in enumerate(CHARACTERS, 1):
        start = CHARACTER_STARTING_ROOMS[char_name]
        intro = CHARACTER_INTROS.get(char_name, "")
        print(f"  {i}. {char_name:<22} (starts in {start:<14})  {intro}")

    print()
    choice = _pick_int(1, len(CHARACTERS))
    chosen_character = CHARACTERS[choice - 1]
    chosen_start     = CHARACTER_STARTING_ROOMS[chosen_character]

    print(
        f"\n  You are playing as {chosen_character},"
        f" starting in the {chosen_start}.\n"
    )

    # ── Start the game ────────────────────────────────────────────────
    game = Game(player_name=name, character_name=chosen_character)
    game.run()


if __name__ == "__main__":
    main()
