# ShieldBase Insurance Quotation Assistant
## Solution Requirements Document

**Prepared for:** Software Engineer Take-Home Assessment  
**Project Type:** LangGraph Hybrid Chatbot  
**Frontend:** Next.js  
**Document Version:** 1.0  

---

## 1. Purpose

This document defines the solution requirements for the **ShieldBase Insurance Quotation Assistant**, a hybrid AI chatbot that combines:

1. **Conversational support** through retrieval-augmented generation (RAG), where users can ask general questions about insurance products.
2. **Transactional quotation workflows**, where users can request a personalized quote for auto, home, or life insurance through a guided step-by-step process.

The goal of this solution is to demonstrate a clean and practical implementation of a **LangGraph-based state machine** that can route between conversational and transactional flows, handle user intent changes mid-conversation, validate structured inputs, and generate a simple quote response.

This is not intended to be a production-grade insurance platform. The solution should instead emphasize clarity of architecture, explicit state transitions, reliable structured flow handling, and a coherent user experience.

---

## 2. Project Objective

The system shall provide an AI assistant for a fictional insurance company called **ShieldBase Insurance**.

The assistant shall support two core interaction modes:

### 2.1 Conversational Mode
The chatbot shall answer general questions about ShieldBase insurance products using a small internal knowledge base. Responses must be grounded in retrieved content and must avoid making unsupported claims.

Example use cases:
- What types of insurance do you offer?
- What does your auto policy cover?
- Do you cover pre-existing conditions on life insurance?
- What is the difference between comprehensive and third-party auto coverage?

### 2.2 Transactional Mode
The chatbot shall guide a user through a structured insurance quotation workflow. The assistant must:
- identify the insurance product the user wants a quote for
- collect the required customer details
- validate user input
- calculate a basic quote
- present the quote
- allow the user to confirm, adjust details, or restart

Supported product lines:
- Auto insurance
- Home insurance
- Life insurance

---

## 3. Product Vision

The proposed solution is a **hybrid insurance assistant** that feels like a single chat experience, while internally separating free-form conversation from structured transaction handling.

The design should make the following clear:
- free-form insurance Q&A and quote workflows are different interaction modes
- LangGraph is used as the orchestrator because the conversation is stateful
- state transitions are explicit and explainable
- structured data collection should be deterministic where possible
- side questions during a quote flow should not break the process or lose collected inputs

---

## 4. Core Requirements

## 4.1 Functional Requirements

### FR-1: LangGraph State Machine Orchestrator
The system shall use **LangGraph** as the central orchestration framework.

The graph must:
- route user messages based on detected intent
- support both conversational and transactional flows
- preserve state between turns
- support interruption and resumption
- clearly define state transitions

### FR-2: Intent Detection
The system shall determine whether the user intent is one of the following:
- asking an insurance-related question
- requesting a quote
- adjusting a quote
- confirming a quote
- restarting a workflow
- unclear or unsupported input

Intent detection should be lightweight, explainable, and sufficient to route the user into the correct node in the graph.

### FR-3: RAG-Powered Conversational Responses
The system shall support grounded answers using a small insurance knowledge base.

The conversational flow must:
- retrieve relevant documents or chunks from the knowledge base
- pass the retrieved context to the language model
- answer naturally but only from grounded context
- return a fallback response when the answer is not found in the retrieved material

### FR-4: Transactional Quote Workflow
The system shall support quote generation for:
- auto insurance
- home insurance
- life insurance

The quote flow must follow this progression:
1. Identify insurance type
2. Collect required customer details
3. Validate inputs
4. Generate quote
5. Present quote
6. Confirm, adjust, or restart

### FR-5: Product-Specific Data Collection
The system shall collect different fields depending on the selected insurance type.

#### Auto Insurance
Required fields:
- vehicle year
- vehicle make
- vehicle model
- driver age
- driving history
- desired coverage level

#### Home Insurance
Required fields:
- property type
- location
- estimated property value
- desired coverage level

#### Life Insurance
Required fields:
- applicant age
- health status
- desired coverage amount
- term length

### FR-6: Input Validation
The system shall validate user inputs at each relevant step.

Examples:
- vehicle year must not be in the future
- age must be a valid number in a reasonable range
- coverage amount must be greater than zero
- estimated property value must be numeric and positive
- term length must match allowed options

Validation should primarily be implemented through deterministic application logic rather than relying only on the language model.

### FR-7: Quote Generation
The system shall generate a simple quote based on collected inputs.

The quote formula may be basic or dummy, but must be:
- deterministic
- explainable
- product-specific
- easy to inspect during demo and review

Each quote response should include:
- insurance product type
- relevant summary of collected inputs
- estimated premium
- short explanation or notes
- next action options

### FR-8: Confirmation and Restart Handling
After presenting a quote, the system shall allow the user to:
- accept the quote
- adjust one or more details
- restart the flow for the same or a different product

### FR-9: Graceful Mid-Conversation Switching
The system shall support graceful transitions when a user changes intent during a quote flow.

Example:
- user starts an auto quote
- user asks, “What does comprehensive coverage include?”
- system answers using RAG
- system resumes the quote flow from the exact point it paused

The chatbot must not lose already collected transaction data when such interruptions happen.

---

## 4.2 Bonus Requirements

These are not mandatory, but they improve the overall quality of the submission.

### BR-1: Low-Latency Experience
The system should minimize perceived waiting time through:
- efficient retrieval
- fast model selection
- minimal unnecessary graph steps
- frontend loading indicators and streaming if feasible

### BR-2: Polished Web Chat Interface
The system should provide a clean web-based chat experience with:
- message bubbles
- smooth scrolling
- loading indicators
- clear user and assistant distinction
- responsive layout

### BR-3: Embeddable Widget Readiness
If time allows, the frontend may be packaged or structured in a way that can later be embedded into another website using:
- iframe
- script tag
- widget shell component

This is optional and not required for the core submission.

---

## 5. Proposed Solution Architecture

## 5.1 High-Level Architecture

The solution will follow a client-server architecture:

### Frontend
- **Framework:** Next.js
- Responsible for chat interface, message rendering, user input, loading states, and API communication.

### Backend
- Responsible for LangGraph orchestration, intent routing, RAG retrieval, quote workflow handling, validation, and quote generation.

### Vector Retrieval Layer
- Responsible for indexing and retrieving knowledge base documents for conversational mode.

### Language Model Layer
- Used for natural language understanding, intent support, and conversational generation through an OpenRouter-compatible model.

---

## 5.2 Recommended Technology Stack

### Frontend
- Next.js
- React
- Tailwind CSS
- Optional streaming support for improved chat experience

### Backend
- Python
- FastAPI
- LangGraph
- LangChain-compatible utilities if needed

### LLM and Embeddings
- OpenRouter-compatible model provider
- Embeddings provider supported by the provided API budget

### Vector Store
- Chroma or another lightweight vector store suitable for a take-home assessment

### Knowledge Base Format
- Markdown files or text files stored within the repository

---

## 6. State Management Design

## 6.1 Graph Philosophy

The chatbot should behave like one assistant, but internally it must separate:
- conversational retrieval behavior
- structured transactional quote behavior

This separation is necessary because:
- conversational mode is flexible and retrieval-driven
- transactional mode requires strict sequencing and validation
- interruption handling must be explicit and recoverable

## 6.2 Proposed Shared State

A centralized graph state should be maintained across turns.

Suggested state fields:

```python
class ChatState(TypedDict):
    messages: list
    last_user_message: str
    user_intent: str
    active_mode: str
    insurance_type: str | None
    quote_step: str | None
    collected_data: dict
    validation_errors: list[str]
    retrieved_docs: list[str]
    answer: str | None
    quote_result: dict | None
    interrupt_context: dict | None
```

### State Field Definitions

- `messages`: conversation history used by the graph
- `last_user_message`: latest input from the user
- `user_intent`: detected route classification
- `active_mode`: current mode, conversational or transactional
- `insurance_type`: selected product type
- `quote_step`: current step or required field in quote collection
- `collected_data`: structured data gathered so far
- `validation_errors`: current validation feedback
- `retrieved_docs`: retrieved context used for RAG
- `answer`: generated assistant answer
- `quote_result`: generated quote object
- `interrupt_context`: saved transactional checkpoint during interruptions

---

## 7. LangGraph Node Design

The graph should remain simple, clear, and easy to explain during review.

## 7.1 Recommended Nodes

### 1. Router Node
Purpose:
- inspect latest user input
- determine the correct next path
- classify message as question, quote request, confirmation, adjustment, restart, or fallback

### 2. Conversational RAG Node
Purpose:
- retrieve relevant knowledge base chunks
- generate grounded answer
- return response to frontend
- optionally resume a paused quote flow

### 3. Quote Entry Node
Purpose:
- determine which insurance product the user wants
- ask for insurance type if missing

### 4. Quote Collection Node
Purpose:
- ask the next required field for the active product
- read user input and store extracted value

### 5. Quote Validation Node
Purpose:
- validate the current or updated collected inputs
- return errors if invalid
- continue if valid

### 6. Quote Generation Node
Purpose:
- calculate a quote from collected data
- build a structured quote result payload

### 7. Quote Confirmation Node
Purpose:
- present the quote
- ask whether the user wants to confirm, adjust, or restart

### 8. Resume Transaction Node
Purpose:
- return the user to the exact paused quote step after a conversational interruption

### 9. Fallback Node
Purpose:
- handle unclear, unsupported, or ambiguous user messages

---

## 8. Proposed State Transitions

A simple transition design is recommended.

```text
START
  ↓
Router
  ├── Conversational RAG
  ├── Quote Entry
  └── Fallback

Quote Entry
  ↓
Quote Collection
  ↓
Quote Validation
  ├── Invalid → Quote Collection
  └── Valid → Next Field or Quote Generation
  ↓
Quote Generation
  ↓
Quote Confirmation
  ├── Accept → END / Final Response
  ├── Adjust → Quote Collection
  └── Restart → Quote Entry

Interrupt Path:
Transactional Flow
  └── User asks product question
      → Conversational RAG
      → Resume Transaction
```

This design keeps the graph explicit and directly demonstrates the required boundary between free-form conversation and structured transaction handling.

---

## 9. Knowledge Base Requirements

The solution shall include a small fictional knowledge base inside the repository.

## 9.1 Target Size
The knowledge base should contain approximately **5 to 10 documents or text chunks**.

## 9.2 Required Topics
The knowledge base should cover:
- company overview
- available products
- auto insurance coverage details
- home insurance coverage details
- life insurance coverage details
- exclusions
- pricing tiers or coverage levels
- claims process
- deductibles
- cancellation policy
- bundling discounts
- general FAQs

## 9.3 Suggested File Structure

```text
kb/
  company_overview.md
  auto_insurance.md
  home_insurance.md
  life_insurance.md
  pricing_tiers.md
  claims_process.md
  faqs.md
  exclusions.md
  discounts.md
```

## 9.4 RAG Constraints
The conversational answer generator should:
- retrieve only a small number of top relevant chunks
- answer from retrieved context only
- explicitly say when information is unavailable in the knowledge base

This helps keep responses grounded and easier to explain.

---

## 10. Quotation Workflow Requirements

## 10.1 Auto Insurance Flow
The system shall:
1. identify that the quote is for auto insurance
2. collect vehicle year
3. collect vehicle make
4. collect vehicle model
5. collect driver age
6. collect driving history
7. collect desired coverage level
8. validate values
9. generate quote
10. present result and next actions

## 10.2 Home Insurance Flow
The system shall:
1. identify that the quote is for home insurance
2. collect property type
3. collect location
4. collect estimated property value
5. collect desired coverage level
6. validate values
7. generate quote
8. present result and next actions

## 10.3 Life Insurance Flow
The system shall:
1. identify that the quote is for life insurance
2. collect applicant age
3. collect health status
4. collect desired coverage amount
5. collect term length
6. validate values
7. generate quote
8. present result and next actions

---

## 11. Validation Requirements

Validation must be enforced at the application layer.

## 11.1 Example Rules

### Auto
- vehicle year must not exceed the current calendar year
- driver age must be a valid number in a defined range
- coverage level must match supported tiers
- driving history should match supported categories

### Home
- estimated property value must be numeric and greater than zero
- location must not be empty
- property type must match expected categories
- coverage level must match supported tiers

### Life
- age must be a valid number in a reasonable range
- coverage amount must be numeric and greater than zero
- term length must match allowed terms
- health status should be mapped to supported categories

## 11.2 Validation Response Behavior
When a validation error occurs, the system shall:
- explain which value is invalid
- ask for correction
- keep already valid fields intact
- not restart the entire quote flow unless the user asks to restart

---

## 12. Quote Calculation Requirements

The quote engine may use simple deterministic formulas.

## 12.1 Design Principles
The quote calculator should be:
- easy to implement
- transparent
- deterministic
- different per insurance product
- easy to explain during the interview

## 12.2 Example Pricing Logic

### Auto Insurance
Base premium may be adjusted using:
- driver age
- driving history
- vehicle recency
- coverage level

### Home Insurance
Base premium may be adjusted using:
- estimated property value
- property type
- location category
- coverage level

### Life Insurance
Base premium may be adjusted using:
- applicant age
- health status
- desired coverage amount
- term length

## 12.3 Quote Output Format
A generated quote should include:
- selected insurance product
- short summary of collected inputs
- estimated monthly or annual premium
- assumptions or notes
- user options to confirm, adjust, or restart

---

## 13. Frontend Requirements

## 13.1 Frontend Framework
The frontend shall be built using **Next.js**.

## 13.2 Chat Interface Features
The interface should include:
- assistant and user message bubbles
- auto-scroll to latest message
- loading state while waiting for backend response
- input box with send action
- responsive layout
- clear visual distinction between normal answers and quote progression prompts

## 13.3 UX Expectations
The frontend should make the system feel like a real chatbot product even if the backend logic is intentionally simple.

Recommended UX improvements:
- disable input while request is pending if needed
- show “typing” or loading indicator
- preserve chat history during the current session
- display quotes in a visually distinct card or highlighted block

---

## 14. API Requirements

The frontend will communicate with a backend API.

## 14.1 Minimum API Contract
At minimum, the backend should expose a chat endpoint such as:

```http
POST /api/chat
```

Example request:
```json
{
  "message": "I want an auto insurance quote",
  "session_id": "abc123"
}
```

Example response:
```json
{
  "reply": "Sure. What is the vehicle year?",
  "state": {
    "active_mode": "transactional",
    "insurance_type": "auto",
    "quote_step": "vehicle_year"
  }
}
```

## 14.2 Session Handling
The system should support per-session conversational continuity for the duration of the demo or active browser session.

Persistent long-term storage is optional and not required for this take-home.

---

## 15. Non-Functional Requirements

### NFR-1: Clarity
The solution must be easy to read, explain, and demo.

### NFR-2: Maintainability
The codebase should separate concerns clearly:
- graph orchestration
- retrieval logic
- quote logic
- validation
- frontend UI
- API layer

### NFR-3: Reliability
The system should not crash on normal unsupported or ambiguous input. It should always return a controlled response.

### NFR-4: Grounded Responses
Conversational answers should be based on retrieved documents rather than unsupported model invention.

### NFR-5: Fast Setup
The repository should be easy to run locally with clear installation instructions.

---

## 16. Recommended Repository Structure

```text
shieldbase-assistant/
  app/
    graph/
      state.py
      nodes.py
      routing.py
      graph.py
    rag/
      loader.py
      retriever.py
      prompts.py
    quote/
      schemas.py
      validators.py
      calculator.py
      flow.py
    api/
      main.py
      routes.py
  frontend/
    app/
    components/
    lib/
  kb/
    company_overview.md
    auto_insurance.md
    home_insurance.md
    life_insurance.md
    pricing_tiers.md
    claims_process.md
    faqs.md
    exclusions.md
    discounts.md
  tests/
    test_validators.py
    test_quote_calculator.py
    test_routing.py
  README.md
  requirements.txt
```

---

## 17. Testing Requirements

The solution should include at least basic validation of core behavior.

## 17.1 Priority Test Scenarios
Recommended scenarios:
1. user asks a pure insurance product question
2. user completes a full auto quote flow
3. user enters invalid data and corrects it
4. user switches to a product question mid-quote
5. user resumes the quote flow after interruption
6. user restarts with a different insurance product

## 17.2 Suggested Automated Tests
- validator tests
- quote calculation tests
- routing tests
- state transition tests where practical

---

## 18. Demo Readiness Requirements

The final solution should be easy to present in a follow-up interview.

The implementation should make it easy to explain:
- why LangGraph was chosen
- how the state machine is structured
- how RAG and transactional flows are separated
- how interruptions are handled without losing data
- how validation and quote generation work

Recommended demo scenarios:
- insurance FAQ question
- full quote flow
- invalid input correction
- mid-flow question interruption
- restart with another product

---

## 19. Implementation Priorities

To complete the assessment efficiently, development should follow this order:

### Phase 1
- scaffold backend and frontend
- define graph state
- sketch state transitions

### Phase 2
- create knowledge base documents
- implement retrieval pipeline
- implement conversational response path

### Phase 3
- build quote schemas and validation logic
- build quote calculator
- implement transactional flow

### Phase 4
- wire all nodes into LangGraph
- implement interruption and resume logic

### Phase 5
- build and polish Next.js chat interface

### Phase 6
- test core scenarios
- improve README
- prepare final demo walkthrough

---

## 20. Out of Scope

The following are not required for this submission unless time allows:
- production deployment
- real insurance pricing engine
- customer authentication
- database-backed customer records
- multi-user account system
- claims filing workflows
- policy issuance
- payment processing
- full admin dashboard
- advanced analytics

---

## 21. Final Solution Summary

The proposed solution is a **LangGraph-based hybrid insurance chatbot** with a **Next.js frontend** and a backend that cleanly separates two modes of interaction:

1. **Conversational RAG mode** for answering grounded product questions
2. **Transactional quote mode** for collecting structured information and generating quotes

The system is intentionally designed to highlight:
- clear state transitions
- strong separation between free-form and structured interactions
- deterministic validation
- simple, explainable quote generation
- graceful handling of intent switching mid-flow

This approach aligns with the goal of the assessment: demonstrating sound engineering judgment, practical LangGraph usage, and the ability to deliver a coherent solution quickly.
