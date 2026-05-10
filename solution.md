# Cluedo Part 1 – Solution & Test Documentation

**Student:** Wenjie Zhang  
**Project:** Project 2 – Part 1  
**Language:** Python 3 (standard library only)  
**Test file:** `test_game.py`

---

## Overview

This document records the complete test suite for the Cluedo Part 1 implementation.
Every functional requirement is covered by at least one automated test.
All 123 tests pass on a clean Python 3 installation with no external dependencies.

---

## How to Run the Tests

```
cd WenjieZhang_Project2_SourceCode
python test_game.py
```

A PASS / FAIL line prints for every test and a summary line appears at the end.

---

## Test Sections

| # | Section | Tests | What is verified |
|---|---------|-------|-----------------|
| 1 | Card Data | 14 | Lists, counts, uniqueness, Character / Weapon classes |
| 2 | Mansion Layout | 17 | Room count, adjacency, secret passages, bidirectionality |
| 3 | Player Movement | 8 | Start room, valid/invalid moves, secret-passage traversal |
| 4 | Solution Selection | 61 | Valid elements across 20 runs, randomness across 50 runs |
| 5 | Suggestion Matching | 9 | Correct guess, wrong suspect/weapon/room feedback, cancel |
| 6 | Game Initialisation | 10 | Player name, room, object types, solution structure |
| 7 | Input Validation | 3 | Invalid menu choice, non-numeric input, out-of-range number |
| **Total** | | **123** | |

---

## Section 1 – Card Data (`cards.py`)

### What is tested

- `CHARACTERS` list has exactly 6 entries with no duplicates
- `WEAPONS` list has exactly 6 entries with no duplicates
- `ROOMS` list has exactly 9 entries
- Key names are present (Miss Scarlett, Professor Plum, Rope, Wrench, Library)
- `Character` class stores `name` and `starting_room`
- `Weapon` class stores `name` and `room`

### Test script excerpt

```python
test("Six suspects defined",   len(CHARACTERS) == 6)
test("Six weapons defined",    len(WEAPONS)    == 6)
test("Nine rooms defined",     len(ROOMS)      == 9)
test("No duplicate suspects",  len(CHARACTERS) == len(set(CHARACTERS)))
test("No duplicate weapons",   len(WEAPONS)    == len(set(WEAPONS)))

char = Character("Test Char", room)
test("Character stores name",         char.name == "Test Char")
test("Character stores starting room", char.starting_room.name == "Hall")

weapon = Weapon("Test Weapon", room)
test("Weapon stores name", weapon.name == "Test Weapon")
test("Weapon stores room", weapon.room.name == "Hall")
```

### Result

```
-------------------------------------------------------
  1. Card Data (cards.py)
-------------------------------------------------------
  PASS  Six suspects defined
  PASS  Six weapons defined
  PASS  Nine rooms defined
  PASS  Miss Scarlett in suspect list
  PASS  Professor Plum in suspect list
  PASS  Rope in weapon list
  PASS  Wrench in weapon list
  PASS  Library in room list
  PASS  No duplicate suspects
  PASS  No duplicate weapons
  PASS  Character stores name
  PASS  Character stores starting room
  PASS  Weapon stores name
  PASS  Weapon stores room
```

---

## Section 2 – Mansion Layout (`mansion.py`)

### What is tested

- Mansion contains exactly 9 rooms
- All room names from `ROOMS` are present
- Every room has at least one exit
- Key adjacencies (Kitchen–Ballroom, Kitchen–Dining Room)
- Both secret passages exist and are bidirectional
- `get_room` returns `None` for an unknown room name
- `get_connections` returns a sorted list

### Test script excerpt

```python
mansion = Mansion()

test("Mansion has 9 rooms", len(mansion.rooms) == 9)
test("All named rooms exist", all(name in mansion.rooms for name in ROOMS))

for name in ROOMS:
    room = mansion.get_room(name)
    test(f"Room '{name}' has at least one exit",
         len(room.get_connections()) >= 1)

test("Kitchen connects to Ballroom",
     "Ballroom" in kitchen.get_connections())

test("Secret passage: Kitchen <-> Study",
     "Study"   in kitchen.get_connections() and
     "Kitchen" in mansion.get_room("Study").get_connections())

test("Secret passage: Lounge <-> Conservatory",
     "Conservatory" in mansion.get_room("Lounge").get_connections() and
     "Lounge"       in mansion.get_room("Conservatory").get_connections())

test("Connections are bidirectional (Hall <-> Billiard Room)",
     "Billiard Room" in hall.get_connections() and
     "Hall"          in billiard.get_connections())

test("get_room returns None for unknown name",
     mansion.get_room("Dungeon") is None)

test("get_connections returns a sorted list",
     connections == sorted(connections))
```

### Result

```
-------------------------------------------------------
  2. Mansion Layout (mansion.py)
-------------------------------------------------------
  PASS  Mansion has 9 rooms
  PASS  All named rooms exist
  PASS  Room 'Kitchen' has at least one exit
  PASS  Room 'Ballroom' has at least one exit
  PASS  Room 'Conservatory' has at least one exit
  PASS  Room 'Dining Room' has at least one exit
  PASS  Room 'Billiard Room' has at least one exit
  PASS  Room 'Library' has at least one exit
  PASS  Room 'Lounge' has at least one exit
  PASS  Room 'Hall' has at least one exit
  PASS  Room 'Study' has at least one exit
  PASS  Kitchen connects to Ballroom
  PASS  Kitchen connects to Dining Room
  PASS  Secret passage: Kitchen <-> Study
  PASS  Secret passage: Lounge <-> Conservatory
  PASS  Connections are bidirectional (Hall <-> Billiard Room)
  PASS  get_room returns None for unknown name
  PASS  get_connections returns a sorted list
```

---

## Section 3 – Player Movement (`player.py`)

### What is tested

- Player is placed in the correct starting room
- `name` attribute is stored correctly
- `can_move_to` returns `True` for an adjacent room
- `can_move_to` returns `False` for a non-adjacent room
- `move_to` updates `get_location`
- Secret passages are reachable and traversable
- A non-adjacent room (Ballroom from Hall) is correctly rejected

### Test script excerpt

```python
player = Player("Wenjie", hall)

test("Player starts in correct room",         player.get_location() == "Hall")
test("Player name stored correctly",          player.name == "Wenjie")
test("can_move_to returns True for adjacent", player.can_move_to("Study"))
test("can_move_to returns False for non-adj", not player.can_move_to("Kitchen"))

player.move_to(study)
test("Player location updates after move",    player.get_location() == "Study")
test("Secret passage accessible from Study",  player.can_move_to("Kitchen"))

player.move_to(kitchen)
test("Player can traverse secret passage",    player.get_location() == "Kitchen")

player2 = Player("Test", hall)
test("Cannot move to Ballroom from Hall",     not player2.can_move_to("Ballroom"))
```

### Result

```
-------------------------------------------------------
  3. Player Movement (player.py)
-------------------------------------------------------
  PASS  Player starts in correct room
  PASS  Player name stored correctly
  PASS  can_move_to returns True for adjacent room
  PASS  can_move_to returns False for non-adjacent room
  PASS  Player location updates after move
  PASS  Secret passage accessible from Study
  PASS  Player can traverse secret passage
  PASS  Cannot move to Ballroom from Hall (not adjacent)
```

---

## Section 4 – Solution Selection (`game.py`)

### What is tested

- Over 20 independent `Game` instances, every solution element is a valid
  member of `CHARACTERS`, `WEAPONS`, and `ROOMS`
- Over 50 independent games, solutions are not all identical (randomness check)

### Test script excerpt

```python
for i in range(20):
    g = Game("Tester")
    sol = g.solution
    test(f"Run {i+1}: solution character is valid", sol["character"] in CHARACTERS)
    test(f"Run {i+1}: solution weapon is valid",    sol["weapon"]    in WEAPONS)
    test(f"Run {i+1}: solution room is valid",      sol["room"]      in ROOMS)

solutions = [(Game("T").solution["character"],
              Game("T").solution["weapon"],
              Game("T").solution["room"]) for _ in range(50)]
test("Solutions vary across runs (randomness check)", len(set(solutions)) > 1)
```

### Result (first 9 runs shown; all 20 pass)

```
-------------------------------------------------------
  4. Solution Selection (game.py)
-------------------------------------------------------
  PASS  Run 1: solution character is valid
  PASS  Run 1: solution weapon is valid
  PASS  Run 1: solution room is valid
  PASS  Run 2: solution character is valid
  PASS  Run 2: solution weapon is valid
  PASS  Run 2: solution room is valid
  PASS  Run 3: solution character is valid
  PASS  Run 3: solution weapon is valid
  PASS  Run 3: solution room is valid
  ...  (runs 4–20 all pass)
  PASS  Solutions vary across runs (randomness check)
```

---

## Section 5 – Suggestion Matching (`game.py`)

### What is tested

| Scenario | Expected outcome |
|----------|-----------------|
| All three elements correct | `solved = True`, success message printed |
| Wrong suspect only | `solved = False`, "suspect" in output |
| Wrong weapon only | `solved = False`, "weapon" in output |
| Player not in solution room | `solved = False`, "room" in output |
| User enters `0` to cancel | `solved = False`, no crash |

### How the test works

The test finds the correct 1-based list index for the solution's character and
weapon, feeds them as simulated keyboard input via `io.StringIO`, and then
inspects both the `solved` flag and the captured standard output.

```python
random.seed(42)
g = Game("Tester")
sol = g.solution

# Move player to the solution room
g.player.move_to(g.mansion.get_room(sol["room"]))

char_idx   = CHARACTERS.index(sol["character"]) + 1
weapon_idx = WEAPONS.index(sol["weapon"]) + 1

# Correct suggestion
sys.stdin = io.StringIO(f"{char_idx}\n{weapon_idx}\n")
buf = io.StringIO(); sys.stdout = buf
g._make_suggestion()
sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
output = buf.getvalue()

test("Correct suggestion: solved flag set to True",   g.solved)
test("Correct suggestion: success message shown",
     "matches the solution" in output.lower())

# Wrong suspect
wrong_char_idx = (char_idx % len(CHARACTERS)) + 1
g.solved = False
...
test("Wrong suspect: 'suspect' mentioned in feedback", "suspect" in output.lower())
```

### Result

```
-------------------------------------------------------
  5. Suggestion Matching (game.py)
-------------------------------------------------------
  PASS  Correct suggestion: solved flag set to True
  PASS  Correct suggestion: success message shown
  PASS  Wrong suspect: solved flag remains False
  PASS  Wrong suspect: 'suspect' mentioned in feedback
  PASS  Wrong weapon: solved flag remains False
  PASS  Wrong weapon: 'weapon' mentioned in feedback
  PASS  Wrong room: solved flag remains False
  PASS  Wrong room: 'room' mentioned in feedback
  PASS  Entering 0 cancels the suggestion (solved remains False)
```

---

## Section 6 – Game Initialisation (`game.py`)

### What is tested

- `player.name` matches the name passed to `Game()`
- Player starts in the Hall
- `game.characters` has 6 `Character` instances
- `game.weapons` has 6 `Weapon` instances
- `game.solution` contains exactly the keys `character`, `weapon`, `room`
- `game.solved` starts as `False`
- Every character name matches the `CHARACTERS` list
- Every weapon name matches the `WEAPONS` list

### Test script excerpt

```python
g = Game("Alice")

test("Player initialised with correct name", g.player.name == "Alice")
test("Player starts in Hall",                g.player.get_location() == "Hall")
test("Game has 6 character objects",         len(g.characters) == 6)
test("Game has 6 weapon objects",            len(g.weapons) == 6)
test("Solution dictionary has 3 keys",       set(g.solution.keys()) == {"character", "weapon", "room"})
test("solved flag starts as False",          g.solved is False)
test("Characters are Character instances",   all(isinstance(c, Character) for c in g.characters))
test("Weapons are Weapon instances",         all(isinstance(w, Weapon)    for w in g.weapons))
test("All suspect names present",            sorted([c.name for c in g.characters]) == sorted(CHARACTERS))
test("All weapon names present",             sorted([w.name for w in g.weapons])    == sorted(WEAPONS))
```

### Result

```
-------------------------------------------------------
  6. Game Initialisation (game.py)
-------------------------------------------------------
  PASS  Player initialised with correct name
  PASS  Player starts in Hall
  PASS  Game has 6 character objects
  PASS  Game has 6 weapon objects
  PASS  Solution dictionary has 3 keys
  PASS  solved flag starts as False
  PASS  Characters are Character instances
  PASS  Weapons are Weapon instances
  PASS  All suspect names present in character objects
  PASS  All weapon names present in weapon objects
```

---

## Section 7 – Input Validation (`game.py`)

### What is tested

- A menu choice of `"99"` (out of range) produces an "invalid" message
- A menu choice of `"abc"` (non-numeric) produces an "invalid" message
- A suspect number of `"99"` in `_make_suggestion` shows a range-error message

### Test script excerpt

```python
def run_menu(input_str):
    # Append "7" so the game loop terminates after one bad choice
    sys.stdin = io.StringIO(input_str + "\n7\n")
    buf = io.StringIO(); sys.stdout = buf
    g.run()
    sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
    return buf.getvalue()

output = run_menu("99")
test("Invalid menu choice shows error message",
     "invalid" in output.lower())

output = run_menu("abc")
test("Non-numeric menu choice shows error message",
     "invalid" in output.lower())

# _read_int rejects 99 then accepts 0 (cancel)
sys.stdin = io.StringIO("99\n0\n")
...
test("Out-of-range suspect number shows error",
     "between" in output.lower() or "invalid" in output.lower())
```

### Result

```
-------------------------------------------------------
  7. Input Validation (game.py)
-------------------------------------------------------
  PASS  Invalid menu choice shows error message
  PASS  Non-numeric menu choice shows error message
  PASS  Out-of-range suspect number shows error
```

---

## Final Test Run Output

```
=======================================================
  CLUEDO PART 1 - Test Suite
=======================================================

-------------------------------------------------------
  1. Card Data (cards.py)
-------------------------------------------------------
  PASS  Six suspects defined
  PASS  Six weapons defined
  PASS  Nine rooms defined
  PASS  Miss Scarlett in suspect list
  PASS  Professor Plum in suspect list
  PASS  Rope in weapon list
  PASS  Wrench in weapon list
  PASS  Library in room list
  PASS  No duplicate suspects
  PASS  No duplicate weapons
  PASS  Character stores name
  PASS  Character stores starting room
  PASS  Weapon stores name
  PASS  Weapon stores room

-------------------------------------------------------
  2. Mansion Layout (mansion.py)
-------------------------------------------------------
  PASS  Mansion has 9 rooms
  PASS  All named rooms exist
  PASS  Room 'Kitchen' has at least one exit
  PASS  Room 'Ballroom' has at least one exit
  PASS  Room 'Conservatory' has at least one exit
  PASS  Room 'Dining Room' has at least one exit
  PASS  Room 'Billiard Room' has at least one exit
  PASS  Room 'Library' has at least one exit
  PASS  Room 'Lounge' has at least one exit
  PASS  Room 'Hall' has at least one exit
  PASS  Room 'Study' has at least one exit
  PASS  Kitchen connects to Ballroom
  PASS  Kitchen connects to Dining Room
  PASS  Secret passage: Kitchen <-> Study
  PASS  Secret passage: Lounge <-> Conservatory
  PASS  Connections are bidirectional (Hall <-> Billiard Room)
  PASS  get_room returns None for unknown name
  PASS  get_connections returns a sorted list

-------------------------------------------------------
  3. Player Movement (player.py)
-------------------------------------------------------
  PASS  Player starts in correct room
  PASS  Player name stored correctly
  PASS  can_move_to returns True for adjacent room
  PASS  can_move_to returns False for non-adjacent room
  PASS  Player location updates after move
  PASS  Secret passage accessible from Study
  PASS  Player can traverse secret passage
  PASS  Cannot move to Ballroom from Hall (not adjacent)

-------------------------------------------------------
  4. Solution Selection (game.py)
-------------------------------------------------------
  PASS  Run 1: solution character is valid
  PASS  Run 1: solution weapon is valid
  PASS  Run 1: solution room is valid
  PASS  Run 2: solution character is valid
  PASS  Run 2: solution weapon is valid
  PASS  Run 2: solution room is valid
  PASS  Run 3: solution character is valid
  PASS  Run 3: solution weapon is valid
  PASS  Run 3: solution room is valid
  PASS  Run 4: solution character is valid
  PASS  Run 4: solution weapon is valid
  PASS  Run 4: solution room is valid
  PASS  Run 5: solution character is valid
  PASS  Run 5: solution weapon is valid
  PASS  Run 5: solution room is valid
  PASS  Run 6: solution character is valid
  PASS  Run 6: solution weapon is valid
  PASS  Run 6: solution room is valid
  PASS  Run 7: solution character is valid
  PASS  Run 7: solution weapon is valid
  PASS  Run 7: solution room is valid
  PASS  Run 8: solution character is valid
  PASS  Run 8: solution weapon is valid
  PASS  Run 8: solution room is valid
  PASS  Run 9: solution character is valid
  PASS  Run 9: solution weapon is valid
  PASS  Run 9: solution room is valid
  PASS  Run 10: solution character is valid
  PASS  Run 10: solution weapon is valid
  PASS  Run 10: solution room is valid
  PASS  Run 11: solution character is valid
  PASS  Run 11: solution weapon is valid
  PASS  Run 11: solution room is valid
  PASS  Run 12: solution character is valid
  PASS  Run 12: solution weapon is valid
  PASS  Run 12: solution room is valid
  PASS  Run 13: solution character is valid
  PASS  Run 13: solution weapon is valid
  PASS  Run 13: solution room is valid
  PASS  Run 14: solution character is valid
  PASS  Run 14: solution weapon is valid
  PASS  Run 14: solution room is valid
  PASS  Run 15: solution character is valid
  PASS  Run 15: solution weapon is valid
  PASS  Run 15: solution room is valid
  PASS  Run 16: solution character is valid
  PASS  Run 16: solution weapon is valid
  PASS  Run 16: solution room is valid
  PASS  Run 17: solution character is valid
  PASS  Run 17: solution weapon is valid
  PASS  Run 17: solution room is valid
  PASS  Run 18: solution character is valid
  PASS  Run 18: solution weapon is valid
  PASS  Run 18: solution room is valid
  PASS  Run 19: solution character is valid
  PASS  Run 19: solution weapon is valid
  PASS  Run 19: solution room is valid
  PASS  Run 20: solution character is valid
  PASS  Run 20: solution weapon is valid
  PASS  Run 20: solution room is valid
  PASS  Solutions vary across runs (randomness check)

-------------------------------------------------------
  5. Suggestion Matching (game.py)
-------------------------------------------------------
  PASS  Correct suggestion: solved flag set to True
  PASS  Correct suggestion: success message shown
  PASS  Wrong suspect: solved flag remains False
  PASS  Wrong suspect: 'suspect' mentioned in feedback
  PASS  Wrong weapon: solved flag remains False
  PASS  Wrong weapon: 'weapon' mentioned in feedback
  PASS  Wrong room: solved flag remains False
  PASS  Wrong room: 'room' mentioned in feedback
  PASS  Entering 0 cancels the suggestion (solved remains False)

-------------------------------------------------------
  6. Game Initialisation (game.py)
-------------------------------------------------------
  PASS  Player initialised with correct name
  PASS  Player starts in Hall
  PASS  Game has 6 character objects
  PASS  Game has 6 weapon objects
  PASS  Solution dictionary has 3 keys
  PASS  solved flag starts as False
  PASS  Characters are Character instances
  PASS  Weapons are Weapon instances
  PASS  All suspect names present in character objects
  PASS  All weapon names present in weapon objects

-------------------------------------------------------
  7. Input Validation (game.py)
-------------------------------------------------------
  PASS  Invalid menu choice shows error message
  PASS  Non-numeric menu choice shows error message
  PASS  Out-of-range suspect number shows error

=======================================================
  RESULTS: 123/123 passed  --  ALL TESTS PASSED
=======================================================
```

---

## Requirements Coverage Matrix

| Requirement | Test(s) |
|-------------|---------|
| Nine rooms defined | Section 2 |
| Room connections accurate | Section 2 |
| Secret passages work | Section 2 |
| Six suspects defined | Section 1 |
| Six weapons defined | Section 1 |
| Random solution from valid pool | Section 4 |
| Solution varies between runs | Section 4 |
| Player starts in Hall | Section 3, 6 |
| Valid movement accepted | Section 3 |
| Invalid movement rejected | Section 3 |
| Suggestion uses current room | Section 5 |
| Correct suggestion wins the game | Section 5 |
| Wrong guess returns partial feedback | Section 5 |
| Partial feedback names wrong elements | Section 5 |
| Cancel (0) exits suggestion safely | Section 5 |
| Invalid menu input handled | Section 7 |
| Non-numeric input handled | Section 7 |
| Out-of-range number handled | Section 7 |

---

## File Structure After Testing

```
WenjieZhang_Project2_SourceCode/
|
+-- main.py          Game entry point
+-- game.py          Game class and loop
+-- mansion.py       Room and Mansion classes
+-- player.py        Player class
+-- cards.py         Card data and helper classes
+-- test_game.py     Automated test suite (123 tests)
+-- README.md        Setup and gameplay instructions
+-- walkthrough.md   Step-by-step gameplay guide
+-- solution.md      This file: test documentation
```
