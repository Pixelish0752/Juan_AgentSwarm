# Team name : Juan
# Member(s) : Abhrodeep Ghosh (25BAI1616)
# Agentic Swarm: The AI Boardroom (Generic Pharma Engine)

## Solution Summary

This project implements a multi-agent management swarm built using **LangGraph** and powered by **Google Gemini** models (`gemini-3.1-flash-lite`). Designed for the Agentic Swarm challenge, the system simulates a virtual pharmaceutical corporate boardroom. Department agents independently analyze business briefs, cross-examine constraints, trigger mandatory disagreements, and feed structured evidence to a CEO Agent to produce a final, actionable corporate decision with measurable KPIs.

## Agent List

* **Business Research:** Analyzes patent cliffs, competitor pricing, and market timing.
* **Finance (CFO):** Evaluates sourcing costs, capital allocation, inventory buffers, and profit margin constraints.
* **Compliance / Risk Control:** Evaluates regulatory hurdles, bioequivalence risks, and quality control standards.


* **Marketing & Sales (CMO):** Defines go-to-market strategies, distribution channels, and commercial volume targets.
* **CEO Agent:** Resolves department conflicts, compares alternative strategies, weighs trade-offs, and issues the final decision memorandum along with measurable business KPIs.



## Workflow & Boardroom Protocol

The system executes a state-machine graph following the required 5-stage boardroom protocol:

1. **Analyse:** Department agents independently evaluate the incoming business scenario or surprise event.


2. **Share:** Findings and constraints are passed across the shared state.


3. **Challenge:** Agents push back against opposing department goals (e.g., Finance challenging high marketing spend).


4. **Compare:** The workflow cycles up to 3 times to evaluate alternative strategies.


5. **Decide:** The CEO agent synthesizes the trace into a final directive containing the chosen strategy, rejected alternatives, trade-offs, risks, and 3 business KPIs.



## Installation & Execution Instructions

### Prerequisites

* Python 3.10 or higher installed on your system.

### 1. Install Dependencies

Run the following command in your terminal to install the required packages:

```bash
pip install langgraph langchain langchain-google-genai python-dotenv

```

### 2. Configure API Keys

1. Create a file named `api_key.env` in the root project directory.
2. Populate it using your Gemini API keys based on the provided `.env.example` format:
```text
GOOGLE_API_KEY1="your_primary_gemini_api_key"
GOOGLE_API_KEY2="your_secondary_gemini_api_key"

```




### 3. Run the Application

Execute the python script:

```bash
code.py

```

When prompted, type or paste any custom pharmaceutical business scenario or surprise event to see the swarm analyze, debate, and render a final CEO decision.

## Models, Frameworks & External Services

* **Orchestration Framework:** LangGraph / LangChain


* **LLM Provider:** Google AI Studio (Gemini Developer API)


* **Core Model:** `gemini-3.1-flash-lite`

## Known Limitations & Failure-Handling Behavior

* **Rate Limits:** To prevent hitting free-tier rate limits during execution, intentional delays (`time.sleep`) are implemented between agent calls.
* **Key Switching / Fallbacks:** The system incorporates a multi-key fail-safe loop that automatically switches to a secondary API key if the primary key throws an exception. If all keys or API calls fail, hardcoded fallback responses ensure the CEO agent can still render a final decision without crashing the workflow.



## Declaration of Components

* Built natively using LangGraph state graph logic and Google Generative AI Python SDKs. All business rules, department instructions, and multi-key fallback mechanisms were custom-developed for this challenge.
