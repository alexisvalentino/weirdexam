from app.graph.state import ChatState
from app.rag.retriever import get_retriever
from app.rag.prompts import QA_PROMPT
from app.quote.schemas import get_next_missing_field, get_field_prompt
from app.quote.validators import validate_collected_data
from app.quote.calculator import generate_quote
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

# We will use OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "dummy"),
    model="openai/gpt-4o-mini", # fallback default, can use Claude
)

def router_node(state: ChatState) -> dict:
    """Basic routing logic based on user input intent."""
    msg = state.get("last_user_message", "").lower()
    
    # If currently in a transaction and answering a field
    if state.get("active_mode") == "transactional":
        # Check for explicit actions FIRST before assuming they are answering a prompt
        if "accept" in msg or "confirm" in msg:
            return {"user_intent": "accept_quote"}
        if "adjust" in msg or "change" in msg:
            return {"user_intent": "adjust_quote"}
        if "restart" in msg:
            return {"user_intent": "restart_quote"}

        # If we're waiting for a specific field and it's NOT completed
        if state.get("quote_step") not in [None, "completed"]:
             # Check if they want to interrupt
            if "what" in msg or "how" in msg or "why" in msg or "explain" in msg:
                return {"user_intent": "question", "interrupt_context": {"step": state["quote_step"]}}
            return {"user_intent": "provide_field"}
        
        # If we are in transactional mode but haven't picked a type yet, check if msg has one
        if not state.get("insurance_type"):
            if "auto" in msg or "car" in msg:
                return {"user_intent": "start_quote", "insurance_type": "auto"}
            elif "home" in msg or "house" in msg:
                return {"user_intent": "start_quote", "insurance_type": "home"}
            elif "life" in msg:
                return {"user_intent": "start_quote", "insurance_type": "life"}

    # Basic intent matching for starting a new quote
    if "quote" in msg or "buy" in msg or "price" in msg:
        if "auto" in msg or "car" in msg:
            return {"user_intent": "start_quote", "insurance_type": "auto"}
        elif "home" in msg or "house" in msg:
            return {"user_intent": "start_quote", "insurance_type": "home"}
        elif "life" in msg:
            return {"user_intent": "start_quote", "insurance_type": "life"}
        return {"user_intent": "start_quote", "insurance_type": None}
    
    if "accept" in msg or "confirm" in msg:
        return {"user_intent": "accept_quote"}
    
    if "adjust" in msg or "change" in msg:
        return {"user_intent": "adjust_quote"}
    
    if "restart" in msg:
        return {"user_intent": "restart_quote"}

    # Default to question
    return {"user_intent": "question"}


def rag_node(state: ChatState) -> dict:
    """Retrieves documents and answers using LLM."""
    msg = state.get("last_user_message", "")
    retriever = get_retriever()
    docs = retriever.invoke(msg)
    
    context = "\n\n".join([d.page_content for d in docs])
    
    chain = QA_PROMPT | llm
    res = chain.invoke({"context": context, "question": msg})
    
    ans = res.content
    
    # If there was an interruption, remind them where they left off
    if state.get("interrupt_context"):
        ans += "\n\nLet's get back to your quote. " + get_field_prompt(state["insurance_type"], state["interrupt_context"]["step"])
        return {"answer": ans, "retrieved_docs": [d.page_content for d in docs], "active_mode": "transactional"}

    return {"answer": ans, "retrieved_docs": [d.page_content for d in docs]}


def quote_entry_node(state: ChatState) -> dict:
    """Sets up the initial quote state."""
    ins_type = state.get("insurance_type")
    if not ins_type:
        return {"answer": "I can help with that! Are you looking for auto, home, or life insurance?", "active_mode": "transactional"}
    
    next_field = get_next_missing_field(ins_type, state.get("collected_data", {}))
    if next_field:
        prompt = get_field_prompt(ins_type, next_field)
        return {"active_mode": "transactional", "quote_step": next_field, "answer": f"I can help with an {ins_type} quote! {prompt}"}
    
    return {"active_mode": "transactional"}


def quote_collection_node(state: ChatState) -> dict:
    """Extracts field value using LLM and saves it."""
    field = state.get("quote_step")
    ins_type = state.get("insurance_type")
    msg = state.get("last_user_message", "")
    
    # Simple extraction using LLM for robustness
    extract_prompt = f"Given the user said '{msg}', extract the exact real-world information provided for the requested field '{field}'. DO NOT return JSON or lists. Just return the extracted string (e.g. '2022 Honda Civic' or 'Single-family Home, $300k'). If the user provides irrelevant text, return nothing."
    res = llm.invoke(extract_prompt).content.strip()
    
    data = state.get("collected_data", {})
    data[field] = res
    
    return {"collected_data": data}


def quote_validation_node(state: ChatState) -> dict:
    """Validates the latest collected input."""
    field = state.get("quote_step")
    ins_type = state.get("insurance_type")
    data = state.get("collected_data", {})
    val = data.get(field, "")
    
    errors = validate_collected_data(ins_type, field, val)
    if errors:
        # Clear invalid data
        data.pop(field, None)
        # Remind them what field to provide
        prompt = get_field_prompt(ins_type, field)
        return {"validation_errors": errors, "collected_data": data, "answer": prompt}
        
    return {"validation_errors": []}


def quote_prompt_node(state: ChatState) -> dict:
    """Prompts the user for the next required field."""
    ins_type = state.get("insurance_type")
    next_field = get_next_missing_field(ins_type, state.get("collected_data", {}))
    if next_field:
        prompt = get_field_prompt(ins_type, next_field)
        return {"quote_step": next_field, "answer": prompt}
    return {}


def quote_generation_node(state: ChatState) -> dict:
    """Calculates the final quote."""
    ins_type = state.get("insurance_type")
    data = state.get("collected_data", {})
    quote_res = generate_quote(ins_type, data)
    
    if ins_type == "auto":
        vehicle = data.get("vehicle_details", "vehicle").title()
        ans = f"Great! I've generated an instant quote for your {vehicle}:"
    elif ins_type == "home":
        ans = "Great! I've generated an instant quote for your home:"
    else:
        ans = "Great! I've generated an instant life insurance quote based on your details:"

    return {"quote_result": quote_res, "quote_step": "completed", "answer": ans}

def quote_action_node(state: ChatState) -> dict:
    """Handles accept, adjust, and restart intents for active quotes."""
    intent = state.get("user_intent")
    
    if intent == "accept_quote":
        return {
            "answer": "Congratulations! Your quote has been accepted. Your policy is now active, and we will email your official documents to you shortly. Thank you for choosing ShieldBase!",
            "active_mode": "general",
            "insurance_type": None,
            "quote_step": None,
            "collected_data": {},
            "quote_result": None
        }
    
    elif intent == "adjust_quote":
        ins_type = state.get("insurance_type", "auto")
        return {
            "answer": "No problem. Let's adjust your details. What would you like to change?",
            "active_mode": "transactional",
            "quote_step": list(state.get("collected_data", {}).keys())[0] if state.get("collected_data") else None,
            "collected_data": {} # Reset collected data for a fresh adjustment
        }
        
    elif intent == "restart_quote":
        return {
            "answer": "Quote restarted. Are you looking for auto, home, or life insurance?",
            "active_mode": "transactional",
            "insurance_type": None,
            "quote_step": None,
            "collected_data": {},
            "quote_result": None
        }
    
    return {}
