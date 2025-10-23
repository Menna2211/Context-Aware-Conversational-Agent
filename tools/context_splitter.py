from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from model_config import get_openrouter_llm ,get_ollama_llm

@tool
def split_context(user_input: str) -> str:
    """
    Use this ONLY after confirming context is relevant (check_context_relevance returned 'relevant').
    Separates the background context from the actual question.
    Returns JSON: {"context": "...", "question": "..."}
    """
    
    llm = get_openrouter_llm()
    #llm = get_ollama_llm()
    
    with open("prompts/context_splitter_prompt.txt", "r", encoding="utf-8") as f:
        prompt_text = f.read()
    prompt = PromptTemplate.from_template(prompt_text)

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"input": user_input})
    
    return result.strip()