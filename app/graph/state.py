from typing import TypedDict, Annotated, Union
import operator

class ChatState(TypedDict):
    # This state dictionary tracks everything traversing through the LangGraph nodes
    messages: Annotated[list, operator.add]
    last_user_message: str | None
    user_intent: str | None
    active_mode: str | None # "conversational" or "transactional"
    insurance_type: str | None # "auto", "home", or "life"
    quote_step: str | None
    collected_data: dict
    validation_errors: list[str]
    retrieved_docs: list[str]
    answer: str | None
    quote_result: dict | None
    interrupt_context: dict | None
