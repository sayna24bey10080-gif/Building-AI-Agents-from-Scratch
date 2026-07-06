from typing import TypedDict
from langgraph.graph import StateGraph, END
 
 
 
#Define state
 
class StudentState(TypedDict):
    name:str
    marks:int
    grade:str
    feedback:str
    ispass:bool
 
#Node
#calculate Grade
 
def calculate_grade(state:StudentState):
    marks=state["marks"]
 
    if marks >=90:
        grade="A"
 
    elif marks >= 75:
        grade = "B"
 
    else:
        grade = "C"
 
    return {
        "grade": grade
    }
#Generate Feedback
 
def generate_feedback(state:StudentState):
 
    grade=state["grade"]
 
    feedback_map={
         "A": "Excellent",
        "B": "Good",
        "C": "Need Improvement"
    }
 
    return {
        "feedback":feedback_map[grade]
    }
 
def result_checker(state:StudentState):
   
        return{
                "ispass":state["marks"]>=40
        }
   
 
#Node Builder
 
builder=StateGraph(StudentState)
 
#Add Nodes to the graph
 
#Syntax
#builder.add_node(
 #   "node_name",
 #   function_name
#)
 
builder.add_node(
    "calculate_grade",calculate_grade
)
 
builder.add_node(
    "generate_feedback",generate_feedback
)
builder.add_node(
    "result_checker",result_checker
)
#Set Entry point
 
builder.set_entry_point(
    "calculate_grade"
)
 
builder.add_edge(
    "calculate_grade",
    "generate_feedback",
)
 
builder.add_edge(
    "generate_feedback",
    "result_checker"
)
 
builder.add_edge(
    "result_checker",
    END
)
 
graph=builder.compile()
 
result=graph.invoke({
    "name":"Tom",
    "marks":75,
    "ispass":False
})
 
print("\nStudent Evaluation Result")
print("-" * 30)
 
for key, value in result.items():
    print(f"{key}: {value}")
 
 
 
    # Task
    #Add a new field to State
    #Create a new Node
    #Connect it to the workflow
 
    #Rule: Marks >= 40 → Pass
     #Marks < 40 → Fail