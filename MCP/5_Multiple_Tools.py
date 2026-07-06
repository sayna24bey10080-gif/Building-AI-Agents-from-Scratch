# =============================================================
# HANDS-ON 6 — Multiple MCP Tools on One Server
# =============================================================
#
# WHAT THIS TEACHES:
#   - A single MCP server can expose MANY tools
#   - Each @mcp.tool() is independent — its own name, schema, logic
#   - How an AI client would see and choose between 3 different tools
#
# THIS IS A REAL, RUNNABLE MCP SERVER.
#
# REQUIREMENTS:
#   pip install mcp
#
# HOW TO RUN:
#   python insurance_server.py
#
# TEST WITH MCP INSPECTOR (requires Node.js):
#   npx @modelcontextprotocol/inspector python insurance_server.py
# =============================================================
 
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("Insurance Server")
 
 
# -------------------------------------------------------------
# TOOL 1: Policy Lookup
# -------------------------------------------------------------
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """Get insurance policy details by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return f"Policy {policy_id}: {policies.get(policy_id, 'Not Found')}"
 
 
# -------------------------------------------------------------
# TOOL 2: Claim Status
# -------------------------------------------------------------
 
@mcp.tool()
def claim_status(claim_id: str) -> str:
    """Check the current status of an insurance claim."""
    claims = {
        "C1001": "Approved",
        "C1002": "Under Review",
        "C1003": "Rejected",
    }
    status = claims.get(claim_id, "Claim Not Found")
    return f"Claim {claim_id}: {status}"
 
 
# -------------------------------------------------------------
# TOOL 3: Premium Due
# -------------------------------------------------------------
 
@mcp.tool()
def premium_due(customer_id: str) -> str:
    """Get the premium amount due for a customer."""
    premiums = {
        "CUST001": 5000,
        "CUST002": 3200,
        "CUST003": 7800,
    }
    amount = premiums.get(customer_id)
    if amount is None:
        return f"No premium record found for {customer_id}"
    return f"Premium due for {customer_id}: Rs {amount:,}"
 
 
# -------------------------------------------------------------
# Start the Server
# -------------------------------------------------------------
 
if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("\n3 Tools available:")
    print("  1. get_policy(policy_id)")
    print("  2. claim_status(claim_id)")
    print("  3. premium_due(customer_id)")
    print("\nWaiting for MCP client connections (Ctrl+C to stop)...\n")
    mcp.run()
 
 
# =============================================================
# CONCEPT CHECKPOINT:
#
#   Q: Does the order of @mcp.tool() functions matter?
#   A: No. Each tool is registered independently. The AI client
#      discovers all of them and picks whichever fits the query.
#
#   Q: How would an AI agent decide which of these 3 tools to call?
#   A: It reads each tool's name, docstring, and parameter schema,
#      compares them to the user's question, and picks the best
#      match. This decision-making happens on the CLIENT side
#      (the AI), not inside the server.
#
#   Q: Can two tools have overlapping functionality?
#   A: Technically yes, but it's bad practice — it makes tool
#      selection ambiguous for the AI. Keep each tool's purpose
#      distinct, like we have here (lookup vs status vs billing).
#
# CHALLENGE:
#   Add a 4th tool: policy_renewal_date(policy_id) that returns
#   a renewal date string for each policy ID. Add it to the
#   policies dict pattern used in get_policy().
# =============================================================
 