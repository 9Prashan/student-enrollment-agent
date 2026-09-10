# src/main.py

from src.agent import EnrollmentAgent


def main():

    agent = EnrollmentAgent(
        thread_id="student-demo-001"
    )

    conversation = [
        "Hi, what programs do you offer in computer science?",
        "What's the application deadline for that?",
        "I already applied. My ID is APP-1042. What's my status?",
        "Can I get a fee waiver?",
        "What documents do I still need to submit?"
    ]

    print("=" * 70)
    print("STUDENT ENROLLMENT ASSISTANT - DEMO")
    print("=" * 70)

    for turn_number, user_message in enumerate(conversation, start=1):

        print(f"\nTurn {turn_number}")
        print(f"Student: {user_message}")

        response = agent.chat(user_message)

        print(f"Assistant: {response}")


if __name__ == "__main__":
    main()