from tools import check_context_relevance

# Quick test
context = "Python is a programming language used for web development and data science."
question = "What can Python be used for?"

try:
    result = check_context_relevance.invoke({
        "context": context,
        "question": question
    })
    print("✅ Test successful!")
    print("Context:", context)
    print("Question:", question)
    print("Relevance Result:", result)
except Exception as e:
    print(f"❌ Test failed: {e}")