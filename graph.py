from langgraph import StateGraph
from state import GameState
from node import load_game,investigation_hub

graph = StateGraph[GameState]()
graph.add_node("load_game", load_game)
graph.set_entrypoint("load_game")
graph.add_node("investigation_hub", investigation_hub)
graph.add_edge("load_game", "investigation_hub")