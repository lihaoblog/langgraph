from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from agent.tools.tool_demo3 import calculate3

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

graph = create_react_agent(
    llm,
    tools=[calculate3],
    prompt="You are a helpful assistant"
)
