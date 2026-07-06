# =============================================================
# CAPSTONE — Enterprise Insurance Assistant (Qwen + Ollama)
# =============================================================
#
# WHAT THIS DEMONSTRATES:
#   - Replacing keyword-matching (Hands-on 9) and fixed-sequence
#     calling (Hands-on 10-11) with a REAL LLM making decisions
#   - Qwen 2.5 (via Ollama) decides WHICH insurance tool(s) to
#     call based on natural language understanding, not keywords
#   - 6 insurance tools wired to a local, free, offline LLM
#   - This is the production-pattern version of Hands-on 9-11
#
# ARCHITECTURE NOTE:
#   This capstone does NOT run a separate MCP client/server
#   process pair — it uses the SAME tool functions you built
#   in Hands-on 5-8 (as @mcp.tool() functions) directly in
#   Python, with Qwen choosing which to call. This mirrors
#   exactly what an MCP Client + AI Host does internally, while
#   staying simple enough to run as a single script in class.
#
#   If you want the FULL separate MCP server + client architecture,
#   take insurance_server.py from Hands-on 8 (it already has all
#   6 tools as @mcp.tool()) and connect it via the mcp Python
#   client SDK — that is a natural next step after this capstone.
#
# REQUIREMENTS:
#   pip install mcp httpx python-dotenv rich
#   ollama pull qwen2.5:3b
#   (keep Ollama running before starting this script)
#
# HOW TO RUN:
#   python app.py
# =============================================================
 
import json
import httpx
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
 
console = Console()
 
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:3b"
 
 
# =============================================================
# SECTION 1: THE 6 INSURANCE TOOLS
# =============================================================
# These are the SAME tools from Hands-on 5-8, written as plain
# Python functions here. In a full deployment, these would be
# the @mcp.tool() decorated functions inside an MCP server.
# =============================================================
 
CUSTOMER_DB = {
    "C001": {"name": "John",  "policy_id": "P1001", "since": "2021"},
    "C002": {"name": "Priya", "policy_id": "P1002", "since": "2023"},
}
 
POLICY_DB = {
    "P1001": {"type": "Health Insurance", "premium": 5000, "active": True},
    "P1002": {"type": "Car Insurance",    "premium": 3200, "active": True},
    "P1003": {"type": "Life Insurance",   "premium": 7800, "active": False},
}
 
CLAIM_DB = {
    "CL001": {"customer_id": "C001", "status": "Approved",     "amount": 25000},
    "CL002": {"customer_id": "C002", "status": "Under Review", "amount": 80000},
    "CL003": {"customer_id": "C001", "status": "Rejected",     "amount": 150000},
}
 
 
def get_customer(customer_id: str) -> dict:
    """Get customer profile information by customer ID."""
    return CUSTOMER_DB.get(customer_id, {"error": f"Customer {customer_id} not found"})
 
 
def get_policy(policy_id: str) -> dict:
    """Get insurance policy details by policy ID."""
    return POLICY_DB.get(policy_id, {"error": f"Policy {policy_id} not found"})
 
 
def claim_status(claim_id: str) -> dict:
    """Get the current status of an insurance claim by claim ID."""
    return CLAIM_DB.get(claim_id, {"error": f"Claim {claim_id} not found"})
 
 
def premium_due(customer_id: str) -> dict:
    """Get the premium amount due for a customer."""
    customer = CUSTOMER_DB.get(customer_id)
    if not customer:
        return {"error": f"Customer {customer_id} not found"}
    policy = POLICY_DB.get(customer["policy_id"], {})
    return {"customer_id": customer_id, "premium": policy.get("premium", "Unknown")}
 
 
def fraud_check(claim_id: str) -> dict:
    """Run a fraud risk assessment on a claim."""
    claim = CLAIM_DB.get(claim_id)
    if not claim:
        return {"error": f"Claim {claim_id} not found"}
    amount = claim["amount"]
    if amount > 100000:
        risk = "HIGH RISK — manual review required"
    elif amount > 50000:
        risk = "MEDIUM RISK — standard verification recommended"
    else:
        risk = "LOW RISK"
    return {"claim_id": claim_id, "risk_level": risk}
 
 
def renew_policy(policy_id: str) -> dict:
    """Renew an insurance policy by policy ID."""
    policy = POLICY_DB.get(policy_id)
    if not policy:
        return {"error": f"Policy {policy_id} not found"}
    policy["active"] = True
    return {"policy_id": policy_id, "status": "Renewed Successfully", "premium": policy["premium"]}
 
 
# Map tool names (as strings) to actual Python functions
TOOL_REGISTRY = {
    "get_customer":  get_customer,
    "get_policy":    get_policy,
    "claim_status":  claim_status,
    "premium_due":   premium_due,
    "fraud_check":   fraud_check,
    "renew_policy":  renew_policy,
}
 
 
# =============================================================
# SECTION 2: TALK TO QWEN VIA OLLAMA (no extra SDK needed)
# =============================================================
# We use httpx directly against Ollama's REST API.
# This keeps the capstone dependency-light — no langchain
# needed, just httpx (already in requirements.txt).
# =============================================================
 
def call_qwen(prompt: str) -> str:
    """Send a prompt to Qwen via Ollama's local REST API."""
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    try:
        response = httpx.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
    except httpx.ConnectError:
        return "ERROR: Cannot connect to Ollama. Is it running? Try: ollama serve"
    except Exception as e:
        return f"ERROR: {e}"
 
 
# =============================================================
# SECTION 3: THE AGENT — Qwen Decides Which Tool(s) to Call
# =============================================================
# This replaces Hands-on 9's keyword matching with REAL
# language understanding. Qwen reads the user's query and
# decides which tool(s) are relevant and what parameters to use.
# =============================================================
 
def decide_tools(query: str) -> list:
    """
    Ask Qwen which tool(s) should be called for this query.
    Returns a list of {"tool": name, "input": {param: value}}
    """
    prompt = f"""You are an insurance assistant with access to these tools:
 
1. get_customer(customer_id)   — get customer profile. IDs look like: C001, C002
2. get_policy(policy_id)       — get policy details. IDs look like: P1001, P1002, P1003
3. claim_status(claim_id)      — get claim status. IDs look like: CL001, CL002, CL003
4. premium_due(customer_id)    — get premium amount owed by a customer
5. fraud_check(claim_id)       — run fraud risk check on a claim
6. renew_policy(policy_id)     — renew a policy
 
User query: {query}
 
Decide which tool(s) are needed to answer this query. You may need
more than one (e.g. checking a claim often also needs a fraud check).
 
Respond with ONLY a valid JSON array, no explanation, no markdown:
[{{"tool": "claim_status", "input": {{"claim_id": "CL001"}}}}]
 
If multiple tools are needed, include multiple objects in the array.
If you cannot identify a specific ID from the query, use a reasonable
default like C001, P1001, or CL001.
"""
 
    raw = call_qwen(prompt)
    cleaned = raw.strip().replace("```json", "").replace("```", "").strip()
 
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        console.print(f"[yellow]Could not parse Qwen's tool selection: {raw[:200]}[/yellow]")
        return []
 
 
def run_tools(tool_calls: list) -> list:
    """Execute each tool call requested by Qwen and collect results."""
    results = []
    for call in tool_calls:
        tool_name = call.get("tool")
        tool_input = call.get("input", {})
 
        if tool_name not in TOOL_REGISTRY:
            results.append({"tool": tool_name, "error": "Unknown tool"})
            continue
 
        func = TOOL_REGISTRY[tool_name]
        try:
            output = func(**tool_input)
            results.append({"tool": tool_name, "input": tool_input, "output": output})
        except TypeError as e:
            results.append({"tool": tool_name, "error": f"Bad input: {e}"})
 
    return results
 
 
def synthesize_answer(query: str, tool_results: list) -> str:
    """Ask Qwen to turn raw tool results into a natural answer."""
    results_text = json.dumps(tool_results, indent=2)
 
    prompt = f"""Original question: {query}
 
Tool results retrieved:
{results_text}
 
Write a clear, professional answer to the customer using this real data.
Be specific — include actual numbers, statuses, and IDs from the data.
Keep it to 2-4 sentences. Do not mention "tools" or "JSON" — just answer naturally.
"""
    return call_qwen(prompt)
 
 
def insurance_agent(query: str) -> str:
    """Full agent pipeline: decide tools -> run tools -> synthesize answer."""
    console.print(f"\n[cyan]🧠 Qwen deciding which tools to call...[/cyan]")
    tool_calls = decide_tools(query)
 
    if not tool_calls:
        console.print("[yellow]No tools selected — answering directly[/yellow]")
        return call_qwen(query)
 
    console.print(f"[blue]🔧 Tools selected: {[c.get('tool') for c in tool_calls]}[/blue]")
    tool_results = run_tools(tool_calls)
 
    console.print(f"[green]✓ Tools executed, synthesizing answer...[/green]")
    return synthesize_answer(query, tool_results)
 
 
# =============================================================
# SECTION 4: RUN THE CAPSTONE
# =============================================================
 
DEMO_QUERIES = [
    "What is the status of claim CL001?",
    "Is there any fraud risk on claim CL003?",
    "How much premium does customer C001 owe?",
    "Show me the policy details for P1002",
    "Renew policy P1003 for me",
    "Tell me about customer C002 and their policy",
]
 
if __name__ == "__main__":
    console.print("\n[bold magenta]=== ENTERPRISE INSURANCE ASSISTANT (Qwen + Ollama) ===[/bold magenta]")
    console.print("[dim]Model: qwen2.5:3b via Ollama  |  100% local, 100% free[/dim]\n")
 
    # Quick connectivity check
    test = call_qwen("Say OK")
    if "ERROR" in test:
        console.print(Panel(test, title="[bold red]Connection Problem[/bold red]", border_style="red"))
        console.print("\nMake sure Ollama is running and qwen2.5:3b is pulled:")
        console.print("  ollama pull qwen2.5:3b")
        console.print("  ollama serve")
        exit(1)
 
    console.print("[green]Connected to Ollama successfully![/green]\n")
 
    for query in DEMO_QUERIES:
        console.print(f"\n[bold white]Customer Query:[/bold white] {query}")
        answer = insurance_agent(query)
        console.print(Panel(answer, title="[bold green]Assistant Response[/bold green]", border_style="green"))
 
    console.print("\n[bold yellow]=== Capstone Complete ===[/bold yellow]")
    console.print("All 6 insurance tools wired to a free, local LLM.")
    console.print("Zero API cost. Zero cloud dependency.")
 
 
# =============================================================
# CONCEPT CHECKPOINT:
#
#   Q: How is this different from Hands-on 9's keyword agent?
#   A: Hands-on 9 checked if "claim" or "policy" literally
#      appeared in the text. Here, Qwen READS and UNDERSTANDS
#      the query — "Is there fraud risk on CL003?" correctly
#      triggers fraud_check(), not just claim_status(), even
#      though the word "fraud" wasn't an exact keyword match
#      against a hardcoded list.
#
#   Q: Why use httpx directly instead of langchain_ollama?
#   A: Keeps this lab dependency-light and shows students what's
#      actually happening under the hood — a simple HTTP POST
#      to Ollama's REST API. No framework magic.
#
#   Q: What's the relationship between this and the real MCP
#      Server from Hands-on 5-8?
#   A: In production, TOOL_REGISTRY's functions would be the
#      EXACT SAME @mcp.tool() functions running inside
#      insurance_server.py, and decide_tools()/run_tools() would
#      be replaced by the official MCP Client SDK talking to
#      that server over the real MCP protocol. This capstone
#      shows the AGENT LOGIC clearly first — wiring it to a real
#      MCP client/server pair is a natural next project.
#
#   Q: Is this 100% free?
#   A: Yes. Ollama + Qwen 2.5 3B runs entirely on your machine.
#      No API key, no per-token cost, works offline once the
#      model is downloaded.
#
# CHALLENGE:
#   Add a 7th tool: cancel_policy(policy_id) and update the
#   decide_tools() prompt to describe it. Test with a query like
#   "I want to cancel my car insurance policy P1002."
# =============================================================
 
 