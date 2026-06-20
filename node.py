from state import GameState
from constant import characters, unlock_rules,location_rules,clues
def check_location_unlocked(location: str, state: GameState) -> bool:
    rule = location_rules.get(location)
    if rule is None:
        return True
    
    if "interrogated" in rule:
        return state["interrogation_counts"].get(rule["interrogated"], 0) >= rule.get("min_times", 0)
    
    return False

def check_character_unlocked(character: str, state: GameState) -> bool:
    rule = unlock_rules.get(character)
    if rule is None:
        return True
    
    if "clue_found" in rule:
        return rule["clue_found"] in state["clues_found"]
    
    if "interrogated" in rule:
        suspect = rule["interrogated"]
        min_times = rule.get("min_times", 1)
        if state["interrogation_counts"].get(suspect, 0) < min_times:
            return False
        
        if "and" in rule:
            and_rule = rule["and"]
            and_suspect = and_rule["interrogated"]
            and_min = and_rule.get("min_times", 1)
            return state["interrogation_counts"].get(and_suspect, 0) >= and_min
        
        return True
    
    return False

def process_clue_found(clue_name: str, state: GameState) -> GameState:
    # add clue if not already found
    if clue_name not in state["clues_found"]:
        state["clues_found"].append(clue_name)
    
    # look up what this clue unlocks
    clue_data = clues.get(clue_name)
    if not clue_data:
        return state
    
    # unlock characters
    for char in clue_data["unlocks_characters"]:
        if char not in state["unlocked_suspects"]:
            state["unlocked_suspects"].append(char)
    
    # unlock locations (terrace)
    if "terrace" in clue_data["unlocks_locations"]:
        state["terrace_locked"] = False
    
    return state

def load_game(state: GameState) -> GameState:
    # build interrogation counts from characters list
    interrogation_counts = {char["name"]: 0 for char in characters if char["name"] != "host"}
    
    # build unlocked suspects from unlock_rules
    unlocked_suspects = [name for name, rule in unlock_rules.items() if rule is None]
    
    return {
        "clues_found": [],
        "locations_visited": [],
        "unlocked_suspects": unlocked_suspects,
        "interrogation_counts": interrogation_counts,
        "conversation_histories": {},
        "bestfriend_arc_stage": "calm",
        "terrace_locked": True,
        "ending_triggered": False,
        "player_revelations": {},
        "player_suspicions": {},

    }
def investigation_hub(state: GameState) -> GameState:
    available_suspects = state["unlocked_suspects"]
    available_locations = [
        loc for loc, rule in location_rules.items()
        if rule is None or check_location_unlocked(loc, state)
    ]
    
    # for now just print options, frontend will handle this later
    print("\n--- INVESTIGATION HUB ---")
    print(f"Suspects you can talk to: {available_suspects}")
    print(f"Locations you can visit: {available_locations}")
    
    return state