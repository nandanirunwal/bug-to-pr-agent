from typing import TypedDict
from langgraph.graph import StateGraph, END

# State define karo — jo data poore graph mein flow karega
class MyState(TypedDict):
    message: str
    step: int

# Node A
def node_a(state: MyState) -> MyState:
    print("Node A chal raha hai...")
    return {"message": "Node A done!", "step": 1}

# Node B
def node_b(state: MyState) -> MyState:
    print("Node B chal raha hai...")
    return {"message": "Node B done!", "step": 2}

# Node C
def node_c(state: MyState) -> MyState:
    print("Node C chal raha hai...")
    return {"message": "Node C done!", "step": 3}

# Graph banao
graph = StateGraph(MyState)

# Nodes add karo
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_node("node_c", node_c)

# Edges add karo — flow define karo
graph.set_entry_point("node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", "node_c")
graph.add_edge("node_c", END)

# Graph compile karo
app = graph.compile()

# Graph chalao
print("Graph shuru ho raha hai...\n")
result = app.invoke({"message": "start", "step": 0})
print(f"\nFinal State: {result}")
