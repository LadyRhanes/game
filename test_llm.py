from prompt_builder import build_system_prompt
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="qwen2.5:7b")

# mock state for testing
state = {
    "player_revelations": {},
    "interrogation_counts": {"Nick": 0},
    "clues_found": []
}

# build Daisy's system prompt dynamically
system = SystemMessage(content=build_system_prompt("Daisy", state))

conversation = [system]

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    
    conversation.append(HumanMessage(content=user_input))
    response = llm.invoke(conversation)
    conversation.append(AIMessage(content=response.content))
    print(f"Daisy  : {response.content}\n")