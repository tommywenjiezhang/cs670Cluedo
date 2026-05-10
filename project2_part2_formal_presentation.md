# Project 2 Part 2 Formal Presentation: Cluedo Game

## Slide 1: Title

- **Cluedo Digital Edition**
- Project 2 Part 2
- Python command-line implementation
- Investigation, deduction, and final accusation gameplay

**Speaker Notes:**  
This presentation introduces my Project 2 Part 2 Cluedo game. The project recreates the Cluedo experience as a Python command-line application in which the player explores Blackwell Manor, gathers clues through suggestions, tracks evidence, and makes one final accusation to solve the case.

**Demo Cue:**  
State at the beginning that the program is launched from the terminal with `python main.py`.

## Slide 2: Project Overview and Objectives

- Recreate the core mechanics of Cluedo
- Practice object-oriented and modular program design
- Model turn flow, deduction rules, and end-game logic
- Build a reliable text-based interactive system
- Verify behavior with automated tests

**Speaker Notes:**  
The project had both gameplay and software engineering goals. From the player perspective, the system needed to support movement, suggestions, notebook tracking, and accusation-based resolution. From the implementation perspective, it needed to demonstrate modular organization, clear state management, input validation, and a testable control flow.

## Slide 3: Game Rules and Player Experience

- Player enters a detective name and chooses a suspect identity
- The chosen suspect determines the starting room
- Each turn offers a menu of actions
- Movement uses two six-sided dice and room adjacency
- Suggestions test **suspect + weapon** in the current room
- Accusation tests **suspect + weapon + room** and ends the game

**Speaker Notes:**  
When the game starts, the player is guided through a short setup process. After entering a detective name, the player chooses one of the six suspects, such as Miss Scarlett or Professor Plum. That choice determines the starting room, because the code stores a canonical starting location for each suspect. During play, the user interacts through a repeated menu loop that supports movement, deduction, notebook review, room descriptions, the mansion map, and the final accusation workflow.

## Slide 4: Key Features

- Character-based starting positions
- Dice-based movement with step budgeting
- Nine-room mansion with secret passages
- Detective notebook with automatic clue marking
- Story text, room descriptions, and ASCII display output
- Separate suggestion and accusation systems

**Speaker Notes:**  
The game includes several features that make it more complete than a minimal rule prototype. The player has a suspect identity, a starting room, a movement system based on two dice, and a notebook that records ruled-out or confirmed information. The game also includes narrative text, ASCII-style presentation, and secret passages that add strategic movement options.

## Slide 5: System Architecture and Code Structure

- `main.py`: starts the program, prints the intro, reads setup input, and creates the `Game`
- `game.py`: contains the `Game` class and the main gameplay loop
- `mansion.py`: defines `Room` and `Mansion` for the room graph and ASCII map
- `player.py`: stores the detective name, current room, and visited rooms
- `cards.py`: stores suspects, weapons, rooms, starting-room data, `Character`, and `Weapon`
- `notebook.py`, `dice.py`, and `story.py`: handle clue tracking, dice behavior, and narrative/output text
- `test_game.py`: verifies data integrity, rules, and input-handling behavior

**Speaker Notes:**  
The project is organized into focused Python modules rather than one large file. `main.py` is responsible for startup and player setup, while `game.py` acts as the central controller. The board is represented through `Room` and `Mansion`, player state is stored in `Player`, and card-related constants live in `cards.py`. Supporting files isolate dice output, notebook behavior, and story text so the core game loop can remain readable.

## Slide 6: Implementation Details

- Main language: **Python**, using the standard library only
- `Game.__init__()` builds the mansion, selects a random solution, places characters and weapons, and creates the player
- Hidden solution is stored as a dictionary with `character`, `weapon`, and `room`
- `Mansion.rooms` stores room objects; each `Room` keeps connected neighbors
- `Player` stores `name`, `current_room`, and a `visited_rooms` set
- `Notebook` stores suspect, weapon, and room status dictionaries plus notes

**Speaker Notes:**  
The central implementation is the `Game` class in `game.py`. During initialization, it builds the `Mansion`, generates the hidden solution with random choices, creates character and weapon objects, and then places the player in the canonical starting room for the selected suspect. The room network is represented as connected `Room` objects, while the player's investigation state is stored through the `Player`, `Notebook`, and the `Game` fields such as `turn`, `solved`, and `won`.

## Slide 7: Turn Processing and Game Logic

- `Game.run()` repeatedly displays the current location and action menu
- Menu input dispatches to movement, suggestion, accusation, notebook, map, or quit logic
- `_move()` rolls a `DiceRoll`, tracks remaining steps, and prevents same-turn revisits
- Suggestions compare the chosen suspect and weapon plus current room against the solution
- Accusations require confirmation and then check all three solution elements exactly
- `solved` and `won` flags determine whether the game continues or ends

**Speaker Notes:**  
This part of the system is controlled by the main game loop. The loop accepts a menu choice, validates it at the branch level, and then calls the corresponding method. Movement uses `DiceRoll.roll()` and consumes steps one room at a time, while secret passages are handled as a separate branch. Suggestions update the notebook but do not end the game. By contrast, accusations are the only win or lose path, because the code explicitly sets `self.solved` and `self.won` only inside the accusation logic or the quit path.

## Slide 8: Design Choices

- Modular files separate setup, rules, data, display, and testing
- Classes are used for `Game`, `Mansion`, `Room`, `Player`, `Notebook`, `Character`, `Weapon`, and `DiceRoll`
- Lists preserve menu order for suspects, weapons, and rooms
- Dictionaries support fast lookups for starting rooms, notebook status, descriptions, and solution fields
- The room layout is modeled as a graph through connected room objects
- Helper methods isolate validation and output behavior to improve maintainability

**Speaker Notes:**  
These design choices were made to keep the code readable and reliable. Classes group related state and behavior, which makes the game easier to reason about than a purely procedural implementation. Lists are useful for ordered menu display, while dictionaries simplify quick lookup of room descriptions, clue status, and starting locations. The graph-like mansion representation also makes legal movement and map display easier to implement cleanly.

## Slide 9: Demo Walkthrough with Technical Notes

1. Launch the game
   - Viewer sees: introductory story text and the ASCII title banner.
   - Code detail: `main.py` calls `dramatic_print(INTRO_TEXT)` and then prints `ASCII_BANNER` from `story.py`.
2. Enter detective name
   - Viewer sees: a prompt asking for the detective name.
   - Code detail: `main.py` reads the input, strips whitespace, and falls back to `"Detective"` if the entry is empty.
3. Choose a suspect identity
   - Viewer sees: six suspects, each with a starting room and intro text.
   - Code detail: `main.py` loops through `CHARACTERS`, uses `CHARACTER_STARTING_ROOMS`, and validates the choice through `_pick_int()`.
4. Start the investigation
   - Viewer sees: the starting room and its description.
   - Code detail: `Game.__init__()` builds the initial state, creates the `Player`, and immediately prints the starting room description from `ROOM_DESCRIPTIONS`.
5. Show the main menu
   - Viewer sees: current location, exits, and options 1 through 9.
   - Code detail: `Game.run()` calls `player.show_location()` and prints the action menu before dispatching the next choice.
6. Demonstrate movement
   - Viewer sees: ASCII dice, remaining steps, connected rooms, and optional stopping.
   - Code detail: `_move()` uses `DiceRoll.roll()`, decrements steps with `use_step()`, and tracks `visited_this_turn` to prevent loops.
7. Demonstrate room description or map
   - Viewer sees: either a room description or an ASCII mansion map with the current room highlighted.
   - Code detail: `_show_room_description()` reads `ROOM_DESCRIPTIONS`, while `Mansion.display_map()` renders the floor plan.
8. Demonstrate a suggestion
   - Viewer sees: suspect and weapon selection, then clue feedback.
   - Code detail: `_make_suggestion()` fixes the room to `player.get_location()`, compares the guess against `self.solution`, and updates `Notebook`.
9. Show notebook updates
   - Viewer sees: suspects, weapons, rooms, and any stored notes.
   - Code detail: `Notebook.display()` prints status dictionaries using `?`, `X`, and `!` markers.
10. Demonstrate accusation and ending
   - Viewer sees: confirmation prompt, final accusation input, and win or loss story text.
   - Code detail: `_make_accusation()` validates confirmation, checks all three fields, prints `WIN_TEXT` or `LOSE_TEXT`, and sets `solved` and `won`.

**Speaker Notes:**  
The demo should explain not only what appears on screen but also which code path is responsible for that behavior. This is useful in a formal presentation because it shows that the visible gameplay is backed by a clear internal structure rather than by isolated print statements. The audience can connect the user experience directly to startup logic, state initialization, the main menu loop, and the game-rule methods.

**Demo Cue:**  
Keep the demo moving. Pause only briefly after notebook updates, dice output, and the final accusation result.

## Slide 10: Testing and Validation

- Automated test suite is implemented in `test_game.py`
- Card data tests verify suspects, weapons, rooms, and starting-room mappings
- Mansion tests verify adjacency, bidirectional connections, and secret passages
- Player tests verify starting state, legal movement, and room-visit tracking
- Suggestion and accusation tests verify correct logic, cancellation, and win/loss outcomes
- Input tests verify invalid menu choices, non-numeric entries, and out-of-range values
- Current verified result: **161/161 tests passed**

**Speaker Notes:**  
The testing strategy checks both structure and behavior. The suite verifies that the data definitions are correct, that the mansion layout is connected as expected, and that the player can move only through legal paths. It also tests random solution validity, suggestion feedback, accusation success and failure, notebook updates, dice behavior, initialization, and invalid input handling. In addition, the test file sets `story.FAST_MODE = True` so the dramatic typewriter output does not slow the automated runs.

## Slide 11: Challenges and Reliability

- Coordinating hidden solution state, player location, notebook state, and end conditions
- Designing movement with dice, step limits, secret passages, and no same-turn backtracking
- Giving partial suggestion feedback while updating the correct notebook entries
- Preventing invalid user input from breaking the game
- Maintaining readable terminal output during repeated turns

**Speaker Notes:**  
One challenge was that several parts of the state must stay synchronized at all times. The solution, player position, notebook, movement steps, and game-ending flags all affect one another. Another challenge was balancing user interaction with robustness, because command-line games can fail easily if input validation is weak. The helper methods for reading integers and yes-or-no responses, along with the modular class structure, were important for keeping the implementation stable.

## Slide 12: Conclusion and Timing

- Functional command-line implementation of Cluedo
- Strong alignment between gameplay behavior and code structure
- Architecture and implementation can be explained within a 10-minute recording
- Automated testing supports reliability claims
- Future work could include AI opponents, save/load support, or a GUI

**Speaker Notes:**  
In conclusion, this project successfully combines game design and software engineering in a single Python application. The final system is not only playable from the user perspective, but also clearly structured from the implementation perspective. For presentation timing, the introduction and rules should take about two minutes, architecture and implementation about two to three minutes, the demo about three minutes, and the final testing and conclusion section about two minutes.
