# Project 2 Part 2: Cluedo Game Presentation Script

## Presentation Goal

This script is designed for a recording of up to 10 minutes. It is based on the current enhanced command-line implementation in `WenjieZhang_Project2_SourceCode`, which includes character selection, dice-based movement, room descriptions, a detective notebook, and a final accusation system.

---

## Slide 1: Title and Introduction

**Suggested slide title:** `Cluedo Digital Edition - Project 2 Part 2`

**On-screen points:**

- Project overview
- Digital recreation of Cluedo
- Python command-line implementation
- Investigation and deduction gameplay

**Speaker script:**

Hello, my name is [Student Name], and this presentation introduces my Project 2 Cluedo Game. This project is a digital command-line version of Cluedo, also known as Clue, where the player investigates a murder by exploring rooms, testing theories, and making a final accusation. The goal of the game is to determine the correct suspect, weapon, and room before using the one accusation opportunity available in the game.

In this project, I focused on translating the core Cluedo experience into a structured Python program while also adding features that improve usability and immersion, such as character selection, room descriptions, notebook tracking, dice-based movement, and story-driven text output.

**Suggested time:** 45 seconds

---

## Slide 2: Project Objectives

**Suggested slide title:** `Project Objectives`

**On-screen points:**

- Recreate core Cluedo gameplay
- Practice object-oriented programming
- Model rules and turn flow
- Build a reliable interactive system
- Verify behavior with automated testing

**Speaker script:**

The main objectives of this project were both technical and game-focused. From a gameplay perspective, the goal was to recreate the essential Cluedo mechanics: moving through a mansion, making suggestions, tracking evidence, and making a final accusation. From a software engineering perspective, the project was intended to demonstrate object-oriented design, modular program structure, input validation, state management, and testing.

Another goal was to make the game more than just a minimal prototype. I wanted the system to feel complete and consistent, so I implemented supporting features such as room-specific descriptions, a detective notebook, turn-based movement using two dice, and clear win and loss endings. These additions help show how a game can combine logic, data modeling, and user interaction in one application.

**Suggested time:** 50 seconds

---

## Slide 3: Game Overview

**Suggested slide title:** `How the Game Works`

**On-screen points:**

- Intro story and detective name input
- Character identity selection
- Starting room depends on chosen suspect
- Turn-based menu system
- Investigate through movement and suggestions
- Win or lose through accusation

**Speaker script:**

When the program starts, the player sees an introductory story and then enters a detective name. After that, the player chooses one of the six classic suspects as their identity, such as Miss Scarlett or Professor Plum. That decision also affects the player’s starting room, because each character begins in a canonical room defined in the program data.

Once the game begins, the player interacts through a turn-based main menu. On each turn, the player can move by rolling dice, make a suggestion in the current room, view the detective notebook, read the current room description, view the mansion map, or inspect the suspect and weapon lists.

The game is structured around deduction. Suggestions help narrow down the suspect, weapon, and room. However, a suggestion does not end the game, even if it fully matches the hidden solution. To actually win, the player must choose the accusation option and correctly name the suspect, weapon, and room. If the accusation is wrong, the game ends immediately with a losing outcome.

**Suggested time:** 1 minute

---

## Slide 4: Key Features

**Suggested slide title:** `Key Features`

**On-screen points:**

- Character movement with 2d6 dice
- Mansion room navigation
- Secret passages
- Suggestion system
- Final accusation system
- Detective notebook
- Turn-based menu flow
- Story and room flavor text

**Speaker script:**

Several features define the final version of this project.

First, movement is based on rolling two six-sided dice. The total determines how many room-to-room steps the player can take during that turn. This makes navigation more dynamic than simple single-step movement.

Second, the mansion is modeled as a connected room graph. The player can move only to adjacent rooms, and two secret passages provide free movement between opposite corners of the board: Kitchen to Study and Lounge to Conservatory.

Third, the suggestion system allows the player to test a suspect and weapon while the room is automatically fixed to the player’s current location. The game then identifies which parts of the theory are wrong and records that evidence in the detective notebook.

Fourth, the accusation system acts as the final decision point. The player gets one chance to name the full solution. A correct accusation triggers the winning ending, while an incorrect accusation ends the investigation with a loss.

Fifth, the notebook improves the user experience by tracking suspects, weapons, and rooms with status markers. Unknown items are marked with a question mark, ruled-out items are marked with X, and fully confirmed items are marked with an exclamation point.

Finally, the project includes thematic story text, room descriptions, and structured menu output to make the command-line interface clearer and more engaging.

**Suggested time:** 1 minute 10 seconds

---

## Slide 5: Design Choices

**Suggested slide title:** `Design Choices`

**On-screen points:**

- Python standard library only
- Modular architecture
- Object-oriented classes
- Text-based interface
- Dictionary and list driven data
- Graph-based room layout

**Speaker script:**

The project was implemented in Python using only the standard library. This was a practical design choice because it keeps the game portable, easy to run, and suitable for an academic project without external dependencies.

Architecturally, I separated the game into modules with distinct responsibilities. For example, `game.py` handles the overall game loop and turn logic, `mansion.py` models the room network, `player.py` tracks player state, `cards.py` stores suspects, weapons, and room data, `dice.py` handles movement rolls, `notebook.py` manages deduction tracking, and `story.py` stores narrative and feedback text.

I also chose a text-based interface instead of a graphical one. This allowed me to focus on core logic, rule enforcement, and reliability rather than window management or graphics. Even though the project is command-line based, I still made interface decisions such as structured menus, consistent prompts, ASCII art dice, and descriptive text to keep the experience readable and engaging.

For data structures, lists are used for ordered menu content, dictionaries are used for quick lookups such as character starting rooms and notebook status tracking, and room adjacency is modeled through connected `Room` objects, which is effectively a graph structure.

**Suggested time:** 1 minute

---

## Slide 6: Implementation Details

**Suggested slide title:** `Implementation Details`

**On-screen points:**

- `main.py` starts the game
- `Game` class coordinates play
- `Mansion` and `Room` model the board
- `Player` tracks location and visited rooms
- `Notebook` stores deduction state
- `DiceRoll` manages step-based movement

**Speaker script:**

The core implementation is centered around the `Game` class in `game.py`. This class initializes the mansion, randomly selects the hidden solution, places characters and weapons, creates the player object, and runs the main menu loop.

The board itself is implemented through the `Mansion` and `Room` classes. Each room stores its connected neighbors, and the mansion builds all room objects and links them together during initialization. This design makes adjacency checks and map display straightforward.

The `Player` class stores the detective’s name, current room, and visited rooms. The visited-room tracking is important because the movement system prevents revisiting rooms within the same move turn.

The `Notebook` class maintains three status tables for suspects, weapons, and rooms, along with a notes list. This allows suggestion feedback to automatically update the deduction record.

The `DiceRoll` class encapsulates the two-dice result, total movement budget, and remaining steps. It also handles ASCII display of the dice faces.

Input handling is implemented through helper methods in `game.py`, such as `_read_int` and `_read_yes_no`, which validate user entries and prevent common crashes from invalid input.

**Suggested time:** 1 minute

---

## Slide 7: Demo Walkthrough

**Suggested slide title:** `Demo Walkthrough`

**On-screen points:**

- Launch the program
- Enter detective name
- Choose a suspect identity
- Roll dice and move
- View room description and map
- Make suggestion
- Check notebook
- Make final accusation

**Speaker script:**

In the demonstration, I would first launch the game with `python main.py`. The game opens with a story sequence, then asks for the detective name and suspect identity. After character selection, the player starts in the assigned room for that suspect.

Next, I would show the turn menu and choose the movement option. This demonstrates the dice roll, step counting, available exits, and optional use of secret passages. I would also show how first-time room visits trigger room-specific descriptive text.

After moving into a room, I would demonstrate the suggestion system by selecting a suspect and weapon. The game then compares the guess to the hidden solution, explains which elements are wrong, and updates the notebook.

Then I would open the notebook to show how deductions are recorded automatically. Finally, once enough information is gathered, I would show the accusation system and end with either the winning case-closed story or the losing case-unsolved story.

**Suggested time:** 55 seconds

---

## Slide 8: Challenges Faced

**Suggested slide title:** `Challenges Faced`

**On-screen points:**

- Coordinating multiple game states
- Designing movement rules
- Handling partial suggestion feedback
- Preventing invalid input errors
- Keeping the command-line UI readable

**Speaker script:**

One of the main challenges in this project was coordinating multiple parts of the game state at the same time. The program has to track the hidden solution, the player’s current location, visited rooms, movement steps, notebook status, and whether the player has already ended the game through accusation or quitting.

Another challenge was implementing movement rules clearly. Because movement is dice-based and rooms are connected as a graph, I needed to handle adjacency, step consumption, secret passages, optional early stopping, and the restriction against revisiting rooms within a single turn.

Suggestion feedback also required careful logic. The game needs to compare three separate elements and then give partial feedback while updating only the appropriate notebook entries. That behavior had to stay consistent with both the deduction design and the user-facing text.

Finally, because this is a command-line project, a usability challenge was keeping the interface readable. I addressed that through repeated headers, clear menus, standardized prompts, and descriptive feedback messages.

**Suggested time:** 55 seconds

---

## Slide 9: Stability and Reliability

**Suggested slide title:** `Stability and Reliability`

**On-screen points:**

- Input validation
- Invalid choice handling
- Safe cancellation paths
- Automated testing
- Consistent rule enforcement

**Speaker script:**

Stability and reliability were important parts of the project. The game validates numeric input and yes-or-no input so that unexpected entries do not crash the program. Invalid menu choices, non-numeric values, and out-of-range values are all handled with error messages and safe retry behavior.

The game also supports cancellation in several places, such as suggestion and accusation selection, so the player can back out without breaking the game state.

To verify correctness, I used an automated test suite in `test_game.py`. In the current version, all 161 tests pass. These tests cover card data, mansion layout, movement rules, random solution validity, suggestion behavior, accusation win and loss paths, notebook operations, dice behavior, initialization, and input validation.

That testing helps support the claim that the gameplay logic is consistent and that the main rule systems behave as intended.

**Suggested time:** 55 seconds

---

## Slide 10: Conclusion

**Suggested slide title:** `Conclusion`

**On-screen points:**

- Functional Cluedo implementation
- Strong modular design
- Reliable turn-based logic
- Tested and documented
- Opportunities for future expansion

**Speaker script:**

In conclusion, this project successfully implements a complete command-line version of Cluedo with structured gameplay, deduction mechanics, modular design, and automated testing. The final program includes movement, room navigation, suggestions, accusations, notebook tracking, story text, and clear turn-based interaction.

From a programming perspective, the project demonstrates object-oriented design, separation of concerns, data modeling, input validation, and systematic testing. From a gameplay perspective, it recreates the investigation process in a way that is both functional and user friendly within a text-based environment.

If I continued developing the project, future improvements could include computer-controlled opponents, save and load functionality, a graphical user interface, richer replay control, and expanded analytics for player deduction history.

Thank you for watching this presentation.

**Suggested time:** 40 seconds

---

## Recording Notes for the Presenter

- Aim for a calm pace of about 120 to 140 spoken words per minute.
- Keep the total presentation between 8.5 and 10 minutes.
- If the recording runs long, shorten the challenges and conclusion sections first.
- Use the exact menu terms from the program to stay consistent with the live demo.
- If showing code during the presentation, focus on `game.py`, `mansion.py`, and `test_game.py`.
