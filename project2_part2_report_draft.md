# Project 2 Part 2: Cluedo Game Report Draft

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
- The player’s current room

The room is fixed automatically based on the player’s location. After a suggestion, the game reports which elements are incorrect and updates the notebook accordingly. A correct suggestion confirms the theory as evidence, but it does not end the game.

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
- `player.py` defines the `Player` class, which tracks the detective’s location and visited rooms.
- `cards.py` stores static game data such as suspects, weapons, rooms, and canonical starting rooms.
- `notebook.py` defines the `Notebook` class for deduction tracking.
- `dice.py` defines the `DiceRoll` class used for movement.
- `story.py` stores the introduction, room descriptions, suggestion flavor text, and ending narratives.
- `test_game.py` contains the automated test suite.

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

#### `Game`

The `Game` class acts as the central controller. It:

- Builds the mansion
- Selects the hidden solution
- Places characters and weapons
- Creates the player object
- Initializes the notebook
- Runs the main menu loop
- Processes movement, suggestion, accusation, and quit actions

#### `Mansion` and `Room`

The `Mansion` class creates the room network, and each `Room` object stores its name and connected neighbors. This abstraction makes it easy to check legal movement and display room relationships.

#### `Player`

The `Player` class stores:

- Detective name
- Current room
- Set of visited rooms

This supports both display logic and movement restrictions.

#### `Notebook`

The `Notebook` class stores three status dictionaries:

- Suspect statuses
- Weapon statuses
- Room statuses

It also keeps a list of textual notes. This structure allows the game to record deduction progress efficiently.

#### `DiceRoll`

The `DiceRoll` class stores individual die values, the total, and the remaining movement budget. It also provides a display method for ASCII visualization.

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

### Screenshot Placeholders

- `[Insert Screenshot: Main Menu]`
- `[Insert Screenshot: Player Movement]`
- `[Insert Screenshot: Suggestion Feature]`
- `[Insert Screenshot: Accusation Feature]`
- `[Insert Screenshot: Winning Condition]`
- `[Insert Screenshot: Error Handling]`

### Test Case Table

| Test Area | Example Scenario | Expected Outcome | Actual Outcome |
|---|---|---|---|
| Card data | Load suspects and weapons | Correct counts and no duplicates | Passed |
| Mansion layout | Check Kitchen to Study passage | Passage exists and is bidirectional | Passed |
| Movement | Move from Hall to Study | Legal adjacent move succeeds | Passed |
| Movement | Move from Hall to Ballroom directly | Illegal move rejected | Passed |
| Suggestion | Wrong suspect with correct weapon | Feedback identifies suspect as wrong | Passed |
| Suggestion | Correct full suggestion | Notebook can confirm evidence, game continues | Passed |
| Accusation | Correct suspect, weapon, room | Game ends with win state | Passed |
| Accusation | Incorrect final accusation | Game ends with lose state | Passed |
| Notebook | Mark suspect as ruled out | Status updates to `X` | Passed |
| Input validation | Enter non-numeric menu input | Error message shown, no crash | Passed |

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
