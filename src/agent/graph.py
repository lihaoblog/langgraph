from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState

from agent.tools.tool_demo2 import calculate2
from agent.tools.tool_demo5 import runnable_tool
from agent.tools.tool_demo7 import get_user_message

# 本地私有化部署的大模型
llm = ChatOpenAI(
    model='qwen3-8b',
    temperature=0.8,
    api_key='xx',
    base_url="http://localhost:6006/v1",
    extra_body={'chat_template_kwargs': {'enable_thinking': False}},
)

# def get_weather(city: str) -> str:
#     """Get weather for a given city."""
#     return f"It's always sunny in {city}!"

# configurable静态配置不支持修改
def prompt(state:AgentState,config:RunnableConfig)->list[AnyMessage]:
    user_name=config['configurable'].get('user_name','zs')
    print(user_name)
    system_message=f'当前用户{user_name},你是一个智能助手，尽可能回答问题'
    return [{'role':'system','content':system_message}] + state['messages']

graph = create_react_agent(
    llm,
    tools=[calculate2,runnable_tool,get_user_message],
    prompt=prompt
)
