# Project 2 Part 2: Screen Recording Demo Plan

## Demo Objective

This demo plan is designed for a manual screen recording of the current Cluedo project implementation. The goal is to show a smooth, professional walkthrough of the game while explaining both gameplay and technical behavior.

The plan assumes the game is run from the terminal with:

```bash
python main.py
```

---

## Pre-Recording Setup

### Technical setup

- Use a screen resolution of at least 1920x1080 if available.
- Use a clear monospace terminal font at a readable size.
- Maximize the terminal window before recording.
- Close unrelated applications and notifications.
- If possible, enable microphone noise reduction.

### Content setup

- Run one practice round before the final recording.
- Keep a small reference note nearby with the planned demo steps.
- Decide in advance which character to choose and which actions to demonstrate.
- If needed, rehearse a short explanation of the game objective before launching.

### Recording quality guidance

- Record in 1080p and 30 frames per second or better.
- Move the cursor slowly and deliberately.
- Avoid rapid scrolling or hurried typing.
- Pause briefly after major outputs so viewers can read the screen.
- Speak in a steady, professional tone.

---

## Suggested Demo Structure

The strongest demo flow is:

1. Launch the game
2. Explain setup and character selection
3. Show the main menu
4. Demonstrate movement and room navigation
5. Demonstrate room descriptions and map display
6. Demonstrate a suggestion
7. Demonstrate notebook tracking
8. Demonstrate accusation logic
9. Show either a win or loss ending
10. Show quit or restart workflow if needed

Target length: 4 to 6 minutes for the demo itself.

---

## Step-by-Step Demo Sequence

## Step 1: Launching the Game

**What should appear on screen:**

- Terminal window
- Command entry: `python main.py`
- Introductory story text
- ASCII title banner

**What action to perform:**

- Type `python main.py`
- Wait for the intro and banner to display

**What to explain verbally:**

This project is a digital command-line version of Cluedo built in Python. The game begins with a short story introduction to establish the mystery setting at Blackwell Manor before moving into player setup.

---

## Step 2: Enter Detective Name

**What should appear on screen:**

- Prompt asking for detective name

**What action to perform:**

- Enter a name such as `Wenjie` or `Detective`

**What to explain verbally:**

At the start of the game, the player enters a detective name. If the player presses Enter without typing anything, the game assigns a default name. This is a small usability feature that avoids forcing extra input.

---

## Step 3: Character Selection and Starting Room

**What should appear on screen:**

- List of six suspects
- Canonical starting room for each suspect
- Personality descriptions

**What action to perform:**

- Choose one suspect identity
- Recommended choice for demo: `Miss Scarlett`

**What to explain verbally:**

The player chooses a suspect identity at the start of the game. This affects the starting room because each character has a predefined canonical location. This feature adds personality and variation to the opening state of the game.

---

## Step 4: Show the Main Menu

**What should appear on screen:**

- Current location display
- Main action menu with options 1 through 9

**What action to perform:**

- Pause on the menu for a moment

**What to explain verbally:**

The game is controlled through a turn-based menu. From here, the player can move, make a suggestion, make an accusation, view the notebook, inspect the room description, display the mansion map, review characters and weapons, or quit.

---

## Step 5: Demonstrate Character Movement

**What should appear on screen:**

- Dice roll output
- ASCII dice art
- Number of remaining steps
- List of reachable rooms

**What action to perform:**

- Select `1` for Move
- Move to at least one adjacent room
- If enough steps remain, move to a second room
- Stop moving manually before all steps are used, or continue until the step budget is exhausted

**What to explain verbally:**

Movement uses two six-sided dice, and the total determines how many room-to-room steps are available during that turn. Each normal room hop costs one step. The player may also stop early, which gives more control over strategy.

Also explain that the game prevents revisiting rooms within the same movement turn, which avoids wasteful loops and helps enforce clean turn logic.

---

## Step 6: Demonstrate Secret Passage or Room Navigation

**What should appear on screen:**

- Prompt showing `P` as a secret passage option if the player is in the correct room

**What action to perform:**

- If the current room supports it, use the secret passage
- If not, explain the secret passage rule verbally and instead continue normal room navigation

**What to explain verbally:**

Two secret passages are built into the mansion: Kitchen to Study and Lounge to Conservatory. These passages are free and do not consume movement steps, which adds a strategic shortcut system to the game.

---

## Step 7: Demonstrate Room Description and Mansion Map

**What should appear on screen:**

- Room description text
- ASCII mansion map

**What action to perform:**

- Select `5` to view the current room description
- Select `6` to display the mansion map

**What to explain verbally:**

Room descriptions add narrative detail and help the project feel more complete. The mansion map helps the player understand room adjacency and current position, which is important for planning movement and deduction.

---

## Step 8: Demonstrate Suggestion System

**What should appear on screen:**

- Suggestion header
- Current room fixed automatically
- Suspect and weapon selection lists
- Feedback text identifying incorrect elements

**What action to perform:**

- Select `2` to make a suggestion
- Choose one suspect and one weapon
- Let the game process the suggestion

**What to explain verbally:**

Suggestions are the main deduction tool in the game. The player selects a suspect and a weapon, while the room is automatically set to the current room. The system then compares the guess to the hidden solution and reports which elements are incorrect.

Also explain that suggestions do not directly win the game. Even if all three elements match, the player must still use the accusation option to officially solve the case.

---

## Step 9: Demonstrate Notebook Tracking

**What should appear on screen:**

- Detective notebook
- Status markers for suspects, weapons, and rooms
- Personal notes section

**What action to perform:**

- Select `4` to open the notebook

**What to explain verbally:**

The notebook is a key usability feature. It automatically records ruled-out and confirmed information after suggestions. The symbols mean unknown, ruled out, and confirmed. This reduces player memory load and makes the deduction process easier to follow.

---

## Step 10: Demonstrate Accusation Logic

**What should appear on screen:**

- Warning about one accusation only
- Confirmation prompt
- Suspect, weapon, and room selection

**What action to perform:**

- Select `3` to make an accusation
- If you want to show caution first, answer `n` once to cancel
- Then reopen accusation and answer `y`

**What to explain verbally:**

The accusation system is the final decision point. Unlike suggestions, an accusation requires all three elements explicitly, including the room, and the player only gets one chance. A correct accusation wins the game, while an incorrect one ends the investigation immediately.

---

## Step 11: Show Winning or Losing Scenario

**What should appear on screen:**

- Story ending text
- Case closed or case unsolved message

**What action to perform:**

- Complete the accusation
- Let the full ending text appear without rushing

**What to explain verbally:**

This ending demonstrates the full result of the game logic. The project includes separate narrative endings for success and failure, which reinforces the rule that the accusation is the only true win or lose path.

---

## Step 12: Demonstrate Quit Option if Time Allows

**What should appear on screen:**

- Menu option `9`
- Revealed solution
- Exit message

**What action to perform:**

- If the game is still running and time permits, choose `9`

**What to explain verbally:**

The quit option safely ends the game and reveals the hidden solution. This is useful both for testing and for user convenience.

---

## Recommended Spoken Flow

- Open with the project purpose in one sentence.
- Explain each feature only when it appears on screen.
- Keep technical explanations short but precise.
- Avoid reading menus word-for-word unless needed.
- Pause briefly after important outputs such as notebook updates or accusation results.

---

## Demo Verification Checklist

- Game launches correctly
- Intro and title banner are visible
- Detective name input works
- Character selection is shown
- Main menu is clearly visible
- Dice-based movement is demonstrated
- Room adjacency or secret passage is shown
- Room description is shown
- Mansion map is shown
- Suggestion system is demonstrated
- Notebook tracking is demonstrated
- Accusation system is demonstrated
- Win or loss ending is shown
- Audio is clear and easy to follow

---

## Recording Tips for a Professional Result

- Keep the terminal centered and uncluttered.
- Do not type too quickly when entering choices.
- If you make a mistake during recording, pause and restart the segment instead of trying to talk over it.
- Keep your explanation focused on purpose, behavior, and reliability.
- End the demo with a short closing line such as: `This completes the demonstration of the Cluedo game and its main gameplay systems.`
