from langgraph.graph import StateGraph,END
from state import GameState
from node import load_game, investigation_hub, interrogate_suspect,examine_location

graph = StateGraph(GameState)
graph.add_node("load_game", load_game)
graph.add_node("investigation_hub", investigation_hub)
graph.add_node("interrogate_suspect", interrogate_suspect)
graph.add_node("examine_location", examine_location)

graph.set_entry_point("load_game")
graph.add_edge("load_game", "investigation_hub")
def route_action(state: GameState) -> str:
    return state.get("next_action", "interrogate")

graph.add_conditional_edges(
    "investigation_hub",
    route_action,
    {
        "interrogate": "interrogate_suspect",
        "examine": "examine_location",
        "hub": "investigation_hub",
        "end": END
    }
)
graph.add_edge("interrogate_suspect", "investigation_hub")
graph.add_edge("examine_location", "investigation_hub")
# at the bottom of graph.py
app = graph.compile()

# run it
result = app.invoke({})