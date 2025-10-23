from agents import build_context_aware_agent
from langchain_core.messages import HumanMessage
from tools import judge_context_presence, web_search ,split_context ,check_context_relevance

def demo_workflow_adherence():
    """
    Demonstrates that the agent follows the specified workflow
    """
    print("=" * 80)
    print("Context-Aware Agent - Workflow Validation Demo")
    print("=" * 80)
    print("\nWorkflow:")
    print("1. User query → ContextPresenceJudge")
    print("2. If missing → WebSearch")
    print("3. If provided → ContextRelevanceChecker")
    print("4. If relevant → ContextSplitter")
    print("5. Answer\n")
    print("=" * 80)
    
    agent = build_context_aware_agent()
    
    test_cases = [
        {
            "name": "Flow A: Missing Context",
            "query": "What are attention mechanisms?",
            "expected_flow": "judge → search → answer"
        },
        {
            "name": "Flow B: Context Provided + Relevant",
            "query": "Attention mechanisms are components that help models focus on input parts. How are they used in transformers?",
            "expected_flow": "judge → relevance_check → splitter → answer"
        },
        {
            "name": "Flow C: Context Provided + Irrelevant",
            "query": "Python is a programming language. What are attention mechanisms?",
            "expected_flow": "judge → relevance_check → search → answer"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test Case {i}: {test['name']}")
        print(f"Expected Flow: {test['expected_flow']}")
        print("=" * 80)
        print(f"Query: {test['query']}")
        print("-" * 80)
        
        try:
            response = agent.invoke({
                "messages": [HumanMessage(content=test['query'])]
            })
            
            # Track tool usage
            print("\n🔧 Tools Called (in order):")
            tool_sequence = []
            for msg in response["messages"]:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tc in msg.tool_calls:
                        tool_sequence.append(tc['name'])
                        print(f"   → {tc['name']}")
            
            # Validate workflow
            print(f"\n✅ Tool Sequence: {' → '.join(tool_sequence) if tool_sequence else 'No tools'}")
            
            # Final answer
            print("\n🤖 Final Answer:")
            print(response["messages"][-1].content)
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        print()


def test_individual_workflow_steps():
    """
    Test each tool individually to verify behavior
    """
    print("=" * 80)
    print("Testing Individual Workflow Steps")
    print("=" * 80)
    
    # Step 1: Judge Context
    print("\n📍 STEP 1: Judge Context Presence")
    print("-" * 80)
    
    test_inputs = [
        "What is machine learning?",
        "Machine learning is AI. How does it work?"
    ]
    
    for inp in test_inputs:
        result = judge_context_presence.invoke({"user_input": inp})
        print(f"Input: {inp}")
        print(f"Result: {result}\n")
    
    # Step 2: Web Search (when missing)
    print("\n📍 STEP 2: Web Search (when context missing)")
    print("-" * 80)
    result = web_search.invoke({"query": "attention mechanisms"})
    print(result[:200] + "...")
    
    # Step 3: Check Relevance (when provided)
    print("\n\n📍 STEP 3: Check Context Relevance")
    print("-" * 80)
    
    test_relevance = [
        {
            "context": "Attention mechanisms help models focus on relevant input parts.",
            "question": "How do attention mechanisms work?",
            "expected": "relevant"
        },
        {
            "context": "Python is a programming language.",
            "question": "What are attention mechanisms?",
            "expected": "not_relevant"
        }
    ]
    
    for test in test_relevance:
        result = check_context_relevance.invoke({
            "context": test["context"],
            "question": test["question"]
        })
        print(f"Context: {test['context']}")
        print(f"Question: {test['question']}")
        print(f"Result: {result}")
        print(f"Expected: {test['expected']}\n")
    
    # Step 4: Split Context
    print("\n📍 STEP 4: Split Context and Question")
    print("-" * 80)
    result = split_context.invoke({
        "user_input": "Transformers use attention. How do they work?"
    })
    print(result)


# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    # Test individual steps first
    test_individual_workflow_steps()
    
    print("\n\n")
    
    # Then test full workflow adherence
    demo_workflow_adherence()