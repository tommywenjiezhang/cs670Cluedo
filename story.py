# story.py
# All flavour text: story intro, win/lose endings, room descriptions,
# character intros, suggestion feedback, and the dramatic_print helper.

import sys
import time

# Set to True in tests to skip the typewriter delay.
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


ASCII_BANNER = """
  ============================================================
  ||                                                        ||
  ||         C  L  U  E  D  O                               ||
  ||         Digital Edition  --  Blackwell Manor           ||
  ||                                                        ||
  ||      A murder. Six suspects. One accusation.           ||
  ||                                                        ||
  ============================================================
"""

INTRO_TEXT = (
    "\nIt is a stormy October evening at Blackwell Manor.\n"
    "Lord Blackwell has been found dead in his study --\n"
    "the doors locked, the guests still inside.\n"
    "\n"
    "Scotland Yard is delayed by the weather.\n"
    "You must solve this yourself.\n"
    "\n"
    "Six suspects. Six weapons. Nine rooms.\n"
    "One of them is a murderer -- and they are still in the house.\n"
    "\n"
    "You have your instincts, your notebook, and ONE final accusation.\n"
    "Use it wisely.\n"
    "\n"
    "Good luck, Detective.\n"
)

WIN_TEXT = (
    "\nYou step forward and speak in a clear voice.\n"
    "The room falls silent. Every suspect turns to look at you.\n"
    "\n"
    "You name the murderer.\n"
    "You name the weapon.\n"
    "You name the room.\n"
    "\n"
    "A long pause...\n"
    "\n"
    "Then the colour drains from one face -- and they bolt for the door.\n"
    "They don't make it.\n"
    "\n"
    "Inspector Nettlefield arrives the next morning to collect them.\n"
    "Your name will appear in the papers.\n"
    "\n"
    "  * * *  CASE CLOSED  * * *\n"
)

LOSE_TEXT = (
    "\nThe words leave your mouth before doubt can stop them.\n"
    "\n"
    "You are wrong.\n"
    "\n"
    "The real killer smiles quietly from across the room.\n"
    "By morning they are gone -- a carriage in the night,\n"
    "a burned letter, a missing passport.\n"
    "\n"
    "The case goes cold.\n"
    "Scotland Yard blames the fog.\n"
    "\n"
    "You know better.\n"
    "\n"
    "  * * *  CASE UNSOLVED  * * *\n"
)

ROOM_DESCRIPTIONS = {
    "Kitchen": (
        "The smell of burnt copper mingles with old grease. "
        "A carving knife is wedged into the cutting board as if someone left in a hurry. "
        "The clock on the wall stopped at 11:45."
    ),
    "Ballroom": (
        "Crystal chandeliers hang dark and still. "
        "A champagne glass lies shattered near the grand piano, "
        "and a single muddy footprint crosses the parquet floor."
    ),
    "Conservatory": (
        "Tropical plants press against the glass walls; the air is thick and damp. "
        "Something rustles behind the ferns. "
        "The garden door is locked from the inside."
    ),
    "Dining Room": (
        "A long mahogany table set for twelve with only one chair overturned. "
        "The candles are melted to stubs. "
        "A dinner bell lies on the floor as if it rolled from someone's hand."
    ),
    "Billiard Room": (
        "Green baize stretched across three tables, one cue missing from the rack. "
        "A cigar still burns in the ashtray. "
        "Whoever was here left less than five minutes ago."
    ),
    "Library": (
        "Floor-to-ceiling shelves surround you, one bookcase slightly ajar. "
        "A leather journal lies open on the desk, its last entry torn out. "
        "The ink is still wet on the blotter."
    ),
    "Lounge": (
        "Deep leather armchairs face a fireplace full of cold ash. "
        "The drinks cabinet is open and one glass is missing. "
        "A draft from somewhere unnamed stirs the velvet curtains."
    ),
    "Hall": (
        "The entrance hall echoes with every footstep. "
        "A grandfather clock marks the seconds with grim precision. "
        "A monogrammed glove lies abandoned on the bottom stair."
    ),
    "Study": (
        "The victim's private study. Papers are strewn across the floor "
        "as if someone searched the room in desperation. "
        "The safe behind the portrait is open and empty."
    ),
}

CHARACTER_INTROS = {
    "Miss Scarlett":   "Charming and calculating. She knows everyone's secrets.",
    "Colonel Mustard": "A decorated soldier who prefers direct solutions.",
    "Mrs. White":      "The housekeeper. She sees everything and says very little.",
    "Mr. Green":       "Nervous and eager to please -- perhaps a little too eager.",
    "Mrs. Peacock":    "Aristocratic composure that never quite hides the steel underneath.",
    "Professor Plum":  "An academic who finds the puzzle of murder intellectually interesting.",
}

# Flavour text for suggestion feedback.
# Each string naturally contains the keyword the tests check for.
SUGGESTION_FLAVOUR = {
    "suspect": "That suspect was not in the vicinity. The witnesses are certain.",
    "weapon":  "That weapon bears no mark from the crime scene. Think again.",
    "room":    "The crime did not occur in that room. Search the manor further.",
    "all":     "Nothing aligns. Your theory collapses entirely. Start over.",
    "match":   "Everything aligns. Your pulse quickens -- you are very close to the truth.",
}
