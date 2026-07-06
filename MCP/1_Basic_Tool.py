# =============================================================
# HANDS-ON 1 — Understanding MCP Basics
# =============================================================
#
# WHAT THIS TEACHES:
#   - Why MCP exists — the problem it solves
#   - A plain Python function BEFORE we add any MCP machinery
#   - The conceptual difference between calling a function directly
#     vs going through MCP's standardised layers
#
# NO MCP INSTALLED YET — this is pure Python.
#
# REQUIREMENTS: none (standard Python only)
#
# HOW TO RUN:
#   python app.py
# =============================================================
 
print("\n UNDERSTANDING MCP BASICS ===\n")
 
 
# -------------------------------------------------------------
# STEP 1: A Plain Python Tool (no MCP at all)
# -------------------------------------------------------------
# This is just a function. Nothing AI-related, nothing MCP-related.
# We start here so the value of MCP is obvious once we add it.
# -------------------------------------------------------------
 
def get_policy_details(policy_id: str) -> str:
    """Look up policy type by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return policies.get(policy_id, "Policy Not Found")
 
 
print("Calling get_policy_details('P1002') directly:")
print(" ", get_policy_details("P1002"))
 
print("\nCalling get_policy_details('P9999') (unknown ID):")
print(" ", get_policy_details("P9999"))
 
 
 
 
 
# =============================================================
# CONCEPT CHECKPOINT:
#
#   Q: Is get_policy_details() an MCP tool right now?
#   A: No — it's a plain Python function. We turn it into an
#      MCP tool in Hands-on 5 using the @mcp.tool() decorator.
#
#   Q: What problem does MCP actually solve?
#   A: Without it, every AI application needs custom glue code
#      to talk to every tool/database/API. MCP standardises that
#      connection so tools are written once and reused everywhere.
#
#   Q: Is MCP specific to OpenAI or Claude?
#   A: No. MCP is an open protocol. Any AI host (Claude Desktop,
#      custom agents, IDE assistants) that implements an MCP
#      client can talk to any MCP server.
#
# CHALLENGE:
#   Add a get_premium_amount(policy_id) function that returns
#   a premium amount for each policy. We'll convert it to a
#   real MCP tool in Hands-on 6.
# =============================================================
 
 