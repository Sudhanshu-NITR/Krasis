import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()
from app.services.chat_service import get_assistant

def run_test_suite():
    test_queries = [
        "How does the authenticate endpoint work in LangChain Auth Service v2?"
    ]

    print(f"--- Starting Test Suite ---\n")
    
    assistant = get_assistant()

    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        result = assistant.ask(query)
        
        if result["status"] == "success":
            print(f"Response:\n{result['answer']}\n")
        else:
            print(f"Error: {result['message']}\n")
        print("-" * 30)

if __name__ == "__main__":
    run_test_suite()