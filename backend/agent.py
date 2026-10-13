from backend.tools.browser_tools import control_youtube
from backend.tools.mail_tools import send_email
from langchain_core.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage
from langchain_ollama import ChatOllama

TOOLS = [send_email, control_youtube]
TOOL_MAP = {tool.name : tool for tool in TOOLS}

SYSTEM_PROMPT = """You are EndoAgent, a local autonomous desktop assistant.
You have access to the following tools:
1. `send_email`: Send an email via Gmail SMTP. Draft clear, appropriate subjects and message bodies based on user instructions.
2. `control_youtube`: Control YouTube playback in the desktop browser (play, toggle_pause, forward, rewind, next, skip_ad).

Always select the best tool for the user's intent. When the tool finishes, summarize what happened cleanly.
"""

def get_agent_llm(model_name : str = "qwen2.5:7b"):
    """Initialize local ollama model and bind the tools schema."""
    llm = ChatOllama(model = model_name, temperature=0.2)
    return llm.bind_tools(TOOLS)

def run_agent(prompt : str, chat_history : list = None) -> str:
    """Execute a single conversational turn with tool-calling support."""
    llm_with_tools = get_agent_llm()

    message = [SystemMessage(content = SYSTEM_PROMPT)]

    if chat_history:
        message.extend(chat_history)

    message.append(HumanMessage(content= prompt)) 

    response : AIMessage = llm_with_tools.invoke(message)

    message.append(response)

    if response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id = tool_call["id"]

            print(f"\n[Tool Selected] : {tool_name}")
            print(f"[Arguments Generated] : {tool_args}")

            selected_tools = TOOL_MAP.get(tool_name)

            if selected_tools:
                tool_output = selected_tools.invoke(tool_args)
            else:
                tool_output = f"Error: Tool '{tool_name}' is not recognized."

            message.append(
                ToolMessage(content=str(tool_output), tool_call_id = tool_id)
            )    


        final_response : AIMessage = llm_with_tools.invoke(message)
        return final_response.content

    return response.content