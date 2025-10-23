from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from model_config import get_openrouter_llm ,get_ollama_llm
from tools import judge_context_presence, web_search ,split_context ,check_context_relevance

def build_context_aware_agent():
    """
    Builds a context-aware agent using modern LangChain create_agent.
    """
    
    # 1. Initialize the model (modern approach using init_chat_model)
    model = get_openrouter_llm()
    #model = get_ollama_llm()
    
    # 2. Gather all tools
    tools = [
        judge_context_presence,
        web_search,
        split_context,
        check_context_relevance
    ]
    
    # 3. Create system prompt
    with open("prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        system_prompt = f.read()


    # 4. Create the agent using modern create_agent
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt
    )
    
    return agent