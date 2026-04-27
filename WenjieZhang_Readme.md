# Cluedo -- (Project 2 Part 1)

**Student:** Wenjie Zhang  
**Project:** Project 2 -- Part 1  


## How to Run

### Play the game

```
python main.py
```

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
- The feedback is partial when only some parts are wrong. In the recorded session, for example,
  `Professor Plum + Wrench + Ballroom` only ruled out the room, while repeated guesses in other
  rooms eventually isolated `Hall` as the only remaining location.

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

## Live Gameplay Demonstration

Here's a complete recorded playthrough. The walkthrough below follows that
session step by step so a reader can see how the game actually unfolds in practice.

1. The recorded game opens at **Turn 0** with the player using the default detective name,
   playing as **Miss Scarlett**, and starting in the **Hall**.
2. The first action is a suggestion in the Hall: **Miss Scarlett + Candlestick + Hall**.
   The response says the suspect and weapon are wrong, but the room is not ruled out.
3. The notebook is opened immediately after. It shows `[X] Miss Scarlett`, `[X] Candlestick`,
   and a personal note: `Turn 0: Miss Scarlett, Candlestick, Hall -- suspect, weapon wrong.`
4. The player then chooses **Move**, rolls an 11, and travels from **Hall** to **Billiard Room**.
   After arriving, the room's first-visit description is printed, and the player stops moving.
5. On **Turn 1**, the player suggests **Colonel Mustard + Revolver + Billiard Room**.
   The game replies that nothing aligns, which means all three parts are wrong.
6. The notebook now marks **Colonel Mustard**, **Revolver**, and **Billiard Room** with `[X]`
   and adds the Turn 1 note showing that the entire theory was incorrect.
7. The player moves again, going from **Billiard Room** to **Conservatory**. No suggestion is made
   on Turn 2; the turn is used only for repositioning.
8. From the Conservatory, the movement menu shows a secret-passage option to the Lounge, but the
   player walks normally into the **Lounge** instead. This demonstrates that a room can offer both
   standard exits and a free passage on the same turn.
9. On **Turn 3**, the suggestion is **Mrs. White + Rope + Lounge**. The response again says
   nothing aligns, so the suspect, weapon, and room are all eliminated together.
10. Later in the session, the player reaches the **Study** and on **Turn 5** suggests
    **Mr. Green + Lead Pipe + Study**. That entire combination is wrong, so another suspect,
    weapon, and room are ruled out.
11. The transcript then shows the player using secret-passage routes during exploration, including
    passage prompts such as **Conservatory -> Lounge**, **Lounge -> Conservatory**, **Study -> Kitchen**,
    and **Kitchen -> Study**. These examples demonstrate that passage travel costs no movement steps.
12. On **Turn 8**, the player suggests **Mrs. Peacock + Knife + Conservatory**. This also fails
    completely, leaving only one suspect and one weapon still unknown.
13. By **Turn 10**, the remaining likely pair is **Professor Plum + Wrench**. The player tests that
    pair in the **Library**, and the notebook records `room wrong`, meaning the suspect and weapon stay
    viable while only the Library is eliminated.
14. The same pair is then tested room by room as the player narrows the final location:
    **Turn 13** uses **Professor Plum + Wrench + Dining Room** and rules out the room only.
15. On **Turn 14**, **Professor Plum + Wrench + Kitchen** is suggested and again the notebook records
    `room wrong`, leaving fewer possible rooms.
16. On **Turn 15**, the player moves from **Kitchen** to **Ballroom**, makes the suggestion
    **Professor Plum + Wrench + Ballroom**, and the game again says the room is wrong.
17. The notebook is checked one last time. At this point every suspect except **Professor Plum**,
    every weapon except **Wrench**, and every room except **Hall** is marked `[X]`.
18. The player selects **Make an Accusation**, confirms with `y`, and enters
    **Professor Plum + Wrench + Hall**.
19. The accusation is correct. The winning ending text plays, followed by the closing banner
    `CASE CLOSED`.

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
