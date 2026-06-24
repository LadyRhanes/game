from state import GameState
from constant import characters, unlock_rules,location_rules,clues
from prompt_builder import build_system_prompt
from prompt_builder import build_system_prompt
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import state

llm = ChatOllama(model="qwen2.5:7b")

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
        "current_suspect": "",
        "next_action": "",
        "current_location": "",


    }
def investigation_hub(state: GameState) -> GameState:
    available_suspects = state["unlocked_suspects"]
    available_locations = [
        loc for loc, rule in location_rules.items()
        if check_location_unlocked(loc, state)
    ]
    
    print("\n--- INVESTIGATION HUB ---")
    print(f"Suspects: {available_suspects}")
    print(f"Locations: {available_locations}")
    print("\nType a suspect name to interrogate or a location to examine.")
    
    choice = input("\nYour choice: ").strip()
    
    if choice in available_suspects:
        state["current_suspect"] = choice
        state["next_action"] = "interrogate"
    elif choice in available_locations:
        state["current_location"] = choice
        state["next_action"] = "examine"
    else:
        print("Invalid choice, try again.")
        state["next_action"] = "hub"  # loop back

       

    print("\nType a suspect name, location, or 'quit' to end the game.")
    choice = input("\nYour choice: ").strip()
    if choice.lower() == "quit":
        state["next_action"] = "end"

    
         
    
    return state

def interrogate_suspect( state: GameState) -> GameState:
    suspect_name = state["current_suspect"]
    if suspect_name not in state["unlocked_suspects"]:
        print(f"{suspect_name} is not available to talk to yet.")
        return state
    
    # get or create conversation history for this suspect
    if suspect_name not in state["conversation_histories"]:
        system_prompt = build_system_prompt(suspect_name, state)
        state["conversation_histories"][suspect_name] = [
            SystemMessage(content=system_prompt)
        ]
    
    conversation = state["conversation_histories"][suspect_name]
    
    # conversation loop
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "leave", "exit"]:
            break
        
        conversation.append(HumanMessage(content=user_input))
        response = llm.invoke(conversation)
        conversation.append(AIMessage(content=response.content))
        print(f"{suspect_name}: {response.content}\n")
    
    # save conversation history back to state
    state["conversation_histories"][suspect_name] = conversation
    
    # increment count after conversation ends
    state["interrogation_counts"][suspect_name] += 1
    
    return state


def examine_location(state: GameState) -> GameState:
    location = state.get("current_location", "")
    if not location:
        print("No location selected.")
        return state
    
    if location not in state["locations_visited"]:
        state["locations_visited"].append(location)
    
    # find if any clue is located here
    clue_found = None
    for clue_name, clue_data in clues.items():
        if clue_data["found_at"] == location:
            clue_found = clue_name
            break
    
    if clue_found and clue_found not in state["clues_found"]:
        state = process_clue_found(clue_found, state)
        print(f"\nYou find something: {clues[clue_found]['description']}")
    else:
        print(f"\nYou look around {location}... nothing new here.")
    
    return state
