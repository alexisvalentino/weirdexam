from app.graph.nodes import router_node
from app.graph.state import ChatState

def test_intent_start_quote():
    state: ChatState = {
        "messages": [], "last_user_message": "I want an auto quote",
        "user_intent": None, "active_mode": None, "insurance_type": None,
        "quote_step": None, "collected_data": {}, "validation_errors": [],
        "retrieved_docs": [], "answer": None, "quote_result": None, "interrupt_context": None
    }
    
    result = router_node(state)
    assert result["user_intent"] == "start_quote"
    assert result["insurance_type"] == "auto"

def test_intent_question():
    state: ChatState = {
        "messages": [], "last_user_message": "What does a comprehensive policy cover?",
        "user_intent": None, "active_mode": None, "insurance_type": None,
        "quote_step": None, "collected_data": {}, "validation_errors": [],
        "retrieved_docs": [], "answer": None, "quote_result": None, "interrupt_context": None
    }
    
    result = router_node(state)
    assert result["user_intent"] == "question"

def test_intent_interruption():
    state: ChatState = {
        "messages": [], "last_user_message": "Wait, what does liability mean?",
        "user_intent": None, "active_mode": "transactional", "insurance_type": "auto",
        "quote_step": "vehicle_year", "collected_data": {}, "validation_errors": [],
        "retrieved_docs": [], "answer": None, "quote_result": None, "interrupt_context": None
    }
    
    result = router_node(state)
    assert result["user_intent"] == "question"
    assert result["interrupt_context"]["step"] == "vehicle_year"

def test_intent_provide_field():
    state: ChatState = {
        "messages": [], "last_user_message": "I drive a 2018 Honda",
        "user_intent": None, "active_mode": "transactional", "insurance_type": "auto",
        "quote_step": "vehicle_model", "collected_data": {}, "validation_errors": [],
        "retrieved_docs": [], "answer": None, "quote_result": None, "interrupt_context": None
    }
    
    result = router_node(state)
    assert result["user_intent"] == "provide_field"
