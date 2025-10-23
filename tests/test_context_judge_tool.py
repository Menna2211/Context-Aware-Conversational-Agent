from tools import judge_context_presence

# Test the tool
user_message = "I'm building a web app with Flask and need to handle user authentication. What's the best way to implement login functionality?"

result1 = judge_context_presence.invoke({"user_input": user_message})
print(f"Result: {result1}")  # Should print "context_provided"
    

user_message2 = "What is Python?"
result2 = judge_context_presence.invoke({"user_input": user_message2})
print(f"Result: {result2}")  # Should print "context_missing"