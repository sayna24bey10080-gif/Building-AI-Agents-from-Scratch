# =============================================================
# HANDS-ON 7 — MCP Resources
# =============================================================
#
# WHAT THIS TEACHES:
#   - @mcp.resource() — exposing DATA instead of an ACTION
#   - The conceptual difference between a Tool and a Resource
#   - URI-style resource naming (e.g. "policy://all")
#
# KEY DISTINCTION:
#   Tool      -> PERFORMS AN ACTION  (e.g. check_claim_status())
#   Resource  -> PROVIDES DATA       (e.g. "give me the policy list")
#
# Think of it like a REST API:
#   Tool     = POST/PUT endpoint (does something, may have side effects)
#   Resource = GET endpoint (just returns data, read-only)
#
# THIS IS A REAL, RUNNABLE MCP SERVER.
#
# REQUIREMENTS:
#   pip install mcp
#
# HOW TO RUN:
#   python insurance_server.py
# =============================================================
 
from mcp.server.fastmcp import FastMCP
 
mcp = FastMCP("Insurance Server")
 
 
# -------------------------------------------------------------
# TOOLS (actions) — same as Hands-on 6
# -------------------------------------------------------------
 
@mcp.tool()
def get_policy(policy_id: str) -> str:
    """Get insurance policy details by policy ID."""
    policies = {
        "P1001": "Health Insurance",
        "P1002": "Car Insurance",
        "P1003": "Life Insurance",
    }
    return policies.get(policy_id, "Not Found")
 
 
@mcp.tool()
def claim_status(claim_id: str) -> str:
    """Check the current status of an insurance claim."""
    claims = {"C1001": "Approved", "C1002": "Under Review", "C1003": "Rejected"}
    return claims.get(claim_id, "Claim Not Found")
 
 
# -------------------------------------------------------------
# RESOURCE 1: All Policies (read-only data)
# -------------------------------------------------------------
# @mcp.resource("policy://all") registers a resource with a
# URI-style identifier. The AI client can "read" this resource
# to get context WITHOUT triggering any action or side effect.
#
# Compare to a tool: calling claim_status("C1001") performs a
# lookup ACTION each time. Reading policy://all just hands over
# a static-ish snapshot of data — more like a reference document.
# -------------------------------------------------------------
 
@mcp.resource("policy://all")
def get_all_policies() -> str:
    """Provide the full list of available insurance policies."""
    return """
    P1001 - Health Insurance
    P1002 - Car Insurance
    P1003 - Life Insurance
    """
 
 
# -------------------------------------------------------------
# RESOURCE 2: Company FAQ (another read-only data example)
# -------------------------------------------------------------
 
@mcp.resource("insurance://faq")
def get_faq() -> str:
    """Provide frequently asked questions about insurance policies."""
    return """
    Q: How long does claim approval take?
    A: 5-7 business days for standard claims.
 
    Q: Can I change my policy after purchase?
    A: Yes, within the first 15 days (free-look period).
 
    Q: What documents are needed for a claim?
    A: ID proof, policy document, and incident report.
    """
 
 
# -------------------------------------------------------------
# RESOURCE 3: Customer-Specific Data (parameterised resource)
# -------------------------------------------------------------
# Resources can also take parameters via the URI pattern,
# similar to a REST API path parameter.
# -------------------------------------------------------------
 
@mcp.resource("customer://{customer_id}/summary")
def get_customer_summary(customer_id: str) -> str:
    """Provide a summary of a specific customer's account."""
    customers = {
        "CUST001": "John Doe - Health Insurance - Active - Premium Rs 5000/yr",
        "CUST002": "Jane Smith - Car Insurance - Active - Premium Rs 3200/yr",
    }
    return customers.get(customer_id, f"No record found for {customer_id}")
 
 
# -------------------------------------------------------------
# Start the Server
# -------------------------------------------------------------
 
if __name__ == "__main__":
    print("Starting Insurance MCP Server...")
    print("\n2 Tools (actions):")
    print("  1. get_policy(policy_id)")
    print("  2. claim_status(claim_id)")
    print("\n3 Resources (data):")
    print("  1. policy://all")
    print("  2. insurance://faq")
    print("  3. customer://{customer_id}/summary")
    print("\nWaiting for MCP client connections (Ctrl+C to stop)...\n")
    mcp.run()
 
 
# =============================================================
# CONCEPT CHECKPOINT:
#
#   Q: Why is get_all_policies() a Resource and not a Tool?
#   A: It just returns reference data — no parameters needed,
#      no action performed, nothing changes. Pure read.
#
#   Q: Why is claim_status() a Tool and not a Resource?
#   A: It takes a specific input (claim_id) and performs a
#      targeted LOOKUP — conceptually an "action" even though
#      it doesn't modify data. The line can blur, but the
#      convention is: parameterised lookups = tools, static or
#      broad reference data = resources.
#
#   Q: What does the {customer_id} syntax in the URI mean?
#   A: It's a URI template — similar to a route parameter in a
#      web framework. MCP fills it in from the resource request.
#
# CHALLENGE:
#   Add a new resource "claims://recent" that returns a list of
#   the 3 most recently filed claims as a formatted string.
# =============================================================
 
 