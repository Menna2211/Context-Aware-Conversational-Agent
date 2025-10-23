import sys
import os
import json

from tools import split_context

# Just test one case
user_input = "Python is used for data science and machine learning. What libraries are available for ML?"

print("Testing Context Splitter...")
print(f"Input: {user_input}")

result = split_context.invoke({"user_input": user_input})
print("Output:")
print(result)