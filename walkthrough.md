# Cluedo – Digital Edition: Complete Walkthrough

This guide walks you through every step of playing the game, from launching it to
identifying the murderer. Use it as a reference while playing or read it start to
finish to understand the strategy.

---

## Table of Contents

1. [Starting the Game](#1-starting-the-game)
2. [Understanding the Mansion](#2-understanding-the-mansion)
3. [The Main Menu](#3-the-main-menu)
4. [Moving Between Rooms](#4-moving-between-rooms)
5. [Making Suggestions](#5-making-suggestions)
6. [Reading the Feedback](#6-reading-the-feedback)
7. [Elimination Strategy](#7-elimination-strategy)
8. [Full Example Playthrough](#8-full-example-playthrough)
9. [Quick-Reference Cheat Sheet](#9-quick-reference-cheat-sheet)

---

## 1. Starting the Game

Open a terminal, navigate to the project folder, and run:

```
python main.py
```

You will see:

```
================================================
         CLUEDO  –  Part 1  (Python Edition)
================================================
Enter your detective name:
```

Type any name and press **Enter**. If you just press Enter without typing anything,
the game defaults to "Detective".

```
Enter your detective name: Wenjie
```

The welcome screen appears and the game places you in the **Hall** to begin.

---

## 2. Understanding the Mansion

There are **9 rooms**. Each room connects to 2–4 neighbours. Two **secret passages**
let you jump across the mansion in a single move.

```
                    MANSION LAYOUT
    ┌──────────┬──────────────┬───────────────┐
    │  Kitchen │   Ballroom   │ Conservatory  │
    │          ├──────────────┤               │
    │          │              │               │
    ├──────────┤              ├───────────────┤
    │Dining Rm │              │  Billiard Rm  │
    │          │              │               │
    ├──────────┤              ├───────────────┤
    │  Lounge  │    Hall      │    Library    │
    │          │              │               │
    └──────────┴──────────────┴───────────────┤
                                    Study      │
                               ───────────────┘
```

### Room Connections

| Room          | Connected Rooms                              |
|---------------|----------------------------------------------|
| Kitchen       | Ballroom, Dining Room, **Study** *           |
| Ballroom      | Kitchen, Conservatory                        |
| Conservatory  | Ballroom, Billiard Room, **Lounge** *        |
| Dining Room   | Kitchen, Lounge                              |
| Billiard Room | Conservatory, Hall, Library                  |
| Library       | Billiard Room, Study                         |
| Lounge        | Conservatory *, Dining Room, Hall            |
| Hall          | Billiard Room, Lounge, Study                 |
| Study         | Hall, Kitchen *, Library                     |

`*` = **Secret passage** (diagonal shortcut across the mansion)

### Secret Passages

| From          | To            | Why it matters                         |
|---------------|---------------|----------------------------------------|
| Kitchen       | Study         | Lets you cross from top-left to bottom-right instantly |
| Lounge        | Conservatory  | Lets you cross from bottom-left to top-right instantly |

Use secret passages to cover the whole mansion in fewer moves.

---

## 3. The Main Menu

After every action the main menu reappears:

```
================================================
  MAIN MENU
================================================
  1. View current location
  2. Move to another room
  3. Make a suggestion (in current room)
  4. View suspects
  5. View weapons
  6. View mansion map
  7. Quit and reveal solution
```

Type the **number** of the option you want and press **Enter**.

| Option | When to use it |
|--------|----------------|
| 1 | Check where you are and what exits exist |
| 2 | Move to an adjacent room |
| 3 | Make a suggestion without moving first |
| 4 | Remind yourself of all suspect names |
| 5 | Remind yourself of all weapon names |
| 6 | View the full mansion connection map |
| 7 | Give up and see the answer |

---

## 4. Moving Between Rooms

Select **option 2** from the main menu. You will see a numbered list of rooms
you can legally enter:

```
  Where would you like to go?
    1. Billiard Room
    2. Lounge
    3. Study
    0. Cancel
  Enter number:
```

- Type **1**, **2**, or **3** to move into that room.
- Type **0** to cancel and stay where you are.
- Typing any other number shows an error — no invalid movement is ever allowed.

After moving, the game immediately asks:

```
  Make a suggestion here? (y/n):
```

Type **y** to suggest now (recommended — see Section 5), or **n** to return to
the menu first.

### Movement tip: You cannot skip rooms

If you want to reach the Conservatory from the Hall you need **two moves**:

```
Hall  →  Billiard Room  →  Conservatory
```

Plan your route using the connection table above or option 6 (mansion map).

---

## 5. Making Suggestions

A suggestion is your main detective tool. You pick a **suspect** and a **weapon**;
the **room** is always your current location.

Select **option 3** (or press **y** right after entering a room):

```
================================================
  MAKE A SUGGESTION
================================================
  Room: Library  (fixed to your current location)

  Choose a suspect:
    1. Miss Scarlett
    2. Colonel Mustard
    3. Mrs. White
    4. Mr. Green
    5. Mrs. Peacock
    6. Professor Plum
    0. Cancel
  Suspect number: 6

  Choose a weapon:
    1. Candlestick
    2. Revolver
    3. Rope
    4. Lead Pipe
    5. Knife
    6. Wrench
    0. Cancel
  Weapon number: 3

  >> I suggest it was Professor Plum with the Rope in the Library.
```

The game then tells you whether your guess matched the hidden solution.

### The six suspects

| # | Name              | Starting room  |
|---|-------------------|----------------|
| 1 | Miss Scarlett     | Hall           |
| 2 | Colonel Mustard   | Lounge         |
| 3 | Mrs. White        | Ballroom       |
| 4 | Mr. Green         | Conservatory   |
| 5 | Mrs. Peacock      | Library        |
| 6 | Professor Plum    | Study          |

### The six weapons

| # | Weapon      |
|---|-------------|
| 1 | Candlestick |
| 2 | Revolver    |
| 3 | Rope        |
| 4 | Lead Pipe   |
| 5 | Knife       |
| 6 | Wrench      |

---

## 6. Reading the Feedback

### You guessed correctly

```
  *** Your suggestion matches the solution! ***
  You've solved the mystery – congratulations, Detective!
```

The game ends immediately. You win.

### You guessed incorrectly

```
  Your suggestion is not fully correct. Keep investigating!
  Incorrect element(s): weapon, room.
```

The message tells you **which parts are wrong** (suspect, weapon, and/or room).
Any element **not listed** is correct.

#### Interpreting the feedback

| Feedback message says…       | What it means                             |
|------------------------------|-------------------------------------------|
| `Incorrect element(s): room` | Suspect and weapon are both correct       |
| `Incorrect element(s): suspect, weapon` | The room is correct              |
| `Incorrect element(s): suspect, weapon, room` | Everything is wrong         |
| *(nothing listed)*           | All three are correct — you already won!  |

---

## 7. Elimination Strategy

Because the game tells you exactly which elements are wrong, you can narrow down the
solution systematically. Use a piece of paper or a notes file to track your guesses.

### Step-by-step method

**Step 1 – Lock in the room first.**

Visit each room and make a suggestion there, keeping the suspect and weapon the
same for every guess. Watch whether "room" appears in the incorrect list.

- If "room" is **not** in the list → that room is the murder room. Stop changing rooms.
- If "room" **is** in the list → that room is not the answer; move on.

Example route from Hall (7 moves covers all 9 rooms via secret passages):

```
Hall → Lounge → Conservatory → Billiard Room → Library → Study → Kitchen → Ballroom → Dining Room
```

**Step 2 – Lock in the suspect.**

Once you know the correct room, stay there and make repeated suggestions, changing
only the suspect each time.

- If "suspect" is **not** in the list → that suspect is the murderer.

**Step 3 – Lock in the weapon.**

With room and suspect confirmed, change only the weapon until "weapon" disappears
from the feedback.

**Step 4 – Final accusation.**

Make one last suggestion with all three confirmed elements. The game will
congratulate you and the mystery is solved.

### Tracking sheet (copy this while you play)

```
ROOMS (cross off when confirmed wrong)
[ ] Kitchen      [ ] Ballroom     [ ] Conservatory
[ ] Dining Room  [ ] Billiard Rm  [ ] Library
[ ] Lounge       [ ] Hall         [ ] Study

SUSPECTS (cross off when confirmed wrong)
[ ] Miss Scarlett    [ ] Colonel Mustard  [ ] Mrs. White
[ ] Mr. Green        [ ] Mrs. Peacock     [ ] Professor Plum

WEAPONS (cross off when confirmed wrong)
[ ] Candlestick  [ ] Revolver  [ ] Rope
[ ] Lead Pipe    [ ] Knife     [ ] Wrench

CONFIRMED:
  Room    : _________________
  Suspect : _________________
  Weapon  : _________________
```

---

## 8. Full Example Playthrough

Below is a complete sample game. The hidden solution in this example is:
**Professor Plum · Rope · Library** (you won't know this during play).

---

### Launch and name

```
python main.py

Enter your detective name: Wenjie
```

---

### Turn 1 – Start in Hall, test the room

```
  Location : Hall
  Exits    : Billiard Room, Lounge, Study

Your choice (1-7): 3          ← make a suggestion

  Room: Hall  (fixed to your current location)
  Suspect number: 1           ← Miss Scarlett (placeholder)
  Weapon number: 1            ← Candlestick (placeholder)

  >> I suggest it was Miss Scarlett with the Candlestick in the Hall.

  Your suggestion is not fully correct. Keep investigating!
  Incorrect element(s): suspect, weapon, room.
```

All three wrong. Hall is not the murder room. Move on.

---

### Turn 2 – Move to Lounge

```
Your choice (1-7): 2
  Enter number: 2             ← Lounge
  Make a suggestion here? (y/n): y

  Suspect number: 1           ← Miss Scarlett
  Weapon number: 1            ← Candlestick

  >> I suggest it was Miss Scarlett with the Candlestick in the Lounge.

  Incorrect element(s): suspect, weapon, room.
```

Lounge is not the room either.

---

### Turn 3 – Secret passage: Lounge → Conservatory

```
Your choice (1-7): 2
  Enter number: 1             ← Conservatory (secret passage)
  Make a suggestion here? (y/n): y

  Incorrect element(s): suspect, weapon, room.
```

Not here. Continue.

---

### Turn 4 – Conservatory → Billiard Room

```
Your choice (1-7): 2
  Enter number: 2             ← Billiard Room

  Incorrect element(s): suspect, weapon, room.
```

---

### Turn 5 – Billiard Room → Library

```
Your choice (1-7): 2
  Enter number: 3             ← Library
  Make a suggestion here? (y/n): y

  Suspect number: 1           ← Miss Scarlett
  Weapon number: 1            ← Candlestick

  >> I suggest it was Miss Scarlett with the Candlestick in the Library.

  Your suggestion is not fully correct. Keep investigating!
  Incorrect element(s): suspect, weapon.
```

"room" is **not** listed → **Library is the murder room!**

---

### Turn 6 – Stay in Library, find the suspect

Suggest from Library, changing only the suspect:

```
Your choice (1-7): 3

  Suspect number: 2           ← Colonel Mustard
  Weapon number: 1            ← Candlestick

  Incorrect element(s): suspect, weapon.
```

Mustard is wrong. Try again.

```
Your choice (1-7): 3
  Suspect number: 6           ← Professor Plum
  Weapon number: 1            ← Candlestick

  Incorrect element(s): weapon.
```

"suspect" is **not** listed → **Professor Plum is the murderer!**

---

### Turn 7 – Stay in Library, find the weapon

```
Your choice (1-7): 3
  Suspect number: 6           ← Professor Plum
  Weapon number: 2            ← Revolver

  Incorrect element(s): weapon.
```

Not the Revolver.

```
Your choice (1-7): 3
  Suspect number: 6           ← Professor Plum
  Weapon number: 3            ← Rope

  >> I suggest it was Professor Plum with the Rope in the Library.

  *** Your suggestion matches the solution! ***
  You've solved the mystery – congratulations, Detective!
```

Mystery solved in **7 turns**.

---

## 9. Quick-Reference Cheat Sheet

```
START          python main.py  →  enter name  →  begin in Hall

MENU KEYS      1=location  2=move  3=suggest  4=suspects
               5=weapons   6=map   7=quit+reveal

MOVEMENT       type room number from the exit list  |  0 = cancel

SUGGESTION     pick suspect (1-6)  +  weapon (1-6)
               room is fixed to current location

FEEDBACK       element NOT mentioned = correct
               element IS  mentioned = wrong

SECRET PATHS   Kitchen  ↔  Study
               Lounge   ↔  Conservatory

WIN            all three elements correct in one suggestion

STRATEGY       1. Find the room  (suggest same suspect+weapon in each room)
               2. Find the suspect (stay in room, change only suspect)
               3. Find the weapon  (stay in room, change only weapon)
               4. Final suggestion with all three confirmed = win
```
