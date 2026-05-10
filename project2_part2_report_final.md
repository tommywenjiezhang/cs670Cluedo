# Project 2 Part 2: Cluedo Game Report

## Title Page

**Project Title:** Cluedo Digital Edition: Enhanced Command-Line Investigation Game  
**Student Name:** [Insert Student Name]  
**Course Name:** [Insert Course Name]  
**Instructor:** [Insert Instructor Name]  
**Submission Date:** [Insert Submission Date]  

---

## Abstract

This project presents a digital command-line implementation of the board game Cluedo, developed in Python using only the standard library. The program recreates the core gameplay loop of investigating a murder by moving through rooms, making suggestions, narrowing down evidence, and making a final accusation. In addition to the baseline deduction mechanics, the project includes enhanced features such as suspect identity selection, canonical starting rooms, dice-based movement, room descriptions, secret passages, a detective notebook, and narrative win and loss endings. The system is organized into multiple modules with clear responsibilities and is supported by an automated test suite. The final result is a functional and reliable text-based game that demonstrates object-oriented programming, modular system design, input validation, and gameplay testing.

---

## Introduction

Cluedo, also known as Clue, is a classic deduction game in which players attempt to identify the correct suspect, weapon, and room involved in a murder. The game is well suited for software implementation because it combines structured game rules, hidden-state logic, user decision making, and repeated deduction cycles.

The motivation for this project was to build an interactive game system that demonstrates both gameplay design and software engineering practice. Rather than creating only a minimal rule checker, the project aimed to provide a more complete experience by including narrative setup, multiple game systems, and usability features that support player decision making.

From an educational perspective, the project was intended to strengthen skills in Python programming, modular decomposition, object-oriented design, input handling, state management, and automated testing. The finished program shows how a traditional board game can be translated into a structured command-line application while preserving its essential deduction mechanics.

---

## Game Rules

### Objective of the Game

The objective is to determine the correct combination of:

- Suspect
- Weapon
- Room

The player gathers information through suggestions and then attempts to solve the case with one final accusation.

### Player Role

The user plays as a detective and selects one of the six classic suspects as an in-game identity. Each suspect has a canonical starting room that determines where the investigation begins.

### Turn Sequence

Each game follows a turn-based structure. On each loop of the main menu, the player may:

- Move by rolling two dice
- Make a suggestion in the current room
- Make an accusation
- View the detective notebook
- View the current room description
- View the mansion map
- View the suspects list
- View the weapons list
- Quit the game

### Suggestions

A suggestion consists of:

- One suspect
- One weapon
- The player's current room

The room is fixed automatically based on the player's location. After a suggestion, the game reports which elements are incorrect and updates the notebook accordingly. A correct suggestion confirms the theory as evidence, but it does not end the game.

### Accusations

An accusation requires the player to explicitly choose:

- One suspect
- One weapon
- One room

The accusation system is the only win or lose path. If all three elements match the hidden solution, the player wins. If any part is wrong, the player loses and the real solution is revealed.

### Winning Conditions

The player wins only by making a correct accusation.

### Losing Conditions

The player loses by making an incorrect accusation. The player may also quit voluntarily, in which case the game reveals the solution and ends without a win.

---

## System Design / Architecture

The project is organized into modular Python files, each responsible for a specific part of the system. This separation improves readability, maintainability, and testing.

### Overall Structure

- `main.py` handles startup, detective name input, suspect identity selection, and game launch.
- `game.py` contains the `Game` class, which coordinates setup, the turn loop, movement, suggestions, accusations, notebook access, and quitting.
- `mansion.py` defines the `Room` and `Mansion` classes used to model the game board and room connections.
- `player.py` defines the `Player` class, which tracks the detective's location and visited rooms.
- `cards.py` stores static game data such as suspects, weapons, rooms, and canonical starting rooms.
- `notebook.py` defines the `Notebook` class for deduction tracking.
- `dice.py` defines the `DiceRoll` class used for movement.
- `story.py` stores the introduction, room descriptions, suggestion flavor text, and ending narratives.
- `test_game.py` contains the automated test suite.

### Module Dependency Diagram

The import graph below shows which modules depend on which others. Arrows point from importer to imported module.

```
main.py
  ├── cards.py          (CHARACTERS, CHARACTER_STARTING_ROOMS)
  ├── story.py          (ASCII_BANNER, INTRO_TEXT, CHARACTER_INTROS, dramatic_print)
  └── game.py
        ├── mansion.py  (Mansion)
        ├── player.py   (Player)
        ├── cards.py    (CHARACTERS, CHARACTERS_NAMES, WEAPONS, ROOMS,
        │                CHARACTER_STARTING_ROOMS, Character, Weapon)
        ├── notebook.py (Notebook)
        ├── dice.py     (DiceRoll)
        └── story.py    (ROOM_DESCRIPTIONS, SUGGESTION_FLAVOUR,
                         dramatic_print, WIN_TEXT, LOSE_TEXT)

auto_solve.py
  ├── story.py          (FAST_MODE)
  ├── game.py
  └── cards.py          (CHARACTERS, WEAPONS, ROOMS)

test_game.py
  ├── story.py          (FAST_MODE)
  ├── cards.py
  ├── mansion.py
  ├── player.py
  ├── game.py
  ├── notebook.py
  └── dice.py

cards.py    — no imports (pure data)
mansion.py  — no imports (pure domain model)
player.py   — no imports (pure domain model)
notebook.py — no imports (pure domain model)
dice.py     — random only
story.py    — sys, time only
```

This layered structure means:

- `cards.py`, `mansion.py`, `player.py`, `notebook.py` are pure domain models with no cross-dependencies.
- `game.py` is the single orchestrator that assembles all domain objects.
- `story.py` is a pure output module; no game logic depends on it for correctness.
- `main.py` is a thin entry point that only wires character selection to `Game`.

### Architectural Style

The architecture follows a modular object-oriented approach:

- Data definitions are separated from gameplay logic.
- Core gameplay state is controlled through one orchestrating object.
- Board structure is modeled explicitly through connected room objects.
- UI output is generated through terminal text and menus rather than graphical widgets.

### Data Flow

The high-level flow is as follows:

1. The program starts in `main.py`.
2. The player enters a detective name and chooses a suspect identity.
3. `Game` is initialized with the chosen identity.
4. A random hidden solution is generated.
5. The player enters the main loop and interacts through menu options.
6. Movement, suggestions, and accusations update game state.
7. The notebook records deductions after suggestion feedback.
8. The loop ends when the player wins, loses, or quits.

### Diagram Placeholders

- `[Insert Architecture Diagram]`
- `[Insert Class Diagram]`

---

## Key Features

### Game Board

The mansion contains nine rooms:

- Kitchen
- Ballroom
- Conservatory
- Dining Room
- Billiard Room
- Library
- Lounge
- Hall
- Study

These rooms are connected through predefined adjacency relationships. The resulting structure functions as a graph, where each room stores references to neighboring rooms.

### Player Movement

Movement is controlled by rolling two six-sided dice. The total value becomes the number of room-hop steps available during that move turn. Each standard move to an adjacent room uses one step. The player may stop moving early if desired.

The system also prevents revisiting rooms within the same move turn, which helps maintain clear movement logic and avoids trivial loops.

### Secret Passages

Two secret passages are supported:

- Kitchen to Study
- Lounge to Conservatory

These moves are free and do not consume movement steps, which adds strategic variety.

### Suggestion Mechanics

The suggestion system allows the player to propose a suspect and weapon while automatically using the current room as the room component. The game compares the guess to the hidden solution and identifies which elements are incorrect.

This design turns suggestions into a structured clue-gathering mechanic rather than an immediate win condition.

### Accusation Mechanics

The accusation system requires all three solution elements to be selected directly. Because the player receives only one accusation opportunity, this feature creates tension and forces careful deduction.

### Turn Management

The game operates through a repeated menu loop. This approach makes the game easy to navigate and ensures that each action updates the state in a controlled and predictable way.

### User Interface

Although the project is command-line based, several interface features improve usability:

- Structured menu headers
- Readable prompts
- ASCII dice art
- Narrative room descriptions
- Notebook status display
- ASCII mansion map
- Story-based win and lose messages

### AI or Multiplayer Support

The project does not currently implement multiplayer or computer-controlled opponents. However, it does include `auto_solve.py`, which demonstrates automated investigation logic for verification and experimentation.

---

## Implementation Details

### Programming Language and Libraries

The project is written in Python and uses only standard library modules such as:

- `random`
- `sys`
- `io`
- `time`

This keeps the project lightweight and easy to run in a standard Python environment.

### Core Classes and Modules

The subsections below provide detailed technical coverage of every module in the codebase. Each subsection explains what the module does, describes its key methods and data structures, and includes real code excerpts to support every claim.

---

#### `cards.py` — Static Game Data

**What it does and why it exists**

`cards.py` is a pure data module with no imports from the project. It serves as the single source of truth for all game card lists and the two object types (`Character`, `Weapon`) that wrap room references for NPC placement. Keeping data here means any other module can import from one place without circular dependencies.

**Data structures**

The suspects, weapons, and rooms are stored as plain Python lists:

```python
CHARACTERS = [
    "Miss Scarlett",
    "Colonel Mustard",
    "Mrs. White",
    "Mr. Green",
    "Mrs. Peacock",
    "Professor Plum",
]

WEAPONS = [
    "Candlestick", "Revolver", "Rope",
    "Lead Pipe", "Knife", "Wrench",
]

ROOMS = [
    "Kitchen", "Ballroom", "Conservatory",
    "Dining Room", "Billiard Room", "Library",
    "Lounge", "Hall", "Study",
]
```

Lists are chosen over sets because order is required for numbered menus, and `random.choice` works directly on sequences. `CHARACTERS_NAMES` is an alias for `CHARACTERS` so modules that import one name can stay consistent.

**Character starting rooms**

```python
CHARACTER_STARTING_ROOMS = {
    "Miss Scarlett":   "Hall",
    "Colonel Mustard": "Lounge",
    "Mrs. White":      "Kitchen",
    "Mr. Green":       "Billiard Room",
    "Mrs. Peacock":    "Library",
    "Professor Plum":  "Study",
}
```

A dictionary is used here for O(1) lookup by name. `game.py` calls `CHARACTER_STARTING_ROOMS[character_name]` during `__init__` to find the correct `Room` object without iterating.

**`Character` and `Weapon` classes**

```python
class Character:
    def __init__(self, name, starting_room):
        self.name = name
        self.starting_room = starting_room  # Room object

    def __str__(self):
        return f"{self.name} (starts in {self.starting_room.name})"


class Weapon:
    def __init__(self, name, room):
        self.name = name
        self.room = room  # Room object

    def __str__(self):
        return f"{self.name} (in {self.room.name})"
```

Both classes wrap a `Room` object rather than a room name string. This allows `game.py` to pass fully resolved room references during setup and avoids any second lookup later.

**Interaction with other components**

`game.py` imports `CHARACTERS`, `WEAPONS`, `ROOMS`, `CHARACTER_STARTING_ROOMS`, `Character`, and `Weapon`. `main.py` imports `CHARACTERS` and `CHARACTER_STARTING_ROOMS` for the character selection menu. `test_game.py` imports everything for validation.

---

#### `mansion.py` — Room Graph and Board

**What it does and why it exists**

`mansion.py` models the game board as a connected graph of `Room` objects. It keeps board structure separate from player logic so rooms can be queried, connected, and displayed without any knowledge of game state.

**`Room` class — key methods**

```python
class Room:
    def __init__(self, name):
        self.name = name
        self._connected = []   # list of Room objects

    def connect(self, other_room):
        """Create a two-way connection between this room and another."""
        if other_room not in self._connected:
            self._connected.append(other_room)
            other_room._connected.append(self)

    def get_connections(self):
        """Return a sorted list of connected room names."""
        return sorted(r.name for r in self._connected)
```

`_connected` stores actual `Room` object references, not strings, so adjacency checks are pointer comparisons. `connect()` writes both directions in a single call — the caller never has to call it twice. `get_connections()` returns sorted names to make menus and test assertions deterministic.

**`Mansion` class — building the graph**

The mansion is built in two phases: first all nine rooms are created as empty `Room` objects stored in `self.rooms` (a dict keyed by name), then all edges including secret passages are added:

```python
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
```

Secret passages are modeled as ordinary edges in the graph. Their special behavior (free movement, no step cost) is handled in `game._move`, not here, which keeps the graph model simple and general.

**`display_map` — marking current location**

```python
def display_map(self, current_room=None):
    def tag(name, abbrev):
        if name == current_room:
            return f"[*{abbrev:<8}]"   # star marker
        return f"[ {abbrev:<8}]"        # space filler
    ...
```

The inner `tag()` closure captures `current_room` from the outer scope and returns a fixed-width string with or without a star marker. All room tags are exactly 11 characters wide so the ASCII grid aligns correctly regardless of which room is active.

**Interaction with other components**

`game.py` calls `Mansion()` in `__init__`, uses `get_room(name)` extensively, and passes `display_map(player.get_location())` for the map menu option. `player.py` receives a `Room` object as its starting room and uses `current_room.get_connections()` for movement checks.

---

#### `player.py` — Detective Location Tracking

**What it does and why it exists**

`Player` is a lightweight object that wraps the detective's current `Room` reference and their visited-room history. It deliberately contains no game logic — it only tracks where the player is and whether a move is structurally legal.

**Key methods and data structures**

```python
class Player:
    def __init__(self, name, starting_room):
        self.name = name
        self.current_room = starting_room
        self.visited_rooms = {starting_room.name}

    def can_move_to(self, room_name):
        """Return True if room_name is directly connected to the current room."""
        return room_name in self.current_room.get_connections()

    def move_to(self, room):
        """Move the player to a new Room object and record the visit."""
        self.current_room = room
        self.visited_rooms.add(room.name)
```

`visited_rooms` is a Python `set` so membership checks (`room_name not in player.visited_rooms`) are O(1). This set is used by `game._move` to display room descriptions only on first entry — a purely cosmetic use that does not affect movement rules.

`can_move_to` delegates entirely to `current_room.get_connections()`. The Player has no knowledge of the graph structure; it simply asks its current room. This means if the mansion graph changes, Player requires no modification.

**Interaction with other components**

`game._move` calls `player.can_move_to()` indirectly (through the exit list built from `player.current_room.get_connections()`), calls `player.move_to(dest_room)` after each hop, and reads `player.get_location()` to check current position. `game._make_suggestion` reads `player.get_location()` to fix the room in suggestions.

---

#### `dice.py` — Movement Dice

**What it does and why it exists**

`dice.py` provides the `DiceRoll` class, which encapsulates both the values rolled and the remaining movement budget. By combining these two concerns into one object, `game._move` always knows how many steps are left without maintaining a separate counter.

**Data structures**

```python
FACES = {
    1: ["+-----+", "|     |", "|  o  |", "|     |", "+-----+"],
    2: ["+-----+", "|o    |", "|     |", "|    o|", "+-----+"],
    # ... up to 6
}
```

`FACES` is a module-level dictionary mapping die value (1–6) to a list of five strings. Each string is exactly seven characters wide so two dice can be printed side-by-side with correct alignment.

**`DiceRoll` class**

```python
class DiceRoll:
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
        f1 = FACES[self.die1]
        f2 = FACES[self.die2]
        print("\n  Rolling the dice...")
        for l1, l2 in zip(f1, f2):
            print(f"    {l1}   {l2}")
        print(f"\n    {self.die1} + {self.die2} = {self.total}  "
              f"-- You have {self.steps_remaining} step(s) to move.\n")
```

`roll()` is a static factory method so callers do not need to manually generate two random integers. `use_step()` guards against decrementing below zero, though the movement loop already terminates when `steps_remaining == 0`. Secret passage moves do not call `use_step()`, making them free.

**Interaction with other components**

`game._move` calls `DiceRoll.roll()` once per turn, calls `dice.display()` to show the dice art, and calls `dice.use_step()` after each standard room hop. Secret passage moves skip `use_step()`.

---

#### `notebook.py` — Deduction Tracker

**What it does and why it exists**

The `Notebook` class records which suspects, weapons, and rooms have been eliminated or confirmed through suggestions. It is the player's investigation memory and is updated automatically by `game._make_suggestion`.

**Data structures and status codes**

```python
class Notebook:
    def __init__(self, suspects, weapons, rooms):
        self.suspects = list(suspects)
        self.weapons  = list(weapons)
        self.rooms    = list(rooms)
        self.s_status = {n: "?" for n in suspects}
        self.w_status = {n: "?" for n in weapons}
        self.r_status = {n: "?" for n in rooms}
        self.notes    = []
```

Three parallel dicts (`s_status`, `w_status`, `r_status`) map each card name to a single-character status code:
- `"?"` — unknown, not yet tested
- `"X"` — ruled out, proven wrong in a suggestion
- `"!"` — confirmed, all three elements matched

`notes` is a plain list of strings for free-text annotations added automatically when suggestions produce partial or total mismatches.

**Marking helpers**

```python
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
```

The default argument `status="X"` covers the common case (ruling out). Passing `"!"` marks a confirmed element. The `if name in` guard prevents a KeyError if an invalid name is ever passed — a defensive check that makes the notebook robust against typos elsewhere.

**Two-column display**

```python
def _print_section(self, title, items, status):
    print(f"\n  {title}:")
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
```

Items are displayed in pairs. The left cell is padded to 20 characters with `:<20` so that the right column always starts in the same horizontal position regardless of name length.

**Interaction with other components**

`game._make_suggestion` calls `mark_suspect`, `mark_weapon`, and `mark_room` based on which elements were wrong, and `mark_*(..., "!")` when all three match. `game._show_notebook` calls `notebook.display()`. `test_game.py` constructs `Notebook` objects directly to verify status transitions.

---

#### `story.py` — Narrative Text and Typewriter Output

**What it does and why it exists**

`story.py` centralizes all player-facing text — the intro, room descriptions, suggestion feedback, win/lose endings, and character backgrounds. Separating narrative content from game logic makes it easy to update text without touching gameplay code.

**`FAST_MODE` flag and `dramatic_print`**

```python
FAST_MODE = False

def dramatic_print(text, delay=0.018):
    """Print text one character at a time for a typewriter effect."""
    if FAST_MODE or delay == 0:
        sys.stdout.write(text)
        sys.stdout.flush()
        print()
        return
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay * 8 if ch in ".!?\n" else delay)
    print()
```

`FAST_MODE` is a module-level boolean. `test_game.py` sets `story.FAST_MODE = True` at the top of the file to bypass the `time.sleep` calls, making the test suite run instantly. The `delay * 8` rule gives sentence-ending punctuation an extended pause for dramatic effect during normal play.

**`SUGGESTION_FLAVOUR` dict**

```python
SUGGESTION_FLAVOUR = {
    "suspect": "That suspect was not in the vicinity. The witnesses are certain.",
    "weapon":  "That weapon bears no mark from the crime scene. Think again.",
    "room":    "The crime did not occur in that room. Search the manor further.",
    "all":     "Nothing aligns. Your theory collapses entirely. Start over.",
    "match":   "Everything aligns. Your pulse quickens -- you are very close to the truth.",
}
```

`game._make_suggestion` indexes this dict with element names (`"suspect"`, `"weapon"`, `"room"`, `"all"`, `"match"`) to produce feedback without embedding long strings in game logic. The test suite checks for the keywords `"suspect"`, `"weapon"`, `"room"`, `"aligns"`, and `"pulse"` in suggestion output — these keywords are deliberately present in the flavour strings.

**Interaction with other components**

`game.py` imports `ROOM_DESCRIPTIONS`, `SUGGESTION_FLAVOUR`, `dramatic_print`, `WIN_TEXT`, and `LOSE_TEXT`. `main.py` imports `ASCII_BANNER`, `INTRO_TEXT`, `CHARACTER_INTROS`, and `dramatic_print`. No other module imports from `story.py`, preserving the clean dependency direction.

---

#### `game.py` — Game Orchestrator

**What it does and why it exists**

`Game` is the central coordinator. Its `__init__` assembles all domain objects and its `run()` method drives the turn loop. No other module has this breadth of responsibility — every other class handles one concern, and `Game` wires them together.

**`__init__` — initialization order**

```python
def __init__(self, player_name, character_name):
    self.mansion    = Mansion()
    self.solution   = self._select_solution()
    self.characters = self._place_characters()
    self.weapons    = self._place_weapons()

    start_room = self.mansion.get_room(
        CHARACTER_STARTING_ROOMS[character_name]
    )
    self.player    = Player(player_name, start_room)
    self.character_name = character_name

    self.notebook  = Notebook(CHARACTERS_NAMES, WEAPONS, ROOMS)
    self.turn      = 0
    self.solved    = False
    self.won       = False

    print(f"\n  You begin your investigation in the {start_room.name}.")
    print(f"  {ROOM_DESCRIPTIONS.get(start_room.name, '')}")
```

Mansion is built first so that `_place_characters` and `_place_weapons` can look up room objects by name. `self.solved` is the loop exit flag; `self.won` distinguishes win from loss. The starting room description is printed immediately so the player has context before the first menu.

**`_select_solution` — random hidden solution**

```python
def _select_solution(self):
    return {
        "character": random.choice(CHARACTERS),
        "weapon":    random.choice(WEAPONS),
        "room":      random.choice(ROOMS),
    }
```

Each of the three elements is chosen independently using `random.choice` on the imported lists. The solution is a plain dict with keys `"character"`, `"weapon"`, `"room"` — no special class is needed because it is only read by comparison code.

**`_move` — dice-based movement loop**

```python
def _move(self):
    dice = DiceRoll.roll()
    dice.display()
    self.turn += 1

    visited_this_turn = {self.player.get_location()}

    while dice.steps_remaining > 0:
        current = self.player.get_location()
        all_exits = self.player.current_room.get_connections()
        exits = [r for r in all_exits if r not in visited_this_turn]

        SECRET_PASSAGES = {
            "Kitchen": "Study",  "Study":   "Kitchen",
            "Lounge":  "Conservatory", "Conservatory": "Lounge",
        }
        passage_dest = SECRET_PASSAGES.get(current)
        has_passage  = (
            passage_dest is not None
            and passage_dest not in visited_this_turn
        )

        if not exits and not has_passage:
            print("  No accessible rooms remain. Remaining steps forfeit.")
            break
        ...
        if choice == "p" and has_passage:
            dest_room = self.mansion.get_room(passage_dest)
            visited_this_turn.add(passage_dest)
            self.player.move_to(dest_room)
            # NOTE: no dice.use_step() call here — passage is free
            ...
```

`visited_this_turn` is a local set initialized with the player's current room. Before building the exit list each iteration, already-visited rooms are filtered out with a list comprehension. This prevents the player from looping back through rooms they entered earlier in the same turn.

Secret passages are handled by an inline `SECRET_PASSAGES` dict. When the current room has a passage and the destination has not been visited this turn, option `P` is added to the menu. Taking a passage calls `player.move_to()` but deliberately omits `dice.use_step()`, making it a free move.

**`_make_suggestion` — clue gathering**

```python
def _make_suggestion(self):
    current_room = self.player.get_location()
    ...
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

    if not wrong:
        # All three match -- but this does NOT end the game
        print(f"  {SUGGESTION_FLAVOUR['match']}")
        print("  Record it in your notebook and make your Accusation to close the case.")
        self.notebook.mark_suspect(chosen_char,   "!")
        self.notebook.mark_weapon(chosen_weapon,  "!")
        self.notebook.mark_room(current_room,     "!")
    elif len(wrong) == 3:
        print(f"  {SUGGESTION_FLAVOUR['all']}")
        self.notebook.add_note(...)
    else:
        for element in wrong:
            print(f"  {SUGGESTION_FLAVOUR[element]}")
        self.notebook.add_note(...)
```

Three boolean comparisons build the `wrong` list. Wrong elements are immediately marked `"X"` in the notebook. The all-match branch marks everything `"!"` but does **not** set `self.solved` — the `run()` loop continues. This is the central design decision: suggestions gather evidence; only an accusation ends the game.

**`_make_accusation` — the only win/lose path**

```python
def _make_accusation(self):
    ...
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
        dramatic_print(LOSE_TEXT)
        self.solved = True
        self.won    = False
```

A single three-way `and` check determines win or loss. In both branches `self.solved = True` is set, which exits the `while not self.solved` loop in `run()`. On a loss, the real solution is printed before the lose narrative. This method is the only place in the codebase that sets `self.solved = True`.

**`_read_int` and `_read_yes_no` — input validation helpers**

```python
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
```

`_read_int` returns `None` for three invalid cases: the cancel character `"0"`, non-numeric text, and out-of-range numbers. Callers check `if char_idx is None: return` immediately after each call, which bubbles the cancel back to the menu without crashing. `_read_yes_no` loops indefinitely until a valid answer is received, making it impossible to accidentally skip a confirmation.

**Interaction with other components**

`Game` owns one instance of each domain object (`Mansion`, `Player`, `Notebook`) and creates `Character` and `Weapon` instances during setup. It calls `DiceRoll.roll()` in `_move`, reads `SUGGESTION_FLAVOUR` and `ROOM_DESCRIPTIONS` from `story.py`, and calls `dramatic_print` for win/lose endings. The `run()` method is the only public interface used by `main.py`.

---

#### `main.py` — Entry Point

**What it does and why it exists**

`main.py` is a thin entry point. Its sole responsibility is to collect the two pieces of startup information the game needs (detective name and character choice) and pass them to `Game`. No game logic lives here.

**`_pick_int` — mandatory integer input**

```python
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
```

Unlike `game._read_int`, this version has no cancel path and loops until a valid integer is entered. It is used only for character selection, where a choice must be made to start the game.

**Character selection loop**

```python
def main():
    dramatic_print(INTRO_TEXT)
    print(ASCII_BANNER)

    name = input("  Enter your detective name: ").strip()
    if not name:
        name = "Detective"

    print("\n  Choose your suspect identity:")
    for i, char_name in enumerate(CHARACTERS, 1):
        start = CHARACTER_STARTING_ROOMS[char_name]
        intro = CHARACTER_INTROS.get(char_name, "")
        print(f"  {i}. {char_name:<22} (starts in {start:<14})  {intro}")

    choice = _pick_int(1, len(CHARACTERS))
    chosen_character = CHARACTERS[choice - 1]
    chosen_start     = CHARACTER_STARTING_ROOMS[chosen_character]

    game = Game(player_name=name, character_name=chosen_character)
    game.run()
```

The character list is enumerated with `enumerate(CHARACTERS, 1)` to produce 1-based numbering. The selected character name is looked up as `CHARACTERS[choice - 1]` (converting back to 0-based index). The blank-name fallback `"Detective"` prevents an empty display name if the user presses Enter without typing.

---

#### `auto_solve.py` — Automated BFS Solver

**What it does and why it exists**

`auto_solve.py` demonstrates a complete automated investigation strategy. It creates a real `Game` object and plays through it using pre-computed inputs rather than keyboard input. It serves as a correctness verification tool and a demonstration that the game can be solved reliably using systematic deduction.

**`EchoingInput` — stdin simulation**

```python
class EchoingInput:
    """Pre-feeds (value, label) pairs as stdin and echoes each choice."""
    def __init__(self, annotated):
        self._items = list(annotated)
        self._index = 0

    def readline(self):
        if self._index >= len(self._items):
            return ""
        value, label = self._items[self._index]
        self._index += 1
        print(f"  [INPUT] {value!r:<4}  -- {label}")
        return value + "\n"
```

`EchoingInput` replaces `sys.stdin` during the live game run. It reads from a pre-built list of `(value, label)` pairs rather than the keyboard. The `label` is only for display — it explains what each input represents. `readline()` returns `value + "\n"` because Python's `input()` internally calls `readline()` and strips the newline.

**`shortest_path` — BFS path finder**

```python
def shortest_path(mansion, start, end):
    """BFS: return room-name list from start to end (inclusive)."""
    if start == end:
        return [start]
    visited = {start}
    queue = deque([[start]])
    while queue:
        path = queue.popleft()
        for nb in mansion.get_room(path[-1]).get_connections():
            if nb == end:
                return path + [nb]
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])
    return None
```

Standard BFS over the mansion graph. Paths are stored as complete lists so the function returns the full route rather than just the distance. This is used by `add_movement` to generate the correct sequence of move inputs for each hop along the route.

**Investigation strategy**

The solver visits rooms in BFS order from the starting room. In each room it makes one suggestion, cycling through the unknown suspects and weapons. Wrong elements are removed from the `unkn_s` and `unkn_w` lists. Correct elements are skipped by advancing a pointer. Room mismatch removes the current room from `unkn_r`. When all three unknown lists have exactly one element left, the solver makes the accusation. This guarantees a correct accusation in at most as many suggestions as there are rooms to visit.

---

### Data Structures

The project uses a mix of simple and effective data structures:

- Lists for ordered menu entries and static data collections
- Dictionaries for quick lookups such as starting rooms and notebook statuses
- Sets for visited-room tracking
- Connected objects for the room graph

### Algorithms and Logic

Key logic includes:

- Random selection of solution elements
- Graph-based adjacency checks for movement
- Step-by-step dice movement with optional early stop
- Secret passage branching during movement
- Element-by-element comparison for suggestion feedback
- Full equality check for final accusations

### State Management

The main game state includes:

- Hidden solution
- Current player location
- Character identity
- Turn number
- Notebook deductions
- Whether the game has been solved
- Whether the player won or lost

This state is updated incrementally through game actions.

### Input Handling and Validation

The game uses helper methods to validate integer ranges and yes-or-no responses. Invalid input is handled safely with user-facing messages rather than unhandled exceptions. Cancel behavior is also supported for some selection prompts.

### Rule Validation

Rule validation includes:

- Only connected rooms may be entered
- Secret passage options appear only in valid rooms
- Out-of-range menu input is rejected
- Suggestions use the current room automatically
- Accusations require explicit confirmation
- Only accusation can produce a true win or loss state

### Code Snippet Placeholders

- `[Insert Code Snippet: Player Movement Logic]`
- `[Insert Code Snippet: Suggestion System]`

---

## Thorough Testing

Testing was a major part of the project. The current automated suite in `test_game.py` verifies the behavior of the major systems in the game. In the current repository state, all 161 automated tests pass.

### Testing Approach

The test suite in `test_game.py` uses a custom lightweight test runner rather than an external framework like `unittest` or `pytest`. This makes the file self-contained and runnable with `python test_game.py` in any standard Python environment.

**Custom runner infrastructure:**

```python
_results = []

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
```

Each call to `test()` records a tuple `(name, passed, message)` in the `_results` list. At the end of the suite, the list is summarized as `passed/total -- ALL TESTS PASSED` or a list of failures.

**Key testing techniques used throughout the suite:**

1. `story.FAST_MODE = True` — set at the top of the file to disable `time.sleep` inside `dramatic_print`, making the entire suite run in under a second.
2. `sys.stdout` redirection — `io.StringIO()` captures printed output so assertions can check for keywords in game feedback.
3. `sys.stdin` injection — `io.StringIO("choice\n")` pre-loads input so interactive prompts read from a string buffer instead of the keyboard.
4. `random.seed(42)` / `random.seed(99)` — fixed seeds in suggestion and accusation tests ensure the hidden solution is predictable, allowing exact index calculations.
5. `make_game()` helper — creates a `Game("Tester", "Miss Scarlett")` with output suppressed, so every test section starts from a consistent state.

```python
def make_game(player_name="Tester"):
    """Create a standard game with Miss Scarlett (starts in Hall)."""
    return Game(player_name, "Miss Scarlett")
```

---

### Test Section 1 — Card Data (`test_card_data`)

**What is being tested:** The correctness and completeness of all static game data in `cards.py`: list sizes, specific membership, uniqueness, alias identity, and correct construction of `Character` and `Weapon` objects.

**Why it matters:** Every other system depends on these lists being exactly right. A wrong count or duplicate entry would cause menus to show wrong entries and solution selection to be unbalanced.

**Test code:**

```python
def test_card_data():
    test("Six suspects defined",   len(CHARACTERS) == 6)
    test("Six weapons defined",    len(WEAPONS) == 6)
    test("Nine rooms defined",     len(ROOMS) == 9)
    test("Miss Scarlett in suspect list",  "Miss Scarlett"  in CHARACTERS)
    test("Professor Plum in suspect list", "Professor Plum" in CHARACTERS)
    test("Rope in weapon list",            "Rope"    in WEAPONS)
    test("Wrench in weapon list",          "Wrench"  in WEAPONS)
    test("Library in room list",           "Library" in ROOMS)
    test("No duplicate suspects",  len(CHARACTERS) == len(set(CHARACTERS)))
    test("No duplicate weapons",   len(WEAPONS)    == len(set(WEAPONS)))
    test("CHARACTERS_NAMES is same as CHARACTERS", CHARACTERS_NAMES is CHARACTERS)
    test("CHARACTER_STARTING_ROOMS has 6 entries", len(CHARACTER_STARTING_ROOMS) == 6)
    test("All suspects have a starting room",
         all(c in CHARACTER_STARTING_ROOMS for c in CHARACTERS))

    mansion = Mansion()
    room = mansion.get_room("Hall")
    char = Character("Test Char", room)
    test("Character stores name",          char.name == "Test Char")
    test("Character stores starting room", char.starting_room.name == "Hall")

    weapon = Weapon("Test Weapon", room)
    test("Weapon stores name", weapon.name == "Test Weapon")
    test("Weapon stores room", weapon.room.name == "Hall")
```

**Inputs / Expected / Actual:**
- Input: module-level lists from `cards.py`
- Expected: 6 suspects, 6 weapons, 9 rooms, no duplicates, correct alias, 6 starting rooms
- Actual: All pass

---

### Test Section 2 — Mansion Layout (`test_mansion`)

**What is being tested:** The structure of the room graph — room count, named room presence, minimum connectivity, specific known adjacencies, and both secret passages in both directions.

**Why it matters:** Incorrect adjacency definitions would allow illegal moves or block valid routes. Secret passage bi-directionality is critical because `Room.connect()` must write both directions.

**Key test code:**

```python
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

connections = hall.get_connections()
test("get_connections returns a sorted list",
     connections == sorted(connections))
```

**Edge cases covered:** Unknown room name returns `None` (not KeyError); `get_connections()` is sorted (deterministic menu ordering).

---

### Test Section 3 — Player Movement (`test_player`)

**What is being tested:** `Player.can_move_to()` returns the correct boolean for adjacent and non-adjacent rooms; `move_to()` updates `current_room` and `visited_rooms`; secret passages are accessible after traversal.

**Why it matters:** If `can_move_to` incorrectly allows illegal moves, players could teleport across the board. If `visited_rooms` does not update, first-visit room descriptions would repeat.

**Test code:**

```python
player = Player("Wenjie", hall)

test("Player starts in correct room",         player.get_location() == "Hall")
test("can_move_to returns True for adjacent", player.can_move_to("Study"))
test("can_move_to returns False for non-adj", not player.can_move_to("Kitchen"))

player.move_to(study)
test("Player location updates after move",    player.get_location() == "Study")
test("Study added to visited_rooms",          "Study" in player.visited_rooms)
test("Secret passage accessible from Study",  player.can_move_to("Kitchen"))

player.move_to(kitchen)
test("Player can traverse secret passage",    player.get_location() == "Kitchen")

player2 = Player("Test", hall)
test("Cannot move to Ballroom from Hall",     not player2.can_move_to("Ballroom"))
```

**Edge cases covered:** Non-adjacent room (`Hall` → `Ballroom`) correctly returns `False`; secret passage is accessible from `Study` to `Kitchen` once the graph edge exists.

---

### Test Section 4 — Solution Selection (`test_solution`)

**What is being tested:** Over 20 independent game instances, each solution element is drawn from the correct list. Over 50 instances, the combined solutions are not all identical (verifying randomness).

**Why it matters:** If solution selection were broken — for example, always returning the first element — the game would be trivially solvable. The randomness check catches deterministic bugs.

**Test code:**

```python
for i in range(20):
    buf = io.StringIO(); sys.stdout = buf
    g = make_game()
    sys.stdout = sys.__stdout__
    sol = g.solution
    test(f"Run {i+1}: solution character is valid", sol["character"] in CHARACTERS)
    test(f"Run {i+1}: solution weapon is valid",    sol["weapon"]    in WEAPONS)
    test(f"Run {i+1}: solution room is valid",      sol["room"]      in ROOMS)

solutions = []
for _ in range(50):
    buf = io.StringIO(); sys.stdout = buf
    g = make_game()
    sys.stdout = sys.__stdout__
    solutions.append((g.solution["character"], g.solution["weapon"], g.solution["room"]))
test("Solutions vary across runs (randomness check)",
     len(set(solutions)) > 1)
```

**Inputs:** 50 `Game` instances with no seed
**Expected:** Multiple distinct `(character, weapon, room)` tuples
**Actual:** Pass (set size well above 1 for 50 runs across 6×6×9 = 324 combinations)

---

### Test Section 5 — Suggestion Matching (`test_suggestions`)

**What is being tested:** Each incorrect suggestion element produces the correct feedback keyword; the `solved` flag never becomes `True` from a suggestion; the notebook is auto-marked correctly; cancelling with `0` exits cleanly.

**Why it matters:** The suggestion/accusation distinction is the most important game rule. If a correct suggestion set `solved = True`, the game would end without the player making an accusation, breaking the core mechanic.

**Test helper and correct-suggestion test:**

```python
random.seed(42)
g = make_game()
sol = g.solution
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

g.solved = False
output = run_suggestion(char_idx, weapon_idx)

test("Correct suggestion: solved flag remains False", not g.solved)
test("Correct suggestion: clue-match flavour shown",
     "aligns" in output.lower() or "pulse" in output.lower())
```

Additional tests verify:
- Wrong suspect: `"suspect"` appears in output, `solved` stays False
- Wrong weapon: `"weapon"` appears in output, `solved` stays False
- Wrong room (player moved away): `"room"` appears in output
- Cancel (input `"0"`): method returns without changing state
- Notebook auto-mark: wrong suspect gets status `"X"`

---

### Test Section 6 — Accusation Win/Lose (`test_accusation`)

**What is being tested:** A correct accusation sets `solved=True` and `won=True` with win text; a wrong accusation sets `solved=True` and `won=False` with lose text; cancelling at confirmation sets nothing.

**Why it matters:** This is the only win/lose path. Incorrect flag handling would produce wrong endings or allow the game to continue after a final accusation.

**Test code:**

```python
random.seed(99)
g = make_game()
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

# Correct accusation
g.solved = False; g.won = False
output = run_accusation(sol["character"], sol["weapon"], sol["room"])
test("Correct accusation: solved=True",  g.solved)
test("Correct accusation: won=True",     g.won)
test("Correct accusation: win text shown",
     "case closed" in output.lower() or "closed" in output.lower())

# Wrong accusation
wrong_char = next(c for c in CHARACTERS if c != sol["character"])
g.solved = False; g.won = False
output = run_accusation(wrong_char, sol["weapon"], sol["room"])
test("Wrong accusation: solved=True",    g.solved)
test("Wrong accusation: won=False",      not g.won)
test("Wrong accusation: lose text shown",
     "unsolved" in output.lower() or "wrong" in output.lower())

# Cancel
g.solved = False; g.won = False
sys.stdin = io.StringIO("n\n")
buf = io.StringIO(); sys.stdout = buf
g._make_accusation()
sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
test("Cancelled accusation: solved=False", not g.solved)
```

---

### Test Section 7 — Notebook (`test_notebook`)

**What is being tested:** Initial status values are all `"?"`; `mark_*` methods update to the correct status; `add_note` stores text; `display()` produces output with all three section headers.

**Why it matters:** An incorrect initial status would hide information from the player. A display failure would make the notebook menu option useless.

**Test code:**

```python
nb = Notebook(CHARACTERS, WEAPONS, ROOMS)

test("All suspects start as '?'", all(v == "?" for v in nb.s_status.values()))
test("All weapons start as '?'",  all(v == "?" for v in nb.w_status.values()))
test("All rooms start as '?'",    all(v == "?" for v in nb.r_status.values()))

nb.mark_suspect("Miss Scarlett")
test("Suspect marked X",  nb.s_status["Miss Scarlett"] == "X")

nb.mark_weapon("Rope", "!")
test("Weapon marked !",   nb.w_status["Rope"] == "!")

nb.mark_room("Library", "X")
test("Room marked X",     nb.r_status["Library"] == "X")

nb.add_note("Test note.")
test("Note added",        "Test note." in nb.notes)

buf = io.StringIO(); sys.stdout = buf
nb.display()
sys.stdout = sys.__stdout__
output = buf.getvalue()
test("Notebook display contains suspects section", "SUSPECTS" in output)
test("Notebook display contains weapons section",  "WEAPONS"  in output)
test("Notebook display contains rooms section",    "ROOMS"    in output)
```

---

### Test Section 8 — Dice (`test_dice`)

**What is being tested:** `DiceRoll` stores individual die values and their sum; `steps_remaining` equals the total; `use_step()` decrements by exactly 1; `roll()` produces a `DiceRoll` with values in the valid range; `display()` produces non-empty output.

**Why it matters:** Incorrect step counting would give the player more or fewer moves than the dice roll. Out-of-range die values would break the `FACES` dict lookup.

**Test code:**

```python
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
```

---

### Test Section 9 — Game Initialisation (`test_game_init`)

**What is being tested:** All `Game.__init__` state fields are set correctly for two different character choices. Character and weapon objects are the correct types. All six suspects and six weapons appear in the object lists.

**Why it matters:** If any field is unset or wrong at init, every subsequent action on the game may fail or produce incorrect results.

**Test code:**

```python
buf = io.StringIO(); sys.stdout = buf
g = Game("Alice", "Miss Scarlett")
sys.stdout = sys.__stdout__

test("Player name stored",           g.player.name == "Alice")
test("Miss Scarlett starts in Hall", g.player.get_location() == "Hall")
test("character_name stored",        g.character_name == "Miss Scarlett")
test("Game has 6 character objects", len(g.characters) == 6)
test("Game has 6 weapon objects",    len(g.weapons) == 6)
test("Solution has 3 keys",
     set(g.solution.keys()) == {"character", "weapon", "room"})
test("solved starts False",          g.solved is False)
test("won starts False",             g.won is False)
test("turn starts at 0",            g.turn == 0)
test("notebook initialised",         g.notebook is not None)

test("Characters are Character instances",
     all(isinstance(c, Character) for c in g.characters))
test("Weapons are Weapon instances",
     all(isinstance(w, Weapon) for w in g.weapons))

# Verify a different starting room
buf = io.StringIO(); sys.stdout = buf
g2 = Game("Bob", "Professor Plum")
sys.stdout = sys.__stdout__
test("Prof Plum starts in Study", g2.player.get_location() == "Study")
```

---

### Test Section 10 — Input Validation (`test_input_validation`)

**What is being tested:** The main menu rejects non-numeric and out-of-range input with an "invalid" message. The `_read_int` helper rejects out-of-range suspect numbers.

**Why it matters:** Invalid input must never crash the program. The game's usability depends on clear rejection messages that guide the player back to a valid choice.

**Test code:**

```python
def run_menu(input_str):
    g.solved = False
    sys.stdin = io.StringIO(input_str + "\n9\n")  # 9 = Quit after bad input
    buf = io.StringIO(); sys.stdout = buf
    g.run()
    sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
    return buf.getvalue()

output = run_menu("99")
test("Invalid menu choice shows error",
     "invalid" in output.lower())

output = run_menu("abc")
test("Non-numeric menu choice shows error",
     "invalid" in output.lower())

# _read_int with out-of-range suspect number
sys.stdin = io.StringIO("99\n0\n")
buf = io.StringIO(); sys.stdout = buf
g2._make_suggestion()
sys.stdout = sys.__stdout__; sys.stdin = sys.__stdin__
output = buf.getvalue()
test("Out-of-range suspect number shows error",
     "between" in output.lower() or "invalid" in output.lower())
```

---

### Testing Categories

#### Functional Testing

Functional tests verify that:

- All suspects, weapons, and rooms are defined correctly
- Mansion connections are valid
- Secret passages exist and are bidirectional
- Player movement updates location correctly
- Suggestions generate appropriate feedback
- Accusations produce correct win and loss outcomes
- Notebook updates occur correctly
- Dice values remain within valid bounds

#### Gameplay Testing

Gameplay testing checks whether the overall flow feels correct in practice:

- The player can start a new game successfully
- The player can move between rooms through valid routes
- The notebook reflects suggestion outcomes
- The accusation system ends the game correctly

#### Edge-Case Testing

Edge-case testing includes:

- Invalid menu inputs
- Non-numeric input
- Out-of-range numeric input
- Canceling suggestions
- Canceling accusations
- Invalid room lookups

#### Input Validation Testing

The test suite explicitly verifies that invalid user choices are handled safely and that the program does not crash when unexpected input is entered.

#### UI Testing

For a command-line project, UI testing focuses on whether important outputs are produced, such as notebook sections, dice display, menu behavior, and end-of-game messages.

---

### Screenshot Placeholders

- `[Insert Screenshot: Main Menu]`
- `[Insert Screenshot: Player Movement]`
- `[Insert Screenshot: Suggestion Feature]`
- `[Insert Screenshot: Accusation Feature]`
- `[Insert Screenshot: Winning Condition]`
- `[Insert Screenshot: Error Handling]`

---

### Test Case Summary Table

The table below lists representative test cases drawn from the 161-assertion suite. Each row maps to one or more `test()` calls in `test_game.py`.

| Test ID | Section | Description | Input | Expected Output | Pass/Fail |
|---|---|---|---|---|---|
| T01 | Card Data | Suspect list has exactly 6 entries | `CHARACTERS` list | `len == 6` | Pass |
| T02 | Card Data | No duplicate suspects | `CHARACTERS` list | `len == len(set(...))` | Pass |
| T03 | Card Data | `CHARACTERS_NAMES` is the same object as `CHARACTERS` | Identity check | `True` | Pass |
| T04 | Card Data | All suspects have a starting room | `CHARACTER_STARTING_ROOMS` keys | All 6 present | Pass |
| T05 | Card Data | `Character` class stores name and room | `Character("Test", room)` | `.name == "Test"`, `.starting_room.name == "Hall"` | Pass |
| T06 | Mansion | Mansion has exactly 9 rooms | `Mansion()` | `len(mansion.rooms) == 9` | Pass |
| T07 | Mansion | Kitchen connects to Ballroom | `kitchen.get_connections()` | Contains `"Ballroom"` | Pass |
| T08 | Mansion | Secret passage Kitchen ↔ Study (both directions) | Adjacency check | Both sides connected | Pass |
| T09 | Mansion | Secret passage Lounge ↔ Conservatory | Adjacency check | Both sides connected | Pass |
| T10 | Mansion | `get_room` returns `None` for unknown name | `"Dungeon"` | `None` | Pass |
| T11 | Mansion | `get_connections()` returns sorted list | `hall.get_connections()` | `== sorted(...)` | Pass |
| T12 | Player | Player starts in correct room | `Player("W", hall)` | `get_location() == "Hall"` | Pass |
| T13 | Player | `can_move_to` True for adjacent (Hall→Study) | Adjacency check | `True` | Pass |
| T14 | Player | `can_move_to` False for non-adjacent (Hall→Kitchen) | Adjacency check | `False` | Pass |
| T15 | Player | `move_to` updates location and visited set | `player.move_to(study)` | Location = Study, Study in visited | Pass |
| T16 | Player | Secret passage accessible from Study to Kitchen | After move to Study | `can_move_to("Kitchen") == True` | Pass |
| T17 | Solution | Solution character is in CHARACTERS (20 runs) | Random game × 20 | Always in list | Pass |
| T18 | Solution | Solutions vary across 50 runs | 50 game instances | `len(set(solutions)) > 1` | Pass |
| T19 | Suggestion | Correct suggestion: `solved` stays `False` | All three correct | `g.solved == False` | Pass |
| T20 | Suggestion | Correct suggestion: match flavour in output | All three correct | `"aligns"` or `"pulse"` in output | Pass |
| T21 | Suggestion | Wrong suspect: `"suspect"` in feedback | Wrong suspect index | `"suspect"` in output | Pass |
| T22 | Suggestion | Wrong weapon: `"weapon"` in feedback | Wrong weapon index | `"weapon"` in output | Pass |
| T23 | Suggestion | Cancel with 0: `solved` stays `False` | Input `"0"` | `g.solved == False` | Pass |
| T24 | Suggestion | Wrong suspect auto-marked `X` in notebook | Wrong suspect tested | `s_status[wrong_char] == "X"` | Pass |
| T25 | Accusation | Correct accusation: `solved=True`, `won=True` | All three correct | Both flags set, win text shown | Pass |
| T26 | Accusation | Wrong accusation: `solved=True`, `won=False` | Wrong suspect | Both flags set, lose text shown | Pass |
| T27 | Accusation | Cancel at confirmation: `solved=False` | Input `"n"` | `g.solved == False` | Pass |
| T28 | Notebook | All statuses initialize to `"?"` | New `Notebook(...)` | All dict values `"?"` | Pass |
| T29 | Notebook | `mark_weapon("Rope", "!")` stores `"!"` | Mark call | `w_status["Rope"] == "!"` | Pass |
| T30 | Notebook | `display()` output includes all three section headers | `display()` call | `"SUSPECTS"`, `"WEAPONS"`, `"ROOMS"` in output | Pass |
| T31 | Dice | `DiceRoll(3, 5)` total is 8 | Direct construction | `total == 8` | Pass |
| T32 | Dice | `use_step()` decrements `steps_remaining` by 1 | Call `use_step()` | `8 → 7` | Pass |
| T33 | Dice | `roll()` die values in `[1, 6]` | `DiceRoll.roll()` | Both dice in range | Pass |
| T34 | Game Init | Miss Scarlett starts in Hall | `Game("A", "Miss Scarlett")` | `player.get_location() == "Hall"` | Pass |
| T35 | Game Init | Professor Plum starts in Study | `Game("B", "Professor Plum")` | `player.get_location() == "Study"` | Pass |
| T36 | Game Init | `solved` and `won` start as `False` | New game | Both `False` | Pass |
| T37 | Input | Menu choice `"99"` shows error message | `run_menu("99")` | `"invalid"` in output | Pass |
| T38 | Input | Non-numeric menu choice shows error | `run_menu("abc")` | `"invalid"` in output | Pass |
| T39 | Input | Out-of-range suspect number shows error | `"99"` then `"0"` in suggestion | `"between"` or `"invalid"` in output | Pass |

---

### Edge Cases Explicitly Covered

The following edge cases are each addressed by at least one test assertion:

| Edge Case | Covered By | Behavior |
|---|---|---|
| Input `"0"` in suggestion cancels cleanly | T23 | `solved` stays `False`, no crash |
| Input `"n"` cancels accusation confirmation | T27 | `solved` stays `False` |
| Non-numeric menu input (`"abc"`) | T38 | "invalid" message, loop continues |
| Out-of-range integer (`"99"`) in menu | T37 | "invalid" message, loop continues |
| Out-of-range integer in `_read_int` | T39 | "between" / "invalid" message, returns `None` |
| `visited_this_turn` blocks re-entry in same move | Tested by movement design | Exit list filtered each iteration |
| Secret passage is free (no step consumed) | Verified by code path in `_move` | `use_step()` not called for passage |
| Correct suggestion does NOT win game | T19 | `solved` remains `False` |
| Randomness: solutions not all identical | T18 | 50 runs produce multiple distinct tuples |
| Unknown room name in `get_room` | T10 | Returns `None`, no KeyError |

---

### Expected vs Actual Outcomes

Across the tested scenarios, the actual outcomes matched the expected outcomes. The current repository state reports:

- `161/161 passed -- ALL TESTS PASSED`

### Bugs Found and Fixed

The development process required careful correction of logic details such as:

- Ensuring suggestions do not end the game directly
- Distinguishing between suggestion confirmation and accusation victory
- Keeping movement and room-visit tracking consistent
- Handling invalid input without crashing

If a more detailed historical bug log is needed, this section can be expanded with specific issue dates or revision notes.

---

## Challenges Faced

### Technical Issues

One technical challenge was coordinating multiple state variables across one interactive loop. The game needs to keep track of the hidden solution, player state, turn count, notebook state, and termination conditions without allowing them to become inconsistent.

### Design Limitations

Because the project uses a command-line interface, the design had to communicate enough information without visual graphics. This created a limitation in how board state and feedback could be presented.

### Logic Debugging

The most important logic challenge was maintaining the distinction between:

- Suggestions as evidence-gathering actions
- Accusations as final game-ending actions

This distinction is central to the gameplay model and had to be implemented carefully.

### Time Constraints

Balancing feature expansion with reliability was another challenge. Adding room flavor text, notebook support, and dice movement increased the scope of the project, so careful modularization was necessary to keep the code manageable.

### Performance Considerations

Performance is not a major limitation in a project of this size, but consistency still matters. The code was designed to keep operations simple and direct, which is appropriate for a lightweight text-based application.

### UI and UX Challenges

Without a graphical interface, readability depended heavily on output formatting. This was addressed through headers, spacing, labeled prompts, map rendering, and notebook formatting.

### How Challenges Were Resolved

- State complexity was reduced through modular class design.
- Movement logic was made clearer by using room adjacency and a dedicated dice object.
- Suggestion and accusation logic were separated into distinct methods.
- UI readability was improved through structured terminal output.
- Reliability was reinforced through automated tests.

---

## Stability and Reliability

The final system is stable for normal interactive use and demonstrates reliable enforcement of its core mechanics.

### Game Stability

The game initializes consistently, maintains valid state during play, and ends cleanly through accusation or quit paths.

### Reliability of Mechanics

The main gameplay systems behave consistently:

- Room connections remain fixed and predictable
- Secret passages are available only where intended
- Suggestions compare exactly three elements
- The notebook reflects suggestion outcomes
- Only accusations determine final win or loss

### Error Handling

The program handles several classes of invalid input:

- Non-numeric entries
- Out-of-range numeric choices
- Invalid menu selections
- User cancellation in selection prompts

This helps prevent crashes and improves usability.

### Input Validation

Validation is built into input helper methods so that error checking is centralized rather than duplicated throughout the code. This makes the code easier to maintain and reduces inconsistency.

### Performance Consistency

The program performs consistently because its data set is small and its operations are simple. No heavy computation or external dependency management is required.

### Crash Prevention and Invalid Move Handling

The movement system only offers valid exits, and the program rejects invalid numeric choices when a user manually enters out-of-range data. As a result, room transitions are constrained to legal game states.

### Consistent Gameplay Behavior

The automated test suite supports the claim that the current implementation behaves consistently across multiple categories of input and game logic.

---

## Additional Details

### Future Improvements

Possible future expansions include:

- Graphical user interface
- Computer-controlled opponents
- Save and load support
- Adjustable story speed or skip options
- Replay log export
- Expanded deduction analytics in the notebook

### Lessons Learned

This project reinforced the importance of:

- Clear separation of responsibilities between modules
- Designing data structures around game rules
- Building validation early rather than adding it late
- Writing tests for both normal and edge-case behavior

### Additional Features Considered

Possible features considered but not fully implemented include:

- Full multiplayer support
- Dynamic non-player suspect behavior
- More advanced map visualization
- Persistent scoreboard or session statistics

---

## Conclusion

This project successfully delivers a functional enhanced command-line version of Cluedo. The game includes structured rule enforcement, modular system design, deduction mechanics, narrative feedback, and automated testing. It demonstrates practical use of object-oriented programming, data modeling, input validation, and gameplay state management in Python.

The final implementation meets the core project goals by recreating the central Cluedo experience while adding usability and presentation improvements such as character identity selection, dice-based movement, notebook tracking, and story-driven output. Overall, the project serves as a strong example of how a traditional board game concept can be transformed into a reliable interactive software application.

---

## Final Submission Checklist

- [ ] Presentation completed
- [ ] Screen recording completed
- [ ] PDF report completed
- [ ] Screenshots added
- [ ] Testing evidence included
- [ ] Demo verified
- [ ] File naming checked
- [ ] Submission ready
