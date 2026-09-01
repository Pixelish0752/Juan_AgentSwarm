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

# 2. Define the Shared Boardroom State
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

# 3. Granular, Morally Grounded Department Agents

def business_research_agent(state: BoardroomState):
    time.sleep(2) 
    prompt = f"""You are the Head of Business Research for a generic pharma and medical device company. 
    Analyze this brief: {state['business_brief']}
    
    Instructions:
    - Actively hunt for newer, better, and highly lucrative market opportunities (e.g., niche complex generics, specialized drug delivery mechanisms, or underserved medical device categories).
    - Analyze specific patent cliffs, API sourcing landscapes, and competitor vulnerabilities.
    - Think out-of-the-box regarding market gaps, but prioritize long-term asset value and public reliability."""
    res = invoke_with_key_switching(state, prompt)
    return {"research_findings": res}

def finance_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CFO. Review Research findings: {state.get('research_findings', 'N/A')}. 
    
    Instructions:
    - Obsess over keeping expenditure, CAPEX, working capital, and unit COGS aggressively low.
    - Do NOT impede the company's growth or compromise the medical product's core efficacy.
    - Conduct tight cost-benefit evaluations of specific medicine formulations or device manufacturing lines.
    - If Marketing suggests an expensive, high-risk strategy, aggressively challenge and push back with hard economic metrics."""
    res = invoke_with_key_switching(state, prompt)
    return {"finance_recommendation": res}

def compliance_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the Head of Compliance, Quality Control, and Regulatory Affairs. Review research and financial plans.
    
    Instructions:
    - Maintain a strict, uncompromising stance on regulatory hurdles (e.g., FDA/CDSCO filings, ANDA approvals), bioequivalence risks, impurity profiles, and medical device ISO quality standards.
    - Ensure patient safety and product integrity take absolute precedence over speed. 
    - Actively veto any shortcut that threatens public safety or corporate moral standing and reliability."""
    res = invoke_with_key_switching(state, prompt)
    return {"compliance_recommendation": res}

def marketing_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CMO. Review Finance constraints: {state.get('finance_recommendation', 'N/A')}. 
    
    Instructions:
    - Be highly creative and granular in designing Go-To-Market (GTM) strategies, digital physician engagement, tiered wholesale rebates, and medical device channel distribution.
    - Propose bold, out-of-the-box commercial campaigns while strictly staying within moral and ethical boundaries. 
    - Protect our brand reputation for unblemished reliability and patient trust above all short-term gains."""
    res = invoke_with_key_switching(state, prompt)
    return {"marketing_recommendation": res}

def ceo_agent(state: BoardroomState):
    time.sleep(2)
    prompt = f"""You are the CEO. Synthesize all department inputs with a deep focus on economic technicalities, numerical precision, and specific medicine/device formulations.
    
    Instructions:
    - Balance bold, out-of-the-box commercial strategies with an unyielding commitment to corporate morality, product reliability, and patient safety.
    - Clearly state the final decision, document at least one rejected alternative with reasons, outline structural trade-offs, and provide 3 rigorous, measurable business KPIs.
    
    Data Inputs:
    - Research: {state.get('research_findings')} 
    - Finance: {state.get('finance_recommendation')} 
    - Compliance: {state.get('compliance_recommendation')} 
    - Marketing: {state.get('marketing_recommendation')}"""
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

# 5. Wire the Graph
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

# 6. Dynamic Execution
if __name__ == "__main__":
    print(" PHARMA BOARDROOM ENGINE ")
    
    user_brief = input("\nEnter your custom pharmaceutical business scenario or surprise event:\n> ")
    
    initial_state = {
        "business_brief": user_brief,
        "debate_messages": [],
        "review_cycle_count": 0,
        "api_key_index": 0
    }
    
    print("\n[Swarm Initialized] Running granular cross-examination and debate...")
    final_state = pharma_swarm.invoke(initial_state)
    
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