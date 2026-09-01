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

# Collect primary and secondary keys (assumes SECONDARY_API_KEY is also in your api_key.env)
api_keys = [
    os.path.expandvars(os.getenv("GOOGLE_API_KEY1", "")),
    os.path.expandvars(os.getenv("GOOGLE_API_KEY2", ""))
]
# Filter out empty keys
api_keys = [k for k in api_keys if k]

if not api_keys:
    raise ValueError("CRITICAL: No valid Gemini API keys found in api_key.env!")

# 3. Define the Shared Boardroom State (including compliance agent and key switcher index)
class BoardroomState(TypedDict):
    business_brief: str
    research_findings: str
    finance_recommendation: str
    compliance_recommendation: str
    marketing_recommendation: str
    ceo_decision: str
    debate_messages: List[str]
    review_cycle_count: int
    api_key_index: int

# Helper function to invoke LLM with automatic fallback switching between keys
def invoke_with_key_switching(state: BoardroomState, prompt: str) -> str:
    current_index = state.get("api_key_index", 0)
    attempts = 0
    
    while attempts < len(api_keys):
        active_key = api_keys[current_index]
        try:
            # Initialize model dynamically with the active key
            llm = ChatGoogleGenerativeAI(
                model="gemini-3.1-flash-lite", 
                temperature=0.4,
                api_key=active_key
            )
            response = llm.invoke(prompt)
            # Return text response safely
            if hasattr(response, "content"):
                return response.content
            return str(response)
        except Exception as e:
            print(f"[Warning] API Key index {current_index} failed with error: {e}. Switching keys...")
            current_index = (current_index + 1) % len(api_keys)
            state["api_key_index"] = current_index
            attempts += 1
            time.sleep(1)
            
    return "API Failure: All available Gemini API keys exhausted."

# 4. Define Agent Nodes using the Key-Switching Wrapper
def business_research_agent(state: BoardroomState):
    time.sleep(2) 
    prompt = f"You are the Head of Research for a generic pharma company. Analyze this brief: {state['business_brief']} Focus on patent cliffs, competitor pricing, and market timing."
    res = invoke_with_key_switching(state, prompt)
    return {"research_findings": res}

def finance_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CFO. Review Research findings: {state.get('research_findings', 'N/A')}. 
    You have a strict constraint: Sourcing costs and inventory stockpiles must not exceed standard margins. 
    If Marketing suggests an expensive strategy, you must explicitly REJECT it and demand a cheaper alternative."""
    res = invoke_with_key_switching(state, prompt)
    return {"finance_recommendation": res}

def compliance_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the Head of Compliance and Risk Control. Review research and financial plans. 
    Evaluate regulatory hurdles, bioequivalence risks, and quality control issues for this scenario: {state['business_brief']}."""
    res = invoke_with_key_switching(state, prompt)
    return {"compliance_recommendation": res}

def marketing_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CMO. Review Finance constraints: {state.get('finance_recommendation', 'N/A')}. 
    You believe dominating the generic market quickly is worth higher costs. 
    Recommend an AGGRESSIVE, fast-tracked go-to-market strategy, even if Finance opposes it."""
    res = invoke_with_key_switching(state, prompt)
    return {"marketing_recommendation": res}

def ceo_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CEO. Resolve the department debate, state the final decision clearly, 
    document at least one rejected alternative, explain trade-offs, and list 3 measurable business KPIs based on: 
    Research: {state.get('research_findings')} | Finance: {state.get('finance_recommendation')} | 
    Compliance: {state.get('compliance_recommendation')} | Marketing: {state.get('marketing_recommendation')}."""
    res = invoke_with_key_switching(state, prompt)
    return {"ceo_decision": res}

# 5. Control Logic for the Boardroom Protocol
def check_debate_status(state: BoardroomState):
    cycle = state.get("review_cycle_count", 0)
    if cycle < 3:
        return "continue_debate"
    return "decide"

def increment_cycle(state: BoardroomState):
    current = state.get("review_cycle_count", 0)
    return {"review_cycle_count": current + 1}

# 6. Wire the Graph (including Compliance Agent Node)[cite: 1]
workflow = StateGraph(BoardroomState)

workflow.add_node("Business_Research", business_research_agent)
workflow.add_node("Finance", finance_agent)
workflow.add_node("Compliance", compliance_agent)
workflow.add_node("Marketing", marketing_agent)
workflow.add_node("Increment_Cycle", increment_cycle)
workflow.add_node("CEO", ceo_agent)

workflow.set_entry_point("Business_Research")
workflow.add_edge("Business_Research", "Finance")
workflow.add_edge("Finance", "Compliance")
workflow.add_edge("Compliance", "Marketing")
workflow.add_edge("Marketing", "Increment_Cycle")

workflow.add_conditional_edges(
    "Increment_Cycle", 
    check_debate_status,
    {
        "continue_debate": "Finance", 
        "decide": "CEO"               
    }
)

workflow.add_edge("CEO", END)
pharma_swarm = workflow.compile()

# 7. Dynamic User Input Execution
if __name__ == "__main__":
    print("==================================================")
    print("  AGENTIC SWARM: PHARMA BOARDROOM ENGINE (FAILSAFE)")
    print("==================================================")
    
    user_brief = input("\nEnter your custom pharmaceutical business scenario or surprise event:\n> ")
    
    initial_state = {
        "business_brief": user_brief,
        "debate_messages": [],
        "review_cycle_count": 0,
        "api_key_index": 0
    }
    
    print("\n[Swarm Initialized] Running department analysis with multi-key fail-safe...")
    final_state = pharma_swarm.invoke(initial_state)
    
    print("\n==================================================")
    print("               FINAL CEO DECISION                 ")
    print("==================================================")
    
    decision_output = final_state["ceo_decision"]
    if isinstance(decision_output, list):
        for item in decision_output:
            if isinstance(item, dict) and 'text' in item:
                print(item['text'])
            else:
                print(item)
    else:
        print(decision_output)