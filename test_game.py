# test_game.py
# Automated test suite for Cluedo -- Enhanced Edition.
# Run with:  python test_game.py
#
# Each test prints PASS or FAIL. A summary line shows the final counts.

import sys
import io
import random

import story
story.FAST_MODE = True   # disable typewriter delay in all tests

from cards import (
    CHARACTERS, CHARACTERS_NAMES, WEAPONS, ROOMS,
    CHARACTER_STARTING_ROOMS, Character, Weapon,
)
from mansion import Room, Mansion
from player import Player
from game import Game
from notebook import Notebook
from dice import DiceRoll

# ---------------------------------------------------------------------------
# Test runner helpers
# ---------------------------------------------------------------------------

_results = []


def make_game(player_name="Tester"):
    """Create a standard game with Miss Scarlett (starts in Hall)."""
    return Game(player_name, "Miss Scarlett")


def test(name, condition, fail_msg=""):
    if condition:
        _results.append((name, True, ""))
        print(f"  PASS  {name}")
    else:
        _results.append((name, False, fail_msg))
        print(f"  FAIL  {name}")
        if fail_msg:
            print(f"        {fail_msg}")


def section(title):
    print(f"\n{'-' * 55}")
    print(f"  {title}")
    print(f"{'-' * 55}")


# ---------------------------------------------------------------------------
# 1. Card Data
# ---------------------------------------------------------------------------

def test_card_data():
    section("1. Card Data (cards.py)")

    test("Six suspects defined",
         len(CHARACTERS) == 6,
         f"Expected 6, got {len(CHARACTERS)}")

    test("Six weapons defined",
         len(WEAPONS) == 6,
         f"Expected 6, got {len(WEAPONS)}")

    test("Nine rooms defined",
         len(ROOMS) == 9,
         f"Expected 9, got {len(ROOMS)}")

    test("Miss Scarlett in suspect list",   "Miss Scarlett"  in CHARACTERS)
    test("Professor Plum in suspect list",  "Professor Plum" in CHARACTERS)
    test("Rope in weapon list",             "Rope"           in WEAPONS)
    test("Wrench in weapon list",           "Wrench"         in WEAPONS)
    test("Library in room list",            "Library"        in ROOMS)

    test("No duplicate suspects",
         len(CHARACTERS) == len(set(CHARACTERS)))
    test("No duplicate weapons",
         len(WEAPONS) == len(set(WEAPONS)))

    test("CHARACTERS_NAMES is same as CHARACTERS",
         CHARACTERS_NAMES is CHARACTERS)

    test("CHARACTER_STARTING_ROOMS has 6 entries",
         len(CHARACTER_STARTING_ROOMS) == 6)

    test("All suspects have a starting room",
         all(c in CHARACTER_STARTING_ROOMS for c in CHARACTERS))

    # Character class (still accepts a Room object)
    mansion = Mansion()
    room = mansion.get_room("Hall")
    char = Character("Test Char", room)
    test("Character stores name",          char.name == "Test Char")
    test("Character stores starting room", char.starting_room.name == "Hall")

    # Weapon class
    weapon = Weapon("Test Weapon", room)
    test("Weapon stores name", weapon.name == "Test Weapon")
    test("Weapon stores room", weapon.room.name == "Hall")


# ---------------------------------------------------------------------------
# 2. Mansion Layout
# ---------------------------------------------------------------------------

def test_mansion():
    section("2. Mansion Layout (mansion.py)")

    mansion = Mansion()

    test("Mansion has 9 rooms",     len(mansion.rooms) == 9)
    test("All named rooms exist",   all(name in mansion.rooms for name in ROOMS))

    for name in ROOMS:
        room = mansion.get_room(name)
        test(f"Room '{name}' has at least one exit",
             len(room.get_connections()) >= 1)

    kitchen = mansion.get_room("Kitchen")
    test("Kitchen connects to Ballroom",    "Ballroom"   in kitchen.get_connections())
    test("Kitchen connects to Dining Room", "Dining Room" in kitchen.get_connections())

    test("Secret passage: Kitchen <-> Study",
         "Study"   in kitchen.get_connections() and
         "Kitchen" in mansion.get_room("Study").get_connections())

    test("Secret passage: Lounge <-> Conservatory",
         "Conservatory" in mansion.get_room("Lounge").get_connections() and
         "Lounge"       in mansion.get_room("Conservatory").get_connections())

    hall    = mansion.get_room("Hall")
    billiard= mansion.get_room("Billiard Room")
    test("Connections are bidirectional (Hall <-> Billiard Room)",
         "Billiard Room" in hall.get_connections() and
         "Hall"          in billiard.get_connections())

    test("get_room returns None for unknown name",
         mansion.get_room("Dungeon") is None)

    connections = hall.get_connections()
    test("get_connections returns a sorted list",
         connections == sorted(connections))


# ---------------------------------------------------------------------------
# 3. Player Movement
# ---------------------------------------------------------------------------

def test_player():
    section("3. Player Movement (player.py)")

    mansion = Mansion()
    hall    = mansion.get_room("Hall")
    study   = mansion.get_room("Study")
    kitchen = mansion.get_room("Kitchen")

    player = Player("Wenjie", hall)

    test("Player starts in correct room",          player.get_location() == "Hall")
    test("Player name stored correctly",           player.name == "Wenjie")
    test("Starting room in visited_rooms",         "Hall" in player.visited_rooms)

    test("can_move_to returns True for adjacent",  player.can_move_to("Study"))
    test("can_move_to returns False for non-adj",  not player.can_move_to("Kitchen"))

    player.move_to(study)
    test("Player location updates after move",     player.get_location() == "Study")
    test("Study added to visited_rooms",           "Study" in player.visited_rooms)

    test("Secret passage accessible from Study",   player.can_move_to("Kitchen"))

    player.move_to(kitchen)
    test("Player can traverse secret passage",     player.get_location() == "Kitchen")

    player2 = Player("Test", hall)
    test("Cannot move to Ballroom from Hall",      not player2.can_move_to("Ballroom"))


# ---------------------------------------------------------------------------
# 4. Solution Selection
# ---------------------------------------------------------------------------

def test_solution():
    section("4. Solution Selection (game.py)")

    # Suppress __init__ output for batch game creation
    for i in range(20):
        buf = io.StringIO(); sys.stdout = buf
        g = make_game()
        sys.stdout = sys.__stdout__
        sol = g.solution

        test(f"Run {i+1}: solution character is valid",
             sol["character"] in CHARACTERS,
             f"Got: {sol['character']}")
        test(f"Run {i+1}: solution weapon is valid",
             sol["weapon"] in WEAPONS,
             f"Got: {sol['weapon']}")
        test(f"Run {i+1}: solution room is valid",
             sol["room"] in ROOMS,
             f"Got: {sol['room']}")

    solutions = []
    for _ in range(50):
        buf = io.StringIO(); sys.stdout = buf
        g = make_game()
        sys.stdout = sys.__stdout__
        solutions.append(
            (g.solution["character"], g.solution["weapon"], g.solution["room"])
        )
    test("Solutions vary across runs (randomness check)",
         len(set(solutions)) > 1,
         f"All 50 runs identical: {solutions[0]}")


# ---------------------------------------------------------------------------
# 5. Suggestion Matching
# ---------------------------------------------------------------------------

def test_suggestions():
    section("5. Suggestion Matching (game.py)")

    random.seed(42)
    buf = io.StringIO(); sys.stdout = buf
    g = make_game()
    sys.stdout = sys.__stdout__

    sol = g.solution

    # Move player to the solution room
    target_room = g.mansion.get_room(sol["room"])
    g.player.move_to(target_room)

    def run_suggestion(char_idx, weapon_idx):
        sys.stdin = io.StringIO(f"{char_idx}\n{weapon_idx}\n")
        buf = io.StringIO(); sys.stdout = buf
        g._make_suggestion()
        sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
        return buf.getvalue()

    char_idx   = CHARACTERS.index(sol["character"]) + 1
    weapon_idx = WEAPONS.index(sol["weapon"]) + 1

    # -- Correct suggestion: solved stays False (need accusation to win) --
    g.solved = False
    output = run_suggestion(char_idx, weapon_idx)

    test("Correct suggestion: solved flag remains False",
         not g.solved,
         "Suggestions should not end the game -- use Accusation")

    test("Correct suggestion: clue-match flavour shown",
         "aligns" in output.lower() or "pulse" in output.lower(),
         f"Output was:\n{output}")

    # -- Wrong suspect --
    wrong_char_idx = (char_idx % len(CHARACTERS)) + 1
    g.solved = False
    output = run_suggestion(wrong_char_idx, weapon_idx)

    test("Wrong suspect: solved flag remains False", not g.solved)
    test("Wrong suspect: 'suspect' mentioned in feedback",
         "suspect" in output.lower(),
         f"Output was:\n{output}")

    # -- Wrong weapon --
    wrong_weapon_idx = (weapon_idx % len(WEAPONS)) + 1
    g.solved = False
    g.player.move_to(target_room)
    output = run_suggestion(char_idx, wrong_weapon_idx)

    test("Wrong weapon: solved flag remains False", not g.solved)
    test("Wrong weapon: 'weapon' mentioned in feedback",
         "weapon" in output.lower(),
         f"Output was:\n{output}")

    # -- Wrong room --
    other_rooms = [r for r in ROOMS if r != sol["room"]]
    g.player.move_to(g.mansion.get_room(other_rooms[0]))
    g.solved = False
    output = run_suggestion(char_idx, weapon_idx)

    test("Wrong room: solved flag remains False", not g.solved)
    test("Wrong room: 'room' mentioned in feedback",
         "room" in output.lower(),
         f"Output was:\n{output}")

    # -- Cancel with 0 --
    def run_cancel():
        sys.stdin = io.StringIO("0\n")
        buf = io.StringIO(); sys.stdout = buf
        g._make_suggestion()
        sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__

    g.solved = False
    run_cancel()
    test("Entering 0 cancels the suggestion", not g.solved)

    # -- Notebook auto-marking --
    g.player.move_to(target_room)
    wrong_char = CHARACTERS[(char_idx % len(CHARACTERS))]
    run_suggestion(CHARACTERS.index(wrong_char) + 1, weapon_idx)
    test("Wrong suspect auto-marked X in notebook",
         g.notebook.s_status.get(wrong_char) == "X",
         f"Status was {g.notebook.s_status.get(wrong_char)}")


# ---------------------------------------------------------------------------
# 6. Accusation (win / lose path)
# ---------------------------------------------------------------------------

def test_accusation():
    section("6. Accusation (game.py)")

    random.seed(99)
    buf = io.StringIO(); sys.stdout = buf
    g = make_game()
    sys.stdout = sys.__stdout__
    sol = g.solution

    def run_accusation(char_name, weapon_name, room_name, confirm="y"):
        ci = CHARACTERS.index(char_name) + 1
        wi = WEAPONS.index(weapon_name) + 1
        ri = ROOMS.index(room_name) + 1
        sys.stdin = io.StringIO(f"{confirm}\n{ci}\n{wi}\n{ri}\n")
        buf = io.StringIO(); sys.stdout = buf
        g._make_accusation()
        sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
        return buf.getvalue()

    # -- Correct accusation --
    g.solved = False; g.won = False
    output = run_accusation(sol["character"], sol["weapon"], sol["room"])
    test("Correct accusation: solved=True",   g.solved)
    test("Correct accusation: won=True",      g.won)
    test("Correct accusation: win text shown",
         "case closed" in output.lower() or "closed" in output.lower(),
         f"Output:\n{output}")

    # -- Wrong accusation (wrong suspect) --
    wrong_char = next(c for c in CHARACTERS if c != sol["character"])
    g.solved = False; g.won = False
    output = run_accusation(wrong_char, sol["weapon"], sol["room"])
    test("Wrong accusation: solved=True",     g.solved)
    test("Wrong accusation: won=False",       not g.won)
    test("Wrong accusation: lose text shown",
         "unsolved" in output.lower() or "wrong" in output.lower(),
         f"Output:\n{output}")

    # -- Cancel accusation (answer n) --
    g.solved = False; g.won = False
    sys.stdin = io.StringIO("n\n")
    buf = io.StringIO(); sys.stdout = buf
    g._make_accusation()
    sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
    test("Cancelled accusation: solved=False", not g.solved)


# ---------------------------------------------------------------------------
# 7. Notebook
# ---------------------------------------------------------------------------

def test_notebook():
    section("7. Notebook (notebook.py)")

    nb = Notebook(CHARACTERS, WEAPONS, ROOMS)

    test("All suspects start as '?'",
         all(v == "?" for v in nb.s_status.values()))
    test("All weapons start as '?'",
         all(v == "?" for v in nb.w_status.values()))
    test("All rooms start as '?'",
         all(v == "?" for v in nb.r_status.values()))

    nb.mark_suspect("Miss Scarlett")
    test("Suspect marked X",  nb.s_status["Miss Scarlett"] == "X")

    nb.mark_weapon("Rope", "!")
    test("Weapon marked !",   nb.w_status["Rope"] == "!")

    nb.mark_room("Library", "X")
    test("Room marked X",     nb.r_status["Library"] == "X")

    nb.add_note("Test note.")
    test("Note added",        "Test note." in nb.notes)

    # display should not crash
    buf = io.StringIO(); sys.stdout = buf
    nb.display()
    sys.stdout = sys.__stdout__
    output = buf.getvalue()
    test("Notebook display contains suspects section", "SUSPECTS" in output)
    test("Notebook display contains weapons section",  "WEAPONS"  in output)
    test("Notebook display contains rooms section",    "ROOMS"    in output)


# ---------------------------------------------------------------------------
# 8. Dice
# ---------------------------------------------------------------------------

def test_dice():
    section("8. Dice (dice.py)")

    d = DiceRoll(3, 5)
    test("DiceRoll stores die1",         d.die1 == 3)
    test("DiceRoll stores die2",         d.die2 == 5)
    test("DiceRoll total is sum",        d.total == 8)
    test("steps_remaining equals total", d.steps_remaining == 8)

    d.use_step()
    test("use_step decrements by 1",     d.steps_remaining == 7)

    random_roll = DiceRoll.roll()
    test("roll() returns DiceRoll",      isinstance(random_roll, DiceRoll))
    test("roll() die1 in [1,6]",         1 <= random_roll.die1 <= 6)
    test("roll() die2 in [1,6]",         1 <= random_roll.die2 <= 6)
    test("roll() total in [2,12]",       2 <= random_roll.total <= 12)

    buf = io.StringIO(); sys.stdout = buf
    d.display()
    sys.stdout = sys.__stdout__
    test("display() produces output",    len(buf.getvalue()) > 0)


# ---------------------------------------------------------------------------
# 9. Game Initialisation
# ---------------------------------------------------------------------------

def test_game_init():
    section("9. Game Initialisation (game.py)")

    buf = io.StringIO(); sys.stdout = buf
    g = Game("Alice", "Miss Scarlett")
    sys.stdout = sys.__stdout__

    test("Player name stored",              g.player.name == "Alice")
    test("Miss Scarlett starts in Hall",    g.player.get_location() == "Hall")
    test("character_name stored",           g.character_name == "Miss Scarlett")
    test("Game has 6 character objects",    len(g.characters) == 6)
    test("Game has 6 weapon objects",       len(g.weapons) == 6)
    test("Solution has 3 keys",
         set(g.solution.keys()) == {"character", "weapon", "room"})
    test("solved starts False",             g.solved is False)
    test("won starts False",                g.won is False)
    test("turn starts at 0",               g.turn == 0)
    test("notebook initialised",            g.notebook is not None)

    test("Characters are Character instances",
         all(isinstance(c, Character) for c in g.characters))
    test("Weapons are Weapon instances",
         all(isinstance(w, Weapon) for w in g.weapons))

    char_names = [c.name for c in g.characters]
    test("All suspect names in character objects",
         sorted(char_names) == sorted(CHARACTERS))

    weapon_names = [w.name for w in g.weapons]
    test("All weapon names in weapon objects",
         sorted(weapon_names) == sorted(WEAPONS))

    # Other characters start in their canonical rooms
    buf = io.StringIO(); sys.stdout = buf
    g2 = Game("Bob", "Professor Plum")
    sys.stdout = sys.__stdout__
    test("Prof Plum starts in Study",
         g2.player.get_location() == "Study")


# ---------------------------------------------------------------------------
# 10. Input Validation
# ---------------------------------------------------------------------------

def test_input_validation():
    section("10. Input Validation (game.py)")

    buf = io.StringIO(); sys.stdout = buf
    g = make_game()
    sys.stdout = sys.__stdout__

    def run_menu(input_str):
        g.solved = False
        sys.stdin = io.StringIO(input_str + "\n9\n")   # 9 = Quit
        buf = io.StringIO(); sys.stdout = buf
        g.run()
        sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
        return buf.getvalue()

    output = run_menu("99")
    test("Invalid menu choice shows error",
         "invalid" in output.lower(),
         f"Output:\n{output}")

    output = run_menu("abc")
    test("Non-numeric menu choice shows error",
         "invalid" in output.lower(),
         f"Output:\n{output}")

    # _read_int: out-of-range suspect number
    buf2 = io.StringIO(); sys.stdout = buf2
    g2 = make_game()
    sys.stdout = sys.__stdout__

    sys.stdin = io.StringIO("99\n0\n")
    buf = io.StringIO(); sys.stdout = buf
    g2._make_suggestion()
    sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
    output = buf.getvalue()
    test("Out-of-range suspect number shows error",
         "between" in output.lower() or "invalid" in output.lower(),
         f"Output:\n{output}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 55)
    print("  CLUEDO -- Enhanced Edition  Test Suite")
    print("=" * 55)

    test_card_data()
    test_mansion()
    test_player()
    test_solution()
    test_suggestions()
    test_accusation()
    test_notebook()
    test_dice()
    test_game_init()
    test_input_validation()

    passed = sum(1 for _, ok, _ in _results if ok)
    failed = sum(1 for _, ok, _ in _results if not ok)
    total  = len(_results)

    print(f"\n{'=' * 55}")
    print(f"  RESULTS: {passed}/{total} passed", end="")
    if failed:
        print(f"  |  {failed} FAILED")
        print("\n  Failed tests:")
        for name, ok, msg in _results:
            if not ok:
                print(f"    - {name}")
                if msg:
                    print(f"      {msg}")
    else:
        print("  --  ALL TESTS PASSED")
    print("=" * 55)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
