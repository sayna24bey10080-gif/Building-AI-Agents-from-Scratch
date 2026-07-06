from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ==========================================
# 1. Define the Tools (@tool decorator)
# ==========================================

@tool
def calculate_attendance(total_classes: int, attended_classes: int) -> str:
    """Calculates attendance percentage and exam eligibility.
    Requires total classes and attended classes."""
    if total_classes == 0:
        return "Error: Total classes cannot be zero."
    
    percentage = (attended_classes / total_classes) * 100
    is_eligible = percentage >= 75
    status = "Eligible for Exam" if is_eligible else "Not Eligible for Exam"
    
    return f"Attendance: {percentage:.2f}%. Status: {status}."

@tool
def calculate_result(mark1: float, mark2: float, mark3: float, mark4: float, mark5: float) -> str:
    """Calculates average marks, grade, and pass/fail status from 5 individual subject marks."""
    avg = (mark1 + mark2 + mark3 + mark4 + mark5) / 5
    
    pass_status = "Pass" if avg >= 50 else "Fail"
    
    if avg >= 90:
        grade = 'A'
    elif avg >= 75:
        grade = 'B'
    elif avg >= 60:
        grade = 'C'
    else:
        grade = 'D'
        
    return f"Average Marks: {avg:.2f}, Grade: {grade}, Status: {pass_status}."

@tool
def calculate_fee_balance(total_fee: float, amount_paid: float) -> str:
    """Calculates the pending course fee amount."""
    pending = total_fee - amount_paid
    return f"Pending Fee Amount: ₹{pending:.2f}"

@tool
def calculate_library_fine(delayed_days: int) -> str:
    """Calculates the library fine amount based on delayed days."""
    fine = 5 * delayed_days
    return f"Fine Amount: ₹{fine}"

@tool
def calculate_hostel_fee(monthly_fee: float, months_stayed: int) -> str:
    """Calculates the total hostel fee based on monthly rent and duration."""
    total_fee = monthly_fee * months_stayed
    return f"Total Hostel Fee: ₹{total_fee:.2f}"

# --- Bonus Challenge ---
STUDENT_DATABASE = {
    "S101": {"name": "Aarav Sharma", "course": "B.Tech CS", "year": "2nd Year"},
    "S102": {"name": "Priya Patel", "course": "B.Com", "year": "3rd Year"},
    "S103": {"name": "Rohan Gupta", "course": "B.Sc Physics", "year": "1st Year"}
}

@tool
def get_student_info(student_id: str) -> str:
    """Retrieves student details (name, course, year) using their Student ID."""
    student = STUDENT_DATABASE.get(student_id.upper())
    if student:
        return f"Student Found - Name: {student['name']}, Course: {student['course']}, Year: {student['year']}."
    return f"No student found with ID: {student_id}."

# ==========================================
# 2. Setup the Agent (Ollama Version)
# ==========================================

def setup_agent():
    # Initialize the local Ollama LLM
    # Make sure your local Ollama server is running!
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )
    
    # List of all tools available to the agent
    tools = [
        calculate_attendance,
        calculate_result,
        calculate_fee_balance,
        calculate_library_fine,
        calculate_hostel_fee,
        get_student_info
    ]
    
    # Define the Prompt Template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful and intelligent College Assistant. Use the provided tools to answer student queries accurately. If a query requires multiple calculations, use all necessary tools before giving a final consolidated answer."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Create the Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the Agent Executor with verbose=True
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    
    return agent_executor

# ==========================================
# 3. Test Cases Execution
# ==========================================

def run_tests():
    agent_executor = setup_agent()
    
    test_cases = {
        "Query 1 (Attendance)": "I attended 72 classes out of 90. Am I eligible for exams?",
        "Query 2 (Result)": "My marks are (95, 90, 88, 91 and 87). What is my grade?",
        "Query 3 (Fee Balance)": "My course fee is 50000 and I have paid 35000. How much fee is pending?",
        "Query 4 (Library Fine)": "I returned a library book 8 days late. What is the fine amount?",
        "Query 5 (Hostel Fee)": "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
        "Bonus Query (Student Info)": "Can you get the details for student ID S102?",
        "Multi-Tool Challenge": """I attended 80 classes out of 100.
My marks are 90, 85, 88, 92 and 95.
My course fee is 60000 and I paid 45000.
Provide:
1. Attendance Status
2. Grade
3. Pending Fee"""
    }

    print("\nStarting Agent Tests with Ollama (Qwen 2.5:3b)...\n" + "="*50)
    
    for title, query in test_cases.items():
        print(f"\n\n--- Running {title} ---")
        print(f"User Query: {query}\n")
        
        try:
            # Invoke the agent
            response = agent_executor.invoke({"input": query})
            print("\nFinal Output:\n", response['output'])
        except Exception as e:
             print(f"\nError executing query: {e}")
             
        print("="*50)

if __name__ == "__main__":
    run_tests()