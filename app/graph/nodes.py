import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from app.graph.state import ChatState
from app.rag.retriever import get_retriever
from app.rag.prompts import QA_PROMPT
from app.quote.schemas import get_next_missing_field, get_field_prompt
from app.quote.validators import validate_collected_data
from app.quote.calculator import generate_quote

load_dotenv()

# We will use OpenRouter
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY", "dummy"),
    model="openai/gpt-4o-mini",
)

def router_node(state: ChatState) -> dict:
    """Smart routing logic that distinguishes between quote actions and information provision."""
    msg = state.get("last_user_message", "").lower()
    active_mode = state.get("active_mode")
    quote_step = state.get("quote_step")
    is_adjusting = state.get("is_adjusting")

    # 1. Higher priority: Global Actions (Detecting intent vs data)
    # If the message contains "adjust" but also a specific detail (e.g. "adjust age to 30"), 
    # we treat it as data entry (provide_field).
    has_value_indicator = any(char.isdigit() for char in msg) or len(msg.split()) > 5
    
    if "restart" in msg:
        return {"user_intent": "restart_quote"}
    if "accept" in msg or "confirm" in msg:
        return {"user_intent": "accept_quote"}
        
    if ("adjust" in msg or "change" in msg) and not has_value_indicator:
        return {"user_intent": "adjust_quote", "is_adjusting": True}

    # 2. Transactional Context
    if active_mode == "transactional":
        # If we are in adjustment mode or waiting for information
        if quote_step and quote_step != "completed":
             # Check for interruption (questions or explanations)
            if any(w in msg for w in ["what", "how", "why", "explain", "help", "who", "tell me"]):
                # Only mark as question if it's NOT likely a field value
                if not has_value_indicator:
                    return {"user_intent": "question", "interrupt_context": {"step": quote_step}}
            
            # Otherwise, assume they are providing the field
            return {"user_intent": "provide_field"}
        
        # If we completed the quote but then start typing (adjustment)
        if quote_step == "completed" or is_adjusting:
            return {"user_intent": "provide_field", "is_adjusting": True}

        # If we are in transactional mode but need insurance type
        if not state.get("insurance_type"):
            for t in ["auto", "car", "home", "house", "life"]:
                if t in msg:
                    t_mapped = "auto" if t in ["auto", "car"] else ("home" if t in ["home", "house"] else "life")
                    return {"user_intent": "start_quote", "insurance_type": t_mapped}

    # 3. Starting a Quote
    if any(k in msg for k in ["quote", "buy", "price", "get started", "insurance"]):
        # Detect type early
        for t in ["auto", "car", "home", "house", "life"]:
            if t in msg:
                t_mapped = "auto" if t in ["auto", "car"] else ("home" if t in ["home", "house"] else "life")
                return {"user_intent": "start_quote", "insurance_type": t_mapped}
        return {"user_intent": "start_quote", "insurance_type": None}

    # 4. Default to FAQ
    return {"user_intent": "question"}


def rag_node(state: ChatState) -> dict:
    """Retrieves documents and answers using LLM with full context window."""
    msg = state.get("last_user_message", "")
    retriever = get_retriever()
    docs = retriever.invoke(msg)
    
    context = "\n\n".join([d.page_content for d in docs])
    
    # Use chain with history
    chain = QA_PROMPT | llm
    history = state.get("messages", [])[:-1] # history excluding current user msg
    
    res = chain.invoke({
        "context": context, 
        "question": msg,
        "history": history
    })
    
    ans = res.content
    
    # If there was an interruption, remind them where they left off
    if state.get("interrupt_context"):
        prompt = get_field_prompt(state["insurance_type"], state["interrupt_context"]["step"])
        ans += f"\n\nReturning to your quote: {prompt}"
        return {
            "answer": ans, 
            "retrieved_docs": [d.page_content for d in docs], 
            "active_mode": "transactional",
            "interrupt_context": None # Clear it so it doesn't repeat
        }

    return {"answer": ans, "retrieved_docs": [d.page_content for d in docs], "messages": [res]}


def quote_entry_node(state: ChatState) -> dict:
    """Sets up the initial quote state concisely."""
    ins_type = state.get("insurance_type")
    collected = state.get("collected_data", {})
    
    if not ins_type:
        return {"answer": "I can help with that! Are you looking for auto, home, or life insurance?", "active_mode": "transactional"}
    
    next_field = get_next_missing_field(ins_type, collected)
    if next_field:
        prompt = get_field_prompt(ins_type, next_field)
        # Avoid repeating the intro if we've already started
        if len(collected) > 0:
            return {"active_mode": "transactional", "quote_step": next_field, "answer": prompt}
        return {"active_mode": "transactional", "quote_step": next_field, "answer": f"I can help with an {ins_type} quote! {prompt}"}
    
    return {"active_mode": "transactional"}


def quote_collection_node(state: ChatState) -> dict:
    """Extracts field value using LLM with context to avoid missing answers."""
    field = state.get("quote_step")
    ins_type = state.get("insurance_type")
    history = state.get("messages", [])
    is_adjusting = state.get("is_adjusting")
    
    # We use the previous messages to see if the user answered the question
    context_msgs = "\n".join([f"{m.type}: {m.content}" for m in history[-5:]])
    
    # Define which fields we are interested in
    from app.quote.schemas import PRODUCT_FIELDS
    available_fields = list(PRODUCT_FIELDS.get(ins_type, {}).keys())
    
    if is_adjusting or field == "completed":
        # If adjusting, we look for any of the fields in the product
        target_desc = f"any of these fields: {', '.join(available_fields)}"
    else:
        target_desc = f"the field: '{field}'"

    extract_prompt = f"""
    You are an AI data extractor for ShieldBase Insurance.
    Conversation context:
    {context_msgs}

    Target: {target_desc}
    
    Rules:
    - Return a JSON object with extracted fields.
    - Example: {{"vehicle_details": "2023 Tesla Model 3"}}
    - If NOT found, return {{}}.
    - DO NOT guess. DO NOT output conversational text.
    """
    
    import json
    res_raw = llm.invoke(extract_prompt).content.strip()
    
    try:
        # LLM might wrap in ```json
        if "```" in res_raw:
            res_raw = res_raw.split("```")[1]
            if res_raw.startswith("json"):
                res_raw = res_raw[4:]
        extracted_data = json.loads(res_raw)
    except:
        extracted_data = {}
    
    data = state.get("collected_data", {}).copy()
    if extracted_data:
        data.update(extracted_data)
    
    return {"collected_data": data}


def quote_validation_node(state: ChatState) -> dict:
    """Validates the latest collected input and provides feedback."""
    field = state.get("quote_step")
    ins_type = state.get("insurance_type")
    data = state.get("collected_data", {})
    
    # If in completion/adjustment, validate all required fields
    if field == "completed" or state.get("is_adjusting"):
        all_errors = []
        from app.quote.schemas import PRODUCT_FIELDS
        for f in PRODUCT_FIELDS.get(ins_type, {}).keys():
            val = data.get(f, "")
            errs = validate_collected_data(ins_type, f, val)
            if errs:
                all_errors.extend(errs)
        return {"validation_errors": all_errors}

    val = data.get(field, "")
    if not val:
        # If extraction failed, ask more clearly
        return {"validation_errors": [f"I didn't catch that. Could you please provide the {field.replace('_', ' ')}?"]}

    errors = validate_collected_data(ins_type, field, val)
    if errors:
        data.pop(field, None) # Clear invalid data
        prompt = get_field_prompt(ins_type, field)
        return {"validation_errors": errors, "collected_data": data, "answer": prompt}
        
    return {"validation_errors": []}


def quote_prompt_node(state: ChatState) -> dict:
    """Prompts for the next field."""
    ins_type = state.get("insurance_type")
    next_field = get_next_missing_field(ins_type, state.get("collected_data", {}))
    if next_field:
        prompt = get_field_prompt(ins_type, next_field)
        return {"quote_step": next_field, "answer": prompt}
    return {}


def quote_generation_node(state: ChatState) -> dict:
    """Calculates the final quote summary."""
    ins_type = state.get("insurance_type")
    data = state.get("collected_data", {})
    quote_res = generate_quote(ins_type, data)
    
    intro = {
        "auto": f"I've generated an instant quote for your {data.get('vehicle_details', 'vehicle')}:",
        "home": "I've generated an instant quote for your home:",
        "life": "I've generated an instant life insurance quote:"
    }.get(ins_type, "Here is your quote:")

    return {"quote_result": quote_res, "quote_step": "completed", "answer": intro, "is_adjusting": False}

def quote_action_node(state: ChatState) -> dict:
    """Handles final quote actions (accept/adjust/restart)."""
    intent = state.get("user_intent")
    
    if intent == "accept_quote":
        return {
            "answer": "Congratulations! Your quote has been accepted and your policy is now active. We've sent the details to your email. Thank you for choosing ShieldBase!",
            "active_mode": "general",
            "insurance_type": None,
            "quote_step": None,
            "collected_data": {},
            "quote_result": None
        }
    
    elif intent == "adjust_quote":
        return {
            "answer": "Sure! I can help you change your details. What would you like to update? (e.g., you can say 'change my vehicle to a 2024 Ford F-150')",
            "active_mode": "transactional",
            "is_adjusting": True
            # DO NOT clear collected_data
        }
        
    elif intent == "restart_quote":
        return {
            "answer": "Restarted. What type of insurance can I help you with today? (Auto, Home, or Life)",
            "active_mode": "transactional",
            "insurance_type": None,
            "quote_step": None,
            "collected_data": {},
            "quote_result": None,
            "is_adjusting": False
        }
    
    return {}
