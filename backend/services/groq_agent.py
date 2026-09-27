import os
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from config import settings

class AgentState(TypedDict):
    query: str
    language: str
    company_context: str
    rag_context: str
    response: str

def load_rag_knowledge() -> str:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    docs_dir = os.path.join(base_dir, "data", "docs")
    content = []
    if os.path.exists(docs_dir):
        for fn in os.listdir(docs_dir):
            if fn.endswith(".txt"):
                with open(os.path.join(docs_dir, fn), "r", encoding="utf-8") as f:
                    content.append(f.read())
    return "\n\n".join(content)

rag_corpus = load_rag_knowledge()

def retriever_node(state: AgentState) -> AgentState:
    state["rag_context"] = rag_corpus[:4000]
    return state

def generator_node(state: AgentState) -> AgentState:
    if not settings.GROQ_API_KEY:
        state["response"] = "Mock Advisor: Groq API key is not configured on the backend server."
        return state

    llm = ChatGroq(
        model_name=settings.GROQ_MODEL,
        temperature=0.1,
        groq_api_key=settings.GROQ_API_KEY
    )

    sys_prompt = f"""
    You are the Senior MSME Subsidy Navigator for India and Karnataka.
    ENTERPRISE PROFILE:
    {state['company_context']}

    OFFICIAL POLICY CONTEXT:
    {state['rag_context']}

    RULES:
    1. Respond in {state['language']}.
    2. Give exact financial percentages, limits, and eligibility steps.
    3. Cite official state portals (e.g., e-Udyog, JanSamarth).
    """

    res = llm.invoke([
        SystemMessage(content=sys_prompt),
        HumanMessage(content=state["query"])
    ])
    state["response"] = res.content
    return state

workflow = StateGraph(AgentState)
workflow.add_node("retriever", retriever_node)
workflow.add_node("generator", generator_node)
workflow.set_entry_point("retriever")
workflow.add_edge("retriever", "generator")
workflow.add_edge("generator", END)

groq_agent_graph = workflow.compile()
