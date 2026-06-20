from typing import TypedDict

class GameState(TypedDict):
    clues_found: list[str]
    locations_visited: list[str]
    unlocked_suspects: list[str]
    interrogation_counts: dict[str, int]
    conversation_histories: dict[str, list]
    bestfriend_arc_stage: str
    terrace_locked: bool
    ending_triggered: bool
    player_revelations: dict[str, list[str]]
# example: {"bestfriend": ["found bullying records", "knows about the fight"]}
    player_suspicions: dict[str, int]  
# example: {"bestfriend": 3, "couple-husband": 1}
# suspicion score per suspect, builds as evidence accumulates