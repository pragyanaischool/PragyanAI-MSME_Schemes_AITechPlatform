import pytest
from services.groq_agent import groq_agent_graph

def test_groq_agent_graph_execution():
    state_input = {
        "query": "What subsidy is available for a ₹30 Lakh machinery investment in Zone 2?",
        "language": "English",
        "company_context": "Sector: Manufacturing, Location: Bengaluru Rural, Zone: Zone 2 (Developing)",
        "rag_context": "",
        "response": ""
    }
    output = groq_agent_graph.invoke(state_input)
    assert "response" in output
    assert len(output["response"]) > 0
