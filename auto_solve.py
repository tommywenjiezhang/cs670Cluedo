# auto_solve.py
# Plays one complete game of Cluedo using a real investigation strategy.
#
# Strategy:
#   1. Create a Game (Miss Scarlett, starts in Hall).
#   2. Visit all rooms in BFS order from Hall.
#   3. In each room make one Suggestion to gather clues:
#        - Cycle through suspects and weapons in turn order.
#        - Wrong elements are eliminated from the unknown set.
#        - Correct elements are skipped and tried again later.
#   4. Stop visiting rooms as soon as exactly one suspect, one weapon,
#      and one room remain -- those must be the solution.
#   5. Make the Accusation from wherever we currently stand.
#
# Each stdin read is echoed via EchoingInput so every decision is visible.
#
# Run with:  python auto_solve.py

import sys
import io
import story
story.FAST_MODE = True

from collections import deque
from game import Game
from cards import CHARACTERS, WEAPONS, ROOMS


# ---------------------------------------------------------------------------
# Echoing stdin wrapper
# ---------------------------------------------------------------------------

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

    def isatty(self):
        return False


# ---------------------------------------------------------------------------
# Graph helpers
# ---------------------------------------------------------------------------

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


def bfs_room_order(mansion, start):
    """All room names in BFS order from start (sorted neighbours for consistency)."""
    order = []
    seen = {start}
    q = deque([start])
    while q:
        room = q.popleft()
        order.append(room)
        for nb in sorted(mansion.get_room(room).get_connections()):
            if nb not in seen:
                seen.add(nb)
                q.append(nb)
    return order


# ---------------------------------------------------------------------------
# Movement helper
# ---------------------------------------------------------------------------

def add_movement(annotated, mansion, path):
    """Append (Move, exit-choice, stop) triples for each hop in path."""
    for i in range(1, len(path)):
        from_room = mansion.get_room(path[i - 1])
        dest = path[i]
        exits = from_room.get_connections()   # sorted list
        exit_idx = exits.index(dest) + 1
        annotated.append(("1", f"menu: Move (roll dice)"))
        annotated.append((str(exit_idx), f"exit #{exit_idx}: {dest}  (from {path[i-1]})"))
        annotated.append(("n", "stop after this hop"))


# ---------------------------------------------------------------------------
# Investigation planner
# ---------------------------------------------------------------------------

def compute_playthrough(g):
    """
    Build the full annotated input sequence for a real investigation.

    Visits rooms in BFS order.  Each room gets one Suggestion that cycles
    through unknowns: wrong elements are eliminated; correct ones are skipped
    so the next unknown in line gets tried.  Once exactly one suspect, weapon,
    and room remain, the Accusation is made.

    Returns: list of (value_str, label_str)
    """
    mansion = g.mansion
    sol     = g.solution    # used only to simulate suggestion feedback

    unkn_s = list(CHARACTERS)   # suspects not yet eliminated
    unkn_w = list(WEAPONS)      # weapons  not yet eliminated
    unkn_r = list(ROOMS)        # rooms    not yet eliminated

    # Pointers into the unknown lists -- advance past correct elements,
    # stay put when an element is removed (new item slides into same index).
    s_ptr = 0
    w_ptr = 0

    annotated = []
    current = g.player.get_location()

    for target in bfs_room_order(mansion, current):

        # ── Move to this room (may be multiple hops) ─────────────────
        if current != target:
            path = shortest_path(mansion, current, target)
            add_movement(annotated, mansion, path)
            current = target

        # ── Already solved before reaching this room? ─────────────────
        if len(unkn_s) == 1 and len(unkn_w) == 1 and len(unkn_r) == 1:
            break

        # ── Suggest: pick next untested suspect + weapon ───────────────
        suggest_s = unkn_s[s_ptr % len(unkn_s)]
        suggest_w = unkn_w[w_ptr % len(unkn_w)]

        char_idx   = CHARACTERS.index(suggest_s) + 1
        weapon_idx = WEAPONS.index(suggest_w)     + 1

        annotated.append(("2", "menu: Make a Suggestion"))
        annotated.append((str(char_idx),   f"suspect #{char_idx}: {suggest_s}"))
        annotated.append((str(weapon_idx), f"weapon  #{weapon_idx}: {suggest_w}"))

        # ── Simulate feedback (compare against hidden solution) ────────
        s_correct = (suggest_s == sol["character"])
        w_correct = (suggest_w == sol["weapon"])
        r_correct = (target    == sol["room"])

        if s_correct:
            s_ptr += 1              # correct -- skip it, try next position
        else:
            unkn_s.remove(suggest_s)    # wrong -- eliminated

        if w_correct:
            w_ptr += 1
        else:
            unkn_w.remove(suggest_w)

        if not r_correct and target in unkn_r:
            unkn_r.remove(target)

        # ── View notebook after each suggestion (shows progress) ──────
        annotated.append(("4", "menu: View Detective's Notebook"))

        # ── Check whether solution is now uniquely determined ──────────
        if len(unkn_s) == 1 and len(unkn_w) == 1 and len(unkn_r) == 1:
            break

    # ── Final Accusation ──────────────────────────────────────────────
    final_s = unkn_s[0]
    final_w = unkn_w[0]
    final_r = unkn_r[0]

    char_idx   = CHARACTERS.index(final_s) + 1
    weapon_idx = WEAPONS.index(final_w)     + 1
    room_idx   = ROOMS.index(final_r)       + 1

    annotated.append(("3", "menu: Make an Accusation"))
    annotated.append(("y", "confirm the accusation"))
    annotated.append((str(char_idx),   f"suspect #{char_idx}: {final_s}"))
    annotated.append((str(weapon_idx), f"weapon  #{weapon_idx}: {final_w}"))
    annotated.append((str(room_idx),   f"room    #{room_idx}: {final_r}"))

    return annotated


# ---------------------------------------------------------------------------
# Simulation preview  (does NOT look at the solution for routing)
# ---------------------------------------------------------------------------

def preview_investigation(g):
    """
    Print what the solver plans to do room-by-room without spoiling the
    accusation in advance.  Shows rooms visited and suspects/weapons tried.
    """
    mansion = g.mansion
    sol     = g.solution

    unkn_s = list(CHARACTERS)
    unkn_w = list(WEAPONS)
    unkn_r = list(ROOMS)
    s_ptr  = 0
    w_ptr  = 0

    current = g.player.get_location()
    visit_order = bfs_room_order(mansion, current)
    steps = []

    for idx, target in enumerate(visit_order, 1):
        if len(unkn_s) == 1 and len(unkn_w) == 1 and len(unkn_r) == 1:
            break

        suggest_s = unkn_s[s_ptr % len(unkn_s)]
        suggest_w = unkn_w[w_ptr % len(unkn_w)]

        s_correct = (suggest_s == sol["character"])
        w_correct = (suggest_w == sol["weapon"])
        r_correct = (target    == sol["room"])

        eliminated = []
        if not s_correct:
            unkn_s.remove(suggest_s)
            eliminated.append(f"suspect '{suggest_s}'")
        else:
            s_ptr += 1
        if not w_correct:
            unkn_w.remove(suggest_w)
            eliminated.append(f"weapon '{suggest_w}'")
        else:
            w_ptr += 1
        if not r_correct and target in unkn_r:
            unkn_r.remove(target)
            eliminated.append(f"room '{target}'")

        elim_str  = (", ".join(eliminated)) if eliminated else "-- no new eliminations --"
        steps.append((idx, target, suggest_s, suggest_w, elim_str,
                      len(unkn_s), len(unkn_w), len(unkn_r)))

    return steps, unkn_s[0], unkn_w[0], unkn_r[0]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    SEP  = "=" * 62
    DASH = "-" * 62

    # Create game; suppress the room-description printed in __init__
    buf = io.StringIO(); sys.stdout = buf
    g = Game("Detective", "Miss Scarlett")
    sys.stdout = sys.__stdout__

    sol   = g.solution
    start = g.player.get_location()

    # ── Pre-game analysis ─────────────────────────────────────────────
    print(SEP)
    print("  AUTO-SOLVER  --  real investigation mode")
    print(SEP)
    print(f"  Starting room  : {start}")
    print(f"  BFS visit order: {' -> '.join(bfs_room_order(g.mansion, start))}")
    print(DASH)
    print("  Strategy")
    print("    Visit every room in BFS order from Hall.")
    print("    Each visit: suggest next untested suspect + weapon in that room.")
    print("    Wrong elements are marked [X] and removed from consideration.")
    print("    Correct elements are skipped; the pointer advances to try the next.")
    print("    Accuse as soon as only one suspect, weapon, and room remain.")
    print(DASH)

    steps, sol_s, sol_w, sol_r = preview_investigation(g)

    print("  Planned investigation  (rooms visited before accusation)")
    print(DASH)
    print(f"  {'#':<3}  {'Room':<16}  {'Suggested':<40}  Unknowns left")
    print(f"  {'-'*3}  {'-'*16}  {'-'*40}  {'-'*13}")
    for num, room, susp, weap, elim, rs, rw, rr in steps:
        combo = f"{susp} / {weap}"
        print(f"  {num:<3}  {room:<16}  {combo:<40}  {rs}s {rw}w {rr}r")
        print(f"       Eliminated: {elim}")
    print(DASH)
    print(f"  Accusation   : {sol_s} | {sol_w} | {sol_r}")
    print(SEP)
    print()

    # ── Build input sequence ──────────────────────────────────────────
    annotated = compute_playthrough(g)

    print(SEP)
    print("  LIVE GAME OUTPUT")
    print(SEP)
    print()

    sys.stdin = EchoingInput(annotated)
    g.run()
    sys.stdin = sys.__stdin__

    print()
    print(SEP)
    print("  AUTO-SOLVER  --  investigation complete")
    print(f"  True solution  : {sol['character']} | {sol['weapon']} | {sol['room']}")
    print(SEP)


if __name__ == "__main__":
    main()
