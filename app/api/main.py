from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage
from pydantic import BaseModel
import uvicorn
from app.graph.graph import graph

app = FastAPI(title="ShieldBase Assistant API")

# Add CORS to allow Next.js frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = "default"

class ChatResponse(BaseModel):
    reply: str | None = None
    state: dict | None = None
    quote_result: dict | None = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Setup configuration to inject session/thread ID for graph memory
    config = {"configurable": {"thread_id": request.session_id}}
    
    # We pass the input. Note our reducer appends messages automatically
    inputs = {
        "messages": [HumanMessage(content=request.message)],
        "last_user_message": request.message,
        "answer": "",
        "validation_errors": [],
        "quote_result": None
    }
    
    # Invoke the LangGraph graph
    result_state = graph.invoke(inputs, config=config)
    
    # Extract the response needed by the frontend from the state
    
    # Determine the response string based on what got populated or active mode
    reply = ""
    # If there are validation errors, we show them
    if result_state.get("validation_errors"):
        reply += "⚠️ " + "\n".join(result_state["validation_errors"]) + "\n\n"
    
    # Print the graph's generated answer if present
    if result_state.get("answer"):
        reply += result_state["answer"]
    
    # Return to Next.js
    return ChatResponse(
        reply=reply.strip() if reply else None,
        state={
            "active_mode": result_state.get("active_mode"),
            "insurance_type": result_state.get("insurance_type"),
            "quote_step": result_state.get("quote_step"),
            "collected_data": result_state.get("collected_data", {})
        },
        quote_result=result_state.get("quote_result")
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
