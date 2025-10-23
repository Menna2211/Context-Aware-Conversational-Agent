"""
User-Friendly Gradio UI for Context-Aware Chatbot
Beautiful, intuitive, and easy to use
"""

import gradio as gr
from agents import build_context_aware_agent
from langchain_core.messages import HumanMessage
import time

# ============================================
# AGENT SETUP
# ============================================

agent = None

def get_agent():
    """Get or initialize the agent."""
    global agent
    if agent is None:
        agent = build_context_aware_agent()
    return agent


# ============================================
# CHAT FUNCTIONS
# ============================================

def chat(message, history):
    """Process chat message with typing animation."""
    if not message.strip():
        return history
    
    # Add user message immediately
    history.append((message, ""))
    
    try:
        # Get agent
        agent = get_agent()
        
        # Show thinking indicator
        history[-1] = (message, "🤔 Thinking...")
        yield history
        
        # Invoke the agent
        response = agent.invoke({
            "messages": [HumanMessage(content=message)]
        })
        
        # Extract answer
        answer = response["messages"][-1].content
        
        # Simulate typing effect
        history[-1] = (message, "")
        for i in range(0, len(answer), 3):
            history[-1] = (message, answer[:i+3])
            time.sleep(0.01)
            yield history
        
        # Final answer
        history[-1] = (message, answer)
        yield history
        
    except Exception as e:
        error_msg = f"😔 Oops! Something went wrong.\n\n**Error:** {str(e)}\n\nPlease try again or rephrase your question."
        history[-1] = (message, error_msg)
        yield history


# ============================================
# GRADIO UI
# ============================================

# Custom CSS for better styling
custom_css = """
.gradio-container {
    max-width: 900px !important;
    margin: auto !important;
}
.message-row {
    padding: 10px !important;
}
#chatbot {
    border-radius: 15px !important;
}
.message {
    font-size: 16px !important;
    line-height: 1.6 !important;
}
"""

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="AI Chatbot") as demo:
    
    # Header
    gr.Markdown(
        """
        # 🤖 Smart Context-Aware Chatbot
        
        Ask me anything! I'll automatically:
        - 🔍 Check if you provided context
        - 🌐 Search for information if needed
        - ✅ Verify context relevance
        - 💬 Give you a comprehensive answer
        """
    )
    
    # Chat interface
    chatbot = gr.Chatbot(
        height=450,
        label="💬 Conversation",
        show_label=False,
        avatar_images=(
            "https://api.dicebear.com/7.x/avataaars/svg?seed=User",
            "https://api.dicebear.com/7.x/bottts/svg?seed=Bot"
        ),
        bubble_full_width=False
    )
    
    # Input area
    with gr.Row():
        msg = gr.Textbox(
            label="",
            placeholder="💭 Ask me anything... (e.g., 'What is machine learning?')",
            lines=2,
            scale=9,
            show_label=False
        )
        submit = gr.Button("Send 🚀", variant="primary", scale=1, size="lg")
    
    # Action buttons
    with gr.Row():
        clear = gr.Button("🗑️ Clear Chat", size="sm")
        retry = gr.Button("🔄 Retry Last", size="sm")
    
    # Helpful tips section
    with gr.Accordion("💡 Tips & Examples", open=False):
        gr.Markdown(
            """
            ### How to get the best answers:
            
            **Without Context** (I'll search for you):
            - "What is machine learning?"
            - "Explain transformers in AI"
            - "How do neural networks work?"
            
            **With Context** (More precise answers):
            - "Attention mechanisms help models focus. How are they used in transformers?"
            - "LangChain is a framework for LLM apps. What are its main features?"
            - "Neural networks consist of layers. What does each layer do?"
            
            **Pro Tips:**
            - Be specific in your questions
            - Provide context when you have it
            - Ask follow-up questions for clarity
            """
        )
    
    # Quick examples
    gr.Examples(
        examples=[
            ["What is LangChain used for?"],
            ["The Eiffel Tower is one of the most famous landmarks in France. How tall is it?"],
            ["Bananas are yellow fruits. What is the capital of Japan?"],
            ["Who invented the telephone?"],
        ],
        inputs=msg,
        label="✨ Try these examples"
    )
    
    # Footer
    gr.Markdown(
        """
        ---
        <div style='text-align: center; color: #666; font-size: 14px;'>
        Made with ❤️ using LangChain • Powered by AI
        </div>
        """
    )
    
    # ============================================
    # EVENT HANDLERS
    # ============================================
    
    def clear_chat():
        """Clear the chat history."""
        return []
    
    def retry_last(history):
        """Retry the last message."""
        if len(history) > 0:
            last_message = history[-1][0]
            history = history[:-1]
            return history, last_message
        return history, ""
    
    # Submit handlers
    submit_event = submit.click(
        chat, 
        inputs=[msg, chatbot], 
        outputs=chatbot
    ).then(
        lambda: "", 
        None, 
        msg
    )
    
    msg_event = msg.submit(
        chat, 
        inputs=[msg, chatbot], 
        outputs=chatbot
    ).then(
        lambda: "", 
        None, 
        msg
    )
    
    # Clear button
    clear.click(clear_chat, outputs=chatbot)
    
    # Retry button
    retry.click(retry_last, inputs=chatbot, outputs=[chatbot, msg])


# ============================================
# LAUNCH
# ============================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 Starting Context-Aware Chatbot")
    print("=" * 60)
    print("\n📦 Loading agent...")
    
    try:
        # Pre-load agent
        get_agent()
        print("✅ Agent loaded successfully!")
    except Exception as e:
        print(f"⚠️  Warning: Could not pre-load agent: {e}")
        print("Agent will load on first message.")
    
    print("\n🌐 Starting web interface...")
    print("📱 Open in your browser: http://127.0.0.1:7860")
    print("\n💡 Tip: Press CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        share=False  # Set to True for public link
    )