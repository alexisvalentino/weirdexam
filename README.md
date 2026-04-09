# ShieldBase AI: Hybrid Insurance Sales & Support Assistant

ShieldBase is a production-grade, insurance-focused AI platform built with **Next.js** and **LangGraph**. It seamlessly orbits between a **Knowledge Assistant (RAG)** and a **Transactional Flow (Quotation)**, ensuring that user intent drives the experience without losing state.

---

## 🛠️ Project Architecture

The system follows a modern decoupled architecture designed for stateful AI interactions:

### 1. Intelligence Core (Backend)
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+) for high-performance, asynchronous API endpoints.
- **Orchestration:** [LangGraph](https://github.com/langchain-ai/langgraph) manages the complex state machine, allowing the bot to pivot between conversational RAG and transactional quoting.
- **Persistence:** **Chroma DB** (Vector Database) stores enterprise knowledge for semantic retrieval.
- **LLM Connectivity:** Powered by **OpenRouter** (integrating GPT-4o-mini), providing state-of-the-art natural language understanding and data extraction.

### 2. Experience Layer (Frontend)
- **Framework:** [Next.js 14](https://nextjs.org/) (App Router) for a fast, SEO-optimized, and responsive user interface.
- **Styling:** Premium **Tailwind CSS** implementation using a curated blue-and-white enterprise aesthetic.
- **Dynamic UI:** Interactive components like **Quote Cards** are rendered based on structured JSON responses from the backend, providing a seamless "form-within-a-chat" experience.

---

## 🧠 AI Logic & Implementation

### 1. Conversation Memory (State)
ShieldBase "remembers" every interaction using LangGraph's native `MemorySaver`.
- **Persistent Sessions:** Every interaction is tracked via a `thread_id`. The AI remembers your name and vehicle details even if you pause to ask a random question.
- **State Schema (`ChatState`):** Defined in `app/graph/state.py`, this structured object tracks:
    - `messages`: A full history of Human and AI messages.
    - `collected_data`: A dictionary for validated insurance inputs.
    - `active_mode`: Tracks if the user is in "conversational" or "transactional" mode.
    - `interrupt_context`: Saves the exact step in a quote flow during user interruptions.

### 2. Hallucination Prevention & Accuracy
We implement several rigorous "guardrails" to ensure ShieldBase remains a reliable insurance expert:
- **Strict Grounding:** The `RAG_SYSTEM_PROMPT` explicitly instructs the LLM to only answer based on retrieved context. If the answer isn't found, it must state: *"I do not have that information."*
- **Deterministic Extraction:** Instead of letting the LLM "chat" about data, we use specialized **Extraction Nodes** (`quote_collection_node`) that strictly parse user text for specific fields, returning `NONE` if no data is found.
- **Low Temperature:** The LLM is configured with a low temperature (approaching 0.0) for extraction and routing nodes, ensuring deterministic and repeatable logic.
- **Rule-Based Validation:** Input data (zip codes, ages, emails) is verified by Python logic in `app/quote/validators.py`, decoupling business rules from LLM unpredictability.
- **K-Search Constraint:** Retrieval is limited to the top 3 (`k=3`) most relevant chunks to maintain high context precision and ignore "noise."

### 3. Knowledge Base & RAG Implementation
- **Source Material:** Enterprise knowledge is stored in the `/kb` directory as Markdown files.
- **Embeddings:** Local inference using `all-MiniLM-L6-v2` (via HuggingFace), ensuring fast and private document indexing.
- **Processing:** Documents are split into semantic chunks using `RecursiveCharacterTextSplitter` (`chunk_size=500`, `chunk_overlap=50`) to maintain meaning across splits.
- **Vector Search:** Chroma DB handles similarity search, allowing the assistant to find "coverage details" or "claims processes" in milliseconds.

### 4. Graph Logic (The Brain)
The AI logic is defined as a directed graph in `app/graph/graph.py`:
- **Router Node:** Classifies intent using keywords and LLM semantics.
- **RAG Node:** Fetches knowledge chunks and synthesizes a grounded response.
- **Transactional Nodes:** A sequence of `Entry` -> `Collection` -> `Validation` -> `Prompt` -> `Generation` that handles the insurance quoting lifecycle.

---

## 🔄 End-to-End User Interaction Flow

### Phase 1: Knowledge Discovery (RAG)
1.  **User Input:** *"What car insurance coverage do you offer?"*
2.  **Routing:** The **Router Node** detects a "question" intent.
3.  **Retrieval:** The **RAG Node** queries Chroma DB, finds `kb/auto_insurance.md`.
4.  **Generation:** The LLM synthesizes an answer using *only* the retrieved text.
5.  **Output:** The user receives a clear explanation of Liability vs. Comprehensive coverage.

### Phase 2: Transactional Entry (The "Pivot")
1.  **User Input:** *"Sounds good, I'd like a quote for my Tesla."*
2.  **Routing:** The **Router** detects `start_quote` and sets `insurance_type="auto"`.
3.  **Initialization:** The **Quote Entry Node** marks the session as `transactional`.

### Phase 3: Conversational Data Collection
1.  **AI Question:** *"What year is your vehicle?"*
2.  **User Input:** *"It's a 2022 Model 3."*
3.  **Extraction:** The **Collection Node** uses the LLM to extract `{"vehicle_year": "2022", "vehicle_model": "Model 3"}`.
4.  **Validation:** The **Validation Node** confirms the year is not in the future.
5.  **Iteration:** The flow repeats (asking for zip code, driver age, etc.) until the **Insurance Schema** is satisfied.

### Phase 4: Finalization
1.  **Calculation:** The **Generation Node** processes the final premium using deterministic formulas in `app/quote/calculator.py`.
2.  **Presentation:** The backend returns a `quote_result` object.
3.  **UI Rendering:** The Next.js frontend detects the `quote_result` and renders a high-fidelity **Quote Card** with "Accept" and "Adjust" buttons.
4.  **Completion:** If the user clicks "Accept", the **Action Node** clears the transactional state and finalizes the policy in the session history.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- [OpenRouter API Key](https://openrouter.ai/)

### Setup & Run
1.  **Install All:** `npm run install:all`
2.  **Configure Env:** Create a `.env` in the root with `OPENROUTER_API_KEY=your_key`
3.  **Start Backend:** `npm run dev:backend`
4.  **Start Frontend:** `npm run dev`

Visit **[http://localhost:3000](http://localhost:3000)** to experience the hybrid insurance assistant.

