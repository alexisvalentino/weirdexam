# ShieldBase AI: Hybrid Insurance Sales & Support Assistant

ShieldBase is a production-grade, insurance-focused AI platform built with **Next.js** and **LangGraph**. It seamlessly orbits between a **Knowledge Assistant (RAG)** and a **Transactional Flow (Quotation)**, ensuring that user intent drives the experience without losing state.

---

## 🏗️ Architecture Overview

The system is split into two primary layers:

### 1. The Intelligence Core (Backend)
- **Framework:** FastAPI (Python 3.10+)
- **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph) manages the state machine and node routing.
- **RAG Engine:** Using `all-MiniLM-L6-v2` local embeddings stored in a **Chroma DB** vector store. It retrieves from the `kb/` folder (markdown files).
- **LLM:** Powered by OpenRouter (defaults to GPT-4o-mini / Claude-3-Haiku) for extraction and grounding.

### 2. The Experience Layer (Frontend)
- **Framework:** Next.js (App Router)
- **Styling:** Vanilla CSS & Tailwind (Blue/White Enterprise Aesthetic).
- **Messaging:** Supports streaming-like responses and dynamic **UI Components** (like QuoteCards) that render when the backend returns structured quote data.

---

## 📈 State Machine & Design Decisions

### The LangGraph Flow
The brain of the assistant uses a directed acyclic graph (DAG) structure defined in `app/graph/graph.py`.

1.  **Router Node:** Every user message is first classified. Is this a question? Is it a request to buy? Is it an answer to a pending question?
2.  **RAG Node (Conversational):** If the intent is "informational," the graph pulls context from the ShieldBase knowledge base and synthesizes a grounded answer.
3.  **Quotation Nodes (Transactional):** If the intent is "transactional," the graph moves through a deterministic sequence:
    - **Extraction:** LLM extracts specific values (e.g., "2022 Honda Civic") from natural language.
    - **Validation:** Internal logic checks if values meet business rules (e.g., driver must be >16).
    - **Persistence:** Collected data is stored in the `ChatState` via `MemorySaver`.

### Key Design Decisions
-   **Interruptible State:** If a user asks "Why do I need a $500 deductible?" *in the middle* of a quote flow, the graph identifies a "Context Switch." It calls the RAG node to answer the question, then uses the `interrupt_context` state to immediately prompt the user for the next quote variable, ensuring zero data loss.
-   **Deterministic Extraction:** Instead of letting the LLM "guess" the next step, we use `app/quote/schemas.py` as a single source of truth for required fields, ensuring the bot never forgets a mandatory question.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- An [OpenRouter API Key](https://openrouter.ai/)

### 1. Installation

From the project root, run the master installation script:
```bash
# Installs backend Python deps and frontend NPM packages
npm run install:all
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY=your_key_here
```

### 3. Running the Platform

You need to run both the backend and frontend simultaneously. We have provided combined commands for convenience:

**A. Start Backend (FastAPI)**
```bash
npm run dev:backend
```

**B. Start Frontend (Next.js)**
```bash
npm run dev:frontend
# or simply
npm run dev
```

Interact with it through localhost **`http://localhost:3000`**.

---

## 👤 User Walkthrough (End-to-End)

The ShieldBase experience is designed to feel like a conversation with an expert agent, not a web form:

1.  **Curiosity Phase:** A user asks: *"What does your auto insurance cover?"*. The bot retrieves the `kb/auto_insurance.md` and explains the tiers.
2.  **Intent Phase:** The user says: *"Sounds good, I'd like a quote for my car."*. The bot detects the `start_quote` intent and switches to Transactional mode.
3.  **The Pivot:** Midway through (after providing their name), the user asks: *"Wait, can I bundle this with home?"*. The bot explains bundling (RAG) and then immediately says: *"Back to your quote, what year is your vehicle?"*.
4.  **Completion:** Once all fields are validated, the bot generates a professional **Quote Card** in the chat UI with the estimated premium and an "Accept Quote" button.
5.  **Activation:** Clicking Accept moves the graph to the `quote_action_node`, finalizing the transaction in the session state.
