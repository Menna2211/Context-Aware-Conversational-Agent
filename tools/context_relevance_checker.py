from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from model_config import get_openrouter_llm , get_ollama_llm

@tool
def check_context_relevance(context: str, question: str) -> str:
    """
    Checks if the provided context is relevant to the user's question.
    Returns 'relevant' or 'not_relevant' only
    """
    
    # Initialize model
    llm = get_openrouter_llm()
    
    # Create prompt template
    with open("prompts/context_relevance_prompt.txt", "r", encoding="utf-8") as f:
        prompt_text = f.read()
    prompt = PromptTemplate.from_template(prompt_text)

    # Create chain using LCEL
    chain = prompt | llm | StrOutputParser()

    # Execute
    result = chain.invoke({
        "context": context,
        "question": question
    })
    
    return result.strip()