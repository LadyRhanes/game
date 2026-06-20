from constant import characters,bestfriend_arc,unlock_rules,clues
from state import GameState

def build_system_prompt(character_name: str, state: dict) -> str:
    # find character data
    char = next(c for c in characters if c["name"] == character_name)
    
    # what has player revealed to this suspect
    revelations = state.get("player_revelations", {}).get(character_name, [])
    revelations_text = ", ".join(revelations) if revelations else "nothing yet"
    
    # how many times interrogated
    times = state.get("interrogation_counts", {}).get(character_name, 0)
        # pick personality based on state
    if character_name == "Daisy" and "bullying_records" in state.get("clues_found", []):
        personality = char.get("personality_confronted")
    else:
        personality = char.get("personality")
    
    # Jonas arc
    arc_text = ""
    if character_name == "Jonas":
        arc_stage = state.get("bestfriend_arc_stage", "calm")
        arc_text = f"\nYour current emotional state: {bestfriend_arc[arc_stage]}"
    
    prompt = f"""You are {char['name']} at a dinner party on a private island where the host has just been found dead.

Your secret: {char['secret']}
Your personality: {char['personality']}
You deflect questions about: {char['deflects_about']}
The detective has revealed to you: {revelations_text}
You have been interrogated {times} times before.
Stay in character. Never directly reveal your secret unless pushed very hard.
Respond naturally as a real person would, not like you're being interviewed.
Never monologue. Keep responses short and guarded. 
."""

    return prompt