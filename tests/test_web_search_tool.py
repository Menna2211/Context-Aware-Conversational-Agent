from tools import web_search

user_message = "What is the latest Python version?"

result = web_search.invoke({"query": user_message})

print(result)