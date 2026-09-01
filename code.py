import os
import time
from typing import TypedDict, List
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END

# 1. Load configuration and API keys
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(current_dir, "api_key.env")
load_dotenv(dotenv_path=env_path, override=True)

api_keys = [
    os.path.expandvars(os.getenv("GOOGLE_API_KEY1", "")),
    os.path.expandvars(os.getenv("GOOGLE_API_KEY2", ""))
]
api_keys = [k for k in api_keys if k]

if not api_keys:
    raise ValueError("CRITICAL: No valid Gemini API keys found in api_key.env!")

# 2. Define the Shared Boardroom State for FinNova Capital
class BoardroomState(TypedDict):
    business_brief: str
    research_findings: str
    finance_recommendation: str
    credit_risk_recommendation: str
    compliance_recommendation: str
    marketing_recommendation: str
    ceo_decision: str
    debate_messages: List[str]
    review_cycle_count: int
    api_key_index: int

# Robust Multi-Key Failsafe Wrapper
def invoke_with_key_switching(state: BoardroomState, prompt: str) -> str:
    current_index = state.get("api_key_index", 0)
    attempts = 0
    
    while attempts < len(api_keys):
        active_key = api_keys[current_index]
        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.1-flash-lite", 
                temperature=0.4,
                api_key=active_key
            )
            response = llm.invoke(prompt)
            if hasattr(response, "content"):
                return response.content
            return str(response)
        except Exception as e:
            print(f"[Warning] API Key index {current_index} failed: {e}. Switching keys...")
            current_index = (current_index + 1) % len(api_keys)
            state["api_key_index"] = current_index
            attempts += 1
            time.sleep(1)
            
    return "API Failure: All available Gemini API keys exhausted."

# 3. Dynamic, Universal FinNova Capital Department Agents

def business_research_agent(state: BoardroomState):
    time.sleep(2) 
    prompt = f"""You are the Business Research Agent for FinNova Capital, an Indian digital lending company serving registered small businesses[cite: 4]. 
    Analyze the following scenario, brief, or problem description in detail, regardless of its format:
    
    "{state['business_brief']}"
    
    Instructions:
    - Extract and evaluate all market segments, customer types, demand figures, acquisition metrics, and contextual background provided in the text.
    - Identify core opportunities, structural bottlenecks, and operational challenges without focusing solely on short-term revenue[cite: 4]."""
    res = invoke_with_key_switching(state, prompt)
    return {"research_findings": res}

def finance_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the Finance and Treasury Agent for FinNova Capital. Review the Business Research findings: {state.get('research_findings', 'N/A')}. 
    
    Instructions:
    - Analyze all capital allocation limits, available funds, cost of funds, servicing/collection costs, setup budgets, and liquidity reserve requirements mentioned in the text.
    - Enforce strict unit economics and cost discipline across all proposals."""
    res = invoke_with_key_switching(state, prompt)
    return {"finance_recommendation": res}

def credit_risk_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the Credit Risk Agent for FinNova Capital. Review finance and research recommendations.
    
    Instructions:
    - Analyze expected credit losses, portfolio default thresholds, segment-specific default rates, fraud risks, and verification requirements specified in the scenario text.
    - Formulate underwriting rules and risk limits that keep defaults strictly at or below mandated ceilings[cite: 4]."""
    res = invoke_with_key_switching(state, prompt)
    return {"credit_risk_recommendation": res}

def compliance_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the Compliance and Customer Protection Agent for FinNova Capital. Review the lending plans and risk thresholds.
    
    Instructions:
    - Ensure fair customer treatment, transparent pricing disclosure, adherence to interest rate caps or regulatory constraints mentioned in the scenario, and strict protection against predatory terms[cite: 4].
    - Veto any approach that violates customer protection rules or legal bounds."""
    res = invoke_with_key_switching(state, prompt)
    return {"compliance_recommendation": res}

def marketing_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the Marketing and Sales Agent for FinNova Capital. Review financial and credit constraints.
    
    Instructions:
    - Evaluate acquisition channels, marketing budgets, cost per qualified application, conversion rates, and target volumes outlined in the scenario text[cite: 4].
    - Propose optimal go-to-market and channel allocation strategies that respect all constraints[cite: 4]."""
    res = invoke_with_key_switching(state, prompt)
    return {"marketing_recommendation": res}

def ceo_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CEO Agent for FinNova Capital. Synthesize all department inputs into a definitive executive decision addressing the core decision question in the text.
    
    Instructions:
    - Balance sustainable growth, affordability, expected credit losses, liquidity, operational capacity, fair customer treatment, and compliance[cite: 4].
    - Your final decision MUST explicitly specify: customer segment mix, product terms, approval policy, budget allocation, risk limits, go-to-market approach, implementation sequence, and measurable outcomes[cite: 4].
    
    Data Inputs:
    - Research: {state.get('research_findings')} 
    - Finance & Treasury: {state.get('finance_recommendation')} 
    - Credit Risk: {state.get('credit_risk_recommendation')} 
    - Compliance & Customer Protection: {state.get('compliance_recommendation')} 
    - Marketing & Sales: {state.get('marketing_recommendation')}"""
    res = invoke_with_key_switching(state, prompt)
    return {"ceo_decision": res}

# 4. Control Logic for the Boardroom Protocol
def check_debate_status(state: BoardroomState):
    cycle = state.get("review_cycle_count", 0)
    if cycle < 3:
        return "continue_debate"
    return "decide"

def increment_cycle(state: BoardroomState):
    current = state.get("review_cycle_count", 0)
    return {"review_cycle_count": current + 1}

# 5. Wire the Graph with Mandatory Lending Agents
workflow = StateGraph(BoardroomState)

workflow.add_node("Business_Research", business_research_agent)
workflow.add_node("Finance_Treasury", finance_agent)
workflow.add_node("Credit_Risk", credit_risk_agent)
workflow.add_node("Compliance_Protection", compliance_agent)
workflow.add_node("Marketing_Sales", marketing_agent)
workflow.add_node("Increment_Cycle", increment_cycle)
workflow.add_node("CEO", ceo_agent)

workflow.set_entry_point("Business_Research")
workflow.add_edge("Business_Research", "Finance_Treasury")
workflow.add_edge("Finance_Treasury", "Credit_Risk")
workflow.add_edge("Credit_Risk", "Compliance_Protection")
workflow.add_edge("Compliance_Protection", "Marketing_Sales")
workflow.add_edge("Marketing_Sales", "Increment_Cycle")

workflow.add_conditional_edges(
    "Increment_Cycle", 
    check_debate_status,
    {
        "continue_debate": "Finance_Treasury", 
        "decide": "CEO"               
    }
)

workflow.add_edge("CEO", END)
finnova_swarm = workflow.compile()

# 6. Dynamic Execution for Any Format/Scenario
if __name__ == "__main__":
    print("     FINNOVA CAPITAL BOARDROOM     ")
    
    print("\nPase any lending scenario, case study, or problem description below (press Enter, then Ctrl+Z / Ctrl+D and Enter when finished, or paste single block):")
    
    # Read multi-line or single-line input dynamically
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    user_brief = "\n".join(lines).strip()
    
    if not user_brief:
        user_brief = "Default Baseline: Launch small-business loan pilot with INR 30 crore, INR 60 lakh marketing budget, max 700 loans, cost of funds 10%, servicing cost 1.5%, max default 5%."

    initial_state = {
        "business_brief": user_brief,
        "debate_messages": [],
        "review_cycle_count": 0,
        "api_key_index": 0
    }
    
    print("\n[Swarm Initialized] Analyzing arbitrary case and running cross-department debate...")
    final_state = finnova_swarm.invoke(initial_state)
    
    print("               FINAL CEO DECISION                 ")
    
    decision_output = final_state["ceo_decision"]
    if isinstance(decision_output, list):
        for item in decision_output:
            if isinstance(item, dict) and 'text' in item:
                print(item['text'])
            else:
                print(item)
    else:
        print(decision_output)