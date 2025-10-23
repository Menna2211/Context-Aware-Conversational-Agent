from agents import build_context_aware_agent
from langchain_core.messages import HumanMessage

def main():
    """Main execution - Week 1 Demo"""
    print("=" * 60)
    print("Context-Aware Chatbot Agent")
    print("=" * 60)
    
    # Build the agent
    agent = build_context_aware_agent()
    
    # Test cases
    test_queries = [
        "What is LangChain used for?",
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Test Query {i}: {query}")
        print("=" * 60)
        
        # Invoke the agent
        response = agent.invoke({
            "messages": [HumanMessage(content=query)]
        })
        
        # Print the response
        print("\nAgent Response:")
        print(response["messages"][-1].content)
        print()

if __name__ == "__main__":
    main()