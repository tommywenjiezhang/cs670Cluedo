# Cluedo -- Enhanced Edition (Project 2)

**Student:** Wenjie Zhang  
**Project:** Project 2 -- Part 1  

---

## Description

A fully immersive, text-based, single-player implementation of the classic board game **Cluedo (Clue)**.
The player chooses a suspect identity, explores a nine-room mansion by rolling dice, gathers clues
through suggestions, and must make one final accusation to win or lose.

### Features

- Opening story intro with typewriter-style dramatic text
- Character selection -- choose one of 6 suspects, each with a unique personality and starting room
- Turn counter displayed in every menu header
- Dice rolling (2d6) for movement with step-by-step room navigation
- Unique atmospheric description for each of the 9 rooms (shown on first visit)
- Detective notebook -- automatically marks ruled-out suspects, weapons, and rooms
- Suggestion feedback with flavour text instead of bare element lists
- Final accusation mechanic -- the only way to win or lose (suggestions gather clues only)
- Win and lose story endings with dramatic text
- ASCII title banner and ASCII mansion floor plan with current-room marker

---

## Requirements

- **Python 3.7 or later** (no third-party packages needed)
- Works on Windows, macOS, and Linux

Check your Python version:

```
python --version
```

---

## Folder Structure

```
WenjieZhang_Project2_SourceCode/
|
+-- main.py        -- Entry point; run this to start the game
+-- game.py        -- Game class: menu loop, movement, suggestions, accusation
+-- mansion.py     -- Room and Mansion classes (board layout + ASCII map)
+-- player.py      -- Player class (location, movement, visited-rooms tracking)
+-- cards.py       -- Card data: CHARACTERS, WEAPONS, ROOMS, Character, Weapon
+-- story.py       -- All story text, dramatic_print(), FAST_MODE flag
+-- dice.py        -- DiceRoll class with ASCII die faces
+-- notebook.py    -- Notebook class: auto-marking and two-column display
+-- README.md      -- This file
```

---

## How to Run

### Play the game

```
cd path\to\WenjieZhang_Project2_SourceCode
python main.py
```

### Run the automated test suite

```
python test_game.py
```

Expected output: `RESULTS: 161/161 passed -- ALL TESTS PASSED`

### Run the automated solver

```
python auto_solve.py
```

The solver uses a real investigation strategy: visits all 9 rooms in BFS order from Hall,
makes one suggestion per room to eliminate suspects/weapons/rooms, and accuses as soon as
exactly one of each remains. Prints a room-by-room elimination table before the live run.

---

## Gameplay Instructions

### Starting the game

1. The opening story plays with a typewriter effect.
2. Enter your detective name (press Enter to accept "Detective").
3. Choose your character from the list -- you will start in that character's canonical room.

### Characters and starting rooms

| # | Character         | Starts in     | Personality |
|---|-------------------|---------------|-------------|
| 1 | Miss Scarlett     | Hall          | Charming and calculating |
| 2 | Colonel Mustard   | Lounge        | Prefers direct solutions |
| 3 | Mrs. White        | Kitchen       | Sees everything, says little |
| 4 | Mr. Green         | Billiard Room | Nervous and eager to please |
| 5 | Mrs. Peacock      | Library       | Aristocratic composure |
| 6 | Professor Plum    | Study         | Finds murder intellectually interesting |

### Main Menu (options 1-9)

| # | Action |
|---|--------|
| 1 | Move -- roll 2d6 and spend steps to hop between rooms |
| 2 | Make a Suggestion in your current room |
| 3 | Make an Accusation -- your ONE chance to win or lose |
| 4 | View Detective's Notebook |
| 5 | View Room Description |
| 6 | View Mansion Map |
| 7 | View Suspects |
| 8 | View Weapons |
| 9 | Quit (reveals the solution) |

### Moving between rooms

- Choose **1** to roll the dice. Two dice (2d6) are shown in ASCII art.
- Your total roll is your step budget for this turn.
- Each hop to an adjacent room costs 1 step.
- After each hop you are asked "Continue moving? (y/n)". Enter **n** to stop early.
- You cannot revisit a room you already passed through in the same turn.
- **Secret passages** (Kitchen <-> Study and Lounge <-> Conservatory) are free -- no step cost.
  Enter **P** at the movement prompt to take one.

### Making a suggestion

A suggestion is fixed to your current room. Choose a suspect and weapon.

- If all three elements (suspect, weapon, room) match the solution: the notebook marks them confirmed `[!]`
  and you are told you are close. **You do not win yet** -- you must Accuse.
- Wrong elements are marked `[X]` in the notebook automatically and flavour feedback is shown.

### Making the final accusation

Choose **3** from the menu. You will pick a suspect, a weapon, **and a room** (not fixed to current location).

- **Correct accusation** -- the WIN story plays and the case is closed.
- **Wrong accusation** -- the LOSE story plays and the game ends. The true solution is revealed.

You only get one accusation. Use suggestions to gather evidence before committing.

### Notebook legend

| Symbol | Meaning |
|--------|---------|
| `[?]`  | Unknown -- not yet investigated |
| `[X]`  | Ruled out -- this element was wrong in a suggestion |
| `[!]`  | Confirmed -- all three elements of a suggestion matched |

---

## Mansion Layout

```
  [Kitchen ]---[Ballroom]---[Conserv.]
       |                        |
  [DiningRm]             [Billiard ]
       |                    |   |
  [Lounge  ]---[ Hall   ]---+ [Library]
                    |              |
                [ Study  ]---------+

  Secret passages:  Kitchen <~~> Study
                    Lounge  <~~> Conservatory
```

---

## Example Session (abbreviated)

```
  AUTO-SOLVER -- pre-game analysis
  Solution suspect : Professor Plum
  Solution weapon  : Revolver
  Solution room    : Study
  Starting room    : Hall
  Route to win     : Hall -> Study
  Hops needed      : 1

  [INPUT] '1'  -- menu: Move (roll dice)
  [INPUT] '3'  -- exit #3: Study  (from Hall)
  [INPUT] 'n'  -- stop moving after this hop

  [INPUT] '2'  -- menu: Make a Suggestion
  [INPUT] '6'  -- suspect #6: Professor Plum
  [INPUT] '2'  -- weapon  #2: Revolver

  [INPUT] '3'  -- menu: Make an Accusation
  [INPUT] 'y'  -- confirm the accusation
  [INPUT] '6'  -- suspect #6: Professor Plum
  [INPUT] '2'  -- weapon  #2: Revolver
  [INPUT] '9'  -- room    #9: Study

  * * *  CASE CLOSED  * * *
```

---

## Feature Checklist

| Feature | Status |
|---------|--------|
| Nine-room mansion with connections | Done |
| Secret passages (Kitchen<->Study, Lounge<->Conservatory) | Done |
| Six suspects with starting rooms | Done |
| Six weapons placed randomly | Done |
| Random murder solution at startup | Done |
| Opening story intro (dramatic typewriter effect) | Done |
| Character selection with personality intros | Done |
| Turn counter in menu header | Done |
| Dice rolling (2d6) with ASCII die art | Done |
| Step-by-step movement with budget | Done |
| Unique room descriptions on first visit | Done |
| Detective notebook with auto-marking | Done |
| Suggestion feedback with flavour text | Done |
| Final accusation (only win/lose path) | Done |
| Win story ending | Done |
| Lose story ending | Done |
| ASCII title banner | Done |
| ASCII mansion floor plan with current-room marker | Done |
| Input validation throughout | Done |
| Automated test suite (161 tests) | Done |
| BFS auto-solver script | Done |

---

## Notes

- The murder solution is selected randomly each run, so every game is different.
- No external libraries are used -- only the Python standard library (`random`, `time`, `sys`, `io`, `collections`).
- `story.FAST_MODE = True` disables the typewriter delay for tests and the auto-solver.

---

## Submission Checklist

Before submitting to Canvas:

1. Confirm the game runs with `python main.py`.
2. Confirm all tests pass with `python test_game.py`.
3. Make sure all files are present inside `WenjieZhang_Project2_SourceCode/`.
4. **Zip the entire folder:**
   - Windows: right-click the folder > Send to > Compressed (zipped) folder
   - Terminal: `zip -r WenjieZhang_Project2_SourceCode.zip WenjieZhang_Project2_SourceCode/`
5. Upload the `.zip` file to the Canvas assignment portal.
