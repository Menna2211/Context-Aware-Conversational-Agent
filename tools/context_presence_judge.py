from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from model_config import get_openrouter_llm ,get_ollama_llm

# Modern approach: Use @tool decorator
@tool
def judge_context_presence(user_input: str) -> str:
    """
    Determines if the user input includes background context or is just a direct question.
    Returns 'context_provided' or 'context_missing'.
    """
    with open("prompts/context_judge_prompt.txt", "r", encoding="utf-8") as f:
        prompt_text = f.read()
 
    # Create prompt template
    prompt = PromptTemplate.from_template(prompt_text)
    
    # Get LLM instance
    llm = get_openrouter_llm()
    #llm = get_ollama_llm()
    # Create chain using LCEL (LangChain Expression Language)
    
    chain = prompt | llm | StrOutputParser()
    
    # Execute and return result
    result = chain.invoke({"input": user_input})
    return result.strip()