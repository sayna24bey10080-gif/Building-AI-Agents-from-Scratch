# =============================================================
# HANDS-ON 2 — MCP Architecture Mapping
# =============================================================
#
# WHAT THIS TEACHES:
#   - The 4 core MCP components: Host, Client, Server, Tool/Resource
#   - How to map a REAL business scenario onto MCP architecture
#   - Practice mapping 3 different domains (loan, hospital, university)
#
# NO MCP INSTALLED YET — this is a conceptual/printed exercise.
#
# REQUIREMENTS: none (standard Python only)
#
# HOW TO RUN:
#   python app.py
# =============================================================
 
print("\n=== HANDS-ON 2: MCP ARCHITECTURE MAPPING ===\n")
 
 
# -------------------------------------------------------------
# STEP 1: The 4 MCP Components
# -------------------------------------------------------------
 
print("=" * 60)
print("THE 4 MCP COMPONENTS")
print("=" * 60)
print("""
  HOST     -> The AI application the user talks to
              (Claude Desktop, ChatGPT, a custom AI assistant)
 
  CLIENT   -> Lives inside the Host. Speaks MCP protocol to Servers.
              Discovers what tools/resources are available.
 
  SERVER   -> Exposes tools, resources, and prompts over MCP.
              This is what YOU build for your business domain.
 
  TOOL     -> An action the AI can PERFORM
              (e.g. "check claim status", "approve a loan")
 
  RESOURCE -> Data the AI can READ
              (e.g. "all policies", "customer database")
""")
 
 
# -------------------------------------------------------------
# STEP 2: Insurance Scenario Mapping
# -------------------------------------------------------------
 
print("=" * 60)
print("SCENARIO: Customer asks - 'What is the status of claim C1001?'")
print("=" * 60)
 
insurance_mapping = {
    "Host":     "AI Assistant (e.g. Claude Desktop / Custom Chatbot)",
    "Client":   "MCP Client (built into the Host)",
    "Server":   "Insurance MCP Server",
    "Tool":     "claim_status(claim_id) — performs the lookup ACTION",
    "Resource": "Claim Database — the underlying DATA being read",
}
 
for component, mapping in insurance_mapping.items():
    print(f"  {component:<10} -> {mapping}")
 
print("""
Flow:
  Customer asks question
       |
  AI Assistant (Host) receives it
       |
  MCP Client decides: "I need the claim_status tool"
       |
  MCP Client calls Insurance MCP Server
       |
  Server runs claim_status('C1001') tool
       |
  Server returns result through Client back to Host
       |
  Host shows answer to customer
""")
 
 
# -------------------------------------------------------------
# STEP 3: Practice — Map 3 More Domains
# -------------------------------------------------------------
# Students fill in / verify these mappings.
# Each dict follows the same Host/Client/Server/Tool/Resource pattern.
# -------------------------------------------------------------
 
print("=" * 60)
print("PRACTICE: Map These 3 Systems to MCP Architecture")
print("=" * 60)
 
domains = {
    "Loan Approval System": {
        "Host":     "Bank's AI Loan Assistant",
        "Client":   "MCP Client inside the assistant",
        "Server":   "Loan MCP Server",
        "Tool":     "check_loan_eligibility(customer_id), approve_loan(loan_id)",
        "Resource": "Customer Credit Score Database",
    },
    "Hospital System": {
        "Host":     "Hospital AI Assistant (for staff or patients)",
        "Client":   "MCP Client inside the assistant",
        "Server":   "Hospital MCP Server",
        "Tool":     "book_appointment(patient_id), check_bed_availability()",
        "Resource": "Patient Records Database",
    },
    "University System": {
        "Host":     "University AI Helpdesk",
        "Client":   "MCP Client inside the helpdesk",
        "Server":   "University MCP Server",
        "Tool":     "check_attendance(student_id), register_course(course_id)",
        "Resource": "Student Academic Records",
    },
}
 
for domain_name, mapping in domains.items():
    print(f"\n--- {domain_name} ---")
    for component, value in mapping.items():
        print(f"  {component:<10} -> {value}")
 
 
# =============================================================
# CONCEPT CHECKPOINT:
#
#   Q: What's the difference between a Tool and a Resource?
#   A: Tool = performs an ACTION (approve_loan, book_appointment)
#      Resource = provides DATA to read (patient records, all policies)
#
#   Q: Does the Host directly talk to the Server?
#   A: No. The Host's MCP Client talks to the Server. The Host
#      itself just shows results to the user.
#
#   Q: Can one MCP Server expose multiple tools and resources?
#   A: Yes — Hands-on 6 and 7 show a server with 3 tools, and
#      Hands-on 7 adds a resource to the same server.
#
# CHALLENGE:
#   Map an E-Commerce system (Customer, Product, Order, Inventory)
#   to MCP architecture using the same Host/Client/Server/Tool/
#   Resource pattern shown above.
# =============================================================
 
 