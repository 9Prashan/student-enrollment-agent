# Student Enrollment Assistant
An Agentic AI Student Enrollment Assistant built with Python, LangGraph, LangChain, and Google Gemini.
## Features
- Program information lookup
- Application status checking
- Application deadline lookup
- Multi-turn conversation memory
- Context-aware follow-up questions
- Graceful escalation for unsupported questions
## Architecture
User -> LangGraph Agent -> Tool Selection -> Tool Execution -> Agent -> Response
## Tools
### Program Information
Returns program name, duration, tuition and prerequisites.
### Application Status
Returns applicant name, applied program, application status, next step and pending documents.
### Application Deadlines
Returns application deadline, document submission deadline and decision notification date.
## Mock Data
Programs:
- Bachelor of Computer Science
- Master of Computer Science
- Bachelor of Data Science
Applicants:
- APP-1042
- APP-1043
- APP-1044
## Technology Stack
- Python
- LangGraph
- LangChain
- Google Gemini
- LangChain Google GenAI
- Python-dotenv
## Project Structure
student-enrollment-agent/
|
|-- src/
|   |-- agent.py
|   |-- main.py
|   |-- tools.py
|
|-- README.md
|-- requirements.txt
|-- .gitignore
## Setup
Create a virtual environment:
python -m venv .venv
Activate on Windows:
.venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Create a .env file:
GEMINI_API_KEY=your_api_key_here
Run:
python -m src.main
## Required Demonstration
1. Hi, what programs do you offer in computer science?
2. What's the application deadline for that?
3. I already applied. My ID is APP-1042. What's my status?
4. Can I get a fee waiver?
5. What documents do I still need to submit?
The agent uses tools for factual university information, maintains conversation context through LangGraph memory, and escalates unsupported questions to an enrollment counselor.
## Limitations
This project uses mock data and is intended as a demonstration. It does not connect to a real university admissions database.
