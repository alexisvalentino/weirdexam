from langgraph.graph import StateGraph, START, END
from app.graph.state import ChatState
from app.graph.nodes import (
    router_node,
    rag_node,
    quote_entry_node,
    quote_collection_node,
    quote_validation_node,
    quote_prompt_node,
    quote_generation_node,
    quote_action_node
)
from app.quote.schemas import get_next_missing_field, get_field_prompt
from langgraph.checkpoint.memory import MemorySaver

def route_from_router(state: ChatState):
    intent = state.get("user_intent")
    if intent == "start_quote":
        return "quote_entry_node"
    elif intent in ["accept_quote", "adjust_quote", "restart_quote"]:
        return "quote_action_node"
    elif intent == "provide_field":
        return "quote_collection_node"
    else:
        return "rag_node"

def route_after_validation(state: ChatState):
    if state.get("validation_errors"):
        return END # quote_validation_node sets the answer prompt
    
    ins_type = state.get("insurance_type")
    next_field = get_next_missing_field(ins_type, state.get("collected_data", {}))
    
    if next_field:
        return "quote_prompt_node" 
    else:
        return "quote_generation_node"

def build_graph():
    builder = StateGraph(ChatState)
    
    builder.add_node("router_node", router_node)
    builder.add_node("rag_node", rag_node)
    builder.add_node("quote_entry_node", quote_entry_node)
    builder.add_node("quote_collection_node", quote_collection_node)
    builder.add_node("quote_validation_node", quote_validation_node)
    builder.add_node("quote_prompt_node", quote_prompt_node)
    builder.add_node("quote_generation_node", quote_generation_node)
    builder.add_node("quote_action_node", quote_action_node)
    
    builder.add_edge(START, "router_node")
    
    # Conditional edge from router
    builder.add_conditional_edges("router_node", route_from_router)
    
    # RAG node finishes turn
    builder.add_edge("rag_node", END)
    
    # Quote Actions
    builder.add_edge("quote_action_node", END) # End turn after accepting/adjusting/restarting
    
    # Quote Entry
    builder.add_edge("quote_entry_node", END) # Pauses for user if questions needed
    
    # Collection -> Validation
    builder.add_edge("quote_collection_node", "quote_validation_node")
    
    builder.add_conditional_edges("quote_validation_node", route_after_validation, {
        END: END,
        "quote_prompt_node": "quote_prompt_node",
        "quote_generation_node": "quote_generation_node"
    })
    
    builder.add_edge("quote_prompt_node", END)
    builder.add_edge("quote_generation_node", END)
    
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph

# Ensure graph is exported
graph = build_graph()
