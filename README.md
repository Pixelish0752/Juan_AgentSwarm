# Team Name: Juan 
# Member(s) : Abhrodeep Ghosh(25BAI1616)
# FinNova Capital:  FinSwarm

## Solution Summary

This project implements a multi-agent digital lending boardroom built using **LangGraph** and powered by **Google Gemini** models (`gemini-3.1-flash-lite`). Tailored for FinNova Capital, a fictional Indian digital lending company serving registered small businesses, the system simulates a specialized executive management swarm. Department agents analyze arbitrary lending test cases and scenarios, cross-examine risk and financial constraints, and feed structured evidence to a CEO Agent to produce a compliant, risk-adjusted lending strategy with measurable outcomes.

## Required Agent Swarm

* **Business Research Agent:** Extracts and evaluates market segments, customer types, demand figures, and acquisition metrics from any test case format.
* **Finance and Treasury Agent:** Analyzes capital allocation limits, available funds, cost of funds, servicing costs, setup budgets, and liquidity reserve requirements.
* **Credit Risk Agent:** Evaluates expected credit losses, portfolio default thresholds, segment-specific default rates, fraud risks, and verification requirements.
* **Compliance and Customer Protection Agent:** Ensures fair customer treatment, transparent pricing disclosure, adherence to interest rate caps or regulatory constraints, and protection against predatory terms.
* **Marketing and Sales Agent:** Evaluates acquisition channels, marketing budgets, cost per qualified application, conversion rates, and target volumes.
* **CEO Agent:** Synthesizes department inputs to balance sustainable growth, affordability, credit losses, liquidity, and compliance, outputting a definitive executive decision memorandum.



## Workflow & Boardroom Protocol

The system executes a state-machine graph following the required 5-stage boardroom protocol:

1. **Analyse:** Department agents independently evaluate the provided lending scenario or test case.


2. **Share:** Findings, risk parameters, and financial constraints are passed across the shared state.


3. **Challenge:** Agents push back against opposing department goals (e.g., Credit Risk challenging aggressive marketing expansion).


4. **Compare:** The workflow cycles up to 3 times to evaluate alternative portfolio strategies.


5. **Decide:** The CEO agent synthesizes the trace into a final directive specifying customer segment mix, product terms, approval policies, budget allocations, risk limits, go-to-market approaches, implementation sequences, and measurable outcomes.



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
2. Populate it using your Gemini API keys based on the required format:
```text
GOOGLE_API_KEY1="your_primary_gemini_api_key"
GOOGLE_API_KEY2="your_secondary_gemini_api_key"

```




### 3. Run the Application

Execute the python script:

```bash
python code.py

```

When prompted, paste any lending test case text or scenario description. Press `Enter` then `Ctrl+Z` (Windows) or `Ctrl+D` (Mac/Linux) and `Enter` to submit multi-line text and trigger the swarm.

## Models, Frameworks & External Services

* **Orchestration Framework:** LangGraph / LangChain


* **LLM Provider:** Google AI Studio (Gemini Developer API)


* **Core Model:** `gemini-3.1-flash-lite`

## Known Limitations & Failure-Handling Behavior

* **Rate Limits:** To prevent hitting free-tier rate limits during execution, intentional delays (`time.sleep`) are implemented between agent calls.
* **Key Switching / Fallbacks:** The system incorporates a multi-key fail-safe loop that automatically switches to a secondary API key if the primary key throws an exception. If all keys or API calls fail, fallback responses ensure the CEO agent can still render a final decision without crashing the workflow.



## Declaration of Components

* Built natively using LangGraph state graph logic and Google Generative AI Python SDKs. All lending business rules, department instructions, and multi-key fallback mechanisms were custom-developed for this challenge.