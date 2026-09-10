# src/agent.py

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv

from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage
)
from langchain_core.tools import tool

from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from src.tools import (
    get_program_info,
    check_application_status,
    get_deadlines
)


# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Please add it to your .env file."
    )


# ---------------------------------------------------------
# LangGraph State
# ---------------------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# ---------------------------------------------------------
# Tools
# ---------------------------------------------------------

@tool
def program_info_tool(program_name: str) -> dict:
    """
    Get information about a university program.

    Returns program name, duration, tuition and prerequisites.
    """
    return get_program_info(program_name)


@tool
def application_status_tool(applicant_id: str) -> dict:
    """
    Check the status of a university application.

    Returns applicant name, program, application status,
    next step and pending documents.
    """
    return check_application_status(applicant_id)


@tool
def deadlines_tool(program_name: str) -> dict:
    """
    Get important deadlines for a university program.

    Returns application deadline, document submission deadline
    and decision notification date.
    """
    return get_deadlines(program_name)


TOOLS = [
    program_info_tool,
    application_status_tool,
    deadlines_tool
]


# ---------------------------------------------------------
# LLM
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    temperature=0,
    google_api_key=API_KEY
)

llm_with_tools = llm.bind_tools(TOOLS)


# ---------------------------------------------------------
# System Instructions
# ---------------------------------------------------------

SYSTEM_MESSAGE = SystemMessage(
    content="""
You are a Student Enrollment Assistant for a university admissions office.

Your responsibilities are:

1. Help students understand available university programs.
2. Provide program information using the program information tool.
3. Provide application deadlines using the deadlines tool.
4. Check application status using the application status tool.
5. Remember relevant information from earlier messages in the conversation.
6. If a student refers to "that program", "the program", or similar wording,
   use the previous conversation context to identify the program.
7. Never invent application, program, deadline, tuition or document information.
   Use the available tools whenever factual university information is requested.
8. If the user asks something unsupported by the available tools, such as
   fee waivers, scholarships, financial aid, or other policies, politely
   escalate to an enrollment counselor.

For unsupported questions, respond naturally using wording similar to:

"I'd recommend speaking with an enrollment counselor for that.
Would you like me to connect you?"

Keep responses concise, helpful and conversational.
"""
)


# ---------------------------------------------------------
# Agent Node
# ---------------------------------------------------------

def agent_node(state: AgentState):

    messages = state["messages"]

    # Add system instructions before the conversation.
    messages_for_llm = [SYSTEM_MESSAGE] + messages

    response = llm_with_tools.invoke(messages_for_llm)

    return {
        "messages": [response]
    }


# ---------------------------------------------------------
# Build LangGraph
# ---------------------------------------------------------

graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", ToolNode(TOOLS))

# Start -> Agent
graph_builder.add_edge(START, "agent")

# Agent decides whether a tool is required.
#
# If tool is required:
#     agent -> tools
#
# If no tool is required:
#     agent -> END
graph_builder.add_conditional_edges(
    "agent",
    tools_condition
)

# After executing a tool, return to the agent
# so it can formulate the final answer.
graph_builder.add_edge("tools", "agent")


# ---------------------------------------------------------
# Memory
# ---------------------------------------------------------

memory = MemorySaver()

graph = graph_builder.compile(
    checkpointer=memory
)


# ---------------------------------------------------------
# Enrollment Agent
# ---------------------------------------------------------

class EnrollmentAgent:

    def __init__(self, thread_id: str = "student-session-001"):

        self.config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

    def chat(self, user_message: str) -> str:

        result = graph.invoke(
            {
                "messages": [
                    HumanMessage(content=user_message)
                ]
            },
            config=self.config
        )

        # Find the latest AI response.
        for message in reversed(result["messages"]):

            if isinstance(message, AIMessage):

                content = message.content

                # Usually Gemini returns a simple string.
                if isinstance(content, str):
                    return content

                # Handle structured content safely.
                if isinstance(content, list):

                    text_parts = []

                    for item in content:

                        if isinstance(item, dict):
                            if "text" in item:
                                text_parts.append(item["text"])

                        elif isinstance(item, str):
                            text_parts.append(item)

                    if text_parts:
                        return " ".join(text_parts)

        return "I'm sorry, I couldn't generate a response."


# ---------------------------------------------------------
# Test helper
# ---------------------------------------------------------

if __name__ == "__main__":

    agent = EnrollmentAgent()

    print("\nStudent Enrollment Assistant")
    print("--------------------------------")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        response = agent.chat(user_input)

        print(f"\nAssistant: {response}")