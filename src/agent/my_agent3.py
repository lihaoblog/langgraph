import asyncio

from fastmcp import FastMCP
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.jwt import RSAKeyPair
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from agent.env_utils import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY




llm=ChatOpenAI(
    model='deepseek-reasoner',
    temperature = 0.7,
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY,

)

# 生成RSA密钥
key_pair=RSAKeyPair.generate()
print(key_pair)
# 配置认证提供方
auth=BearerAuthProvider(
    public_key=key_pair.public_key,  #公钥用于校验签名
    issuer='www.lihao.com',  #什么域名都可以，签发方标识
    audience='my-dev-server'  #服务商标识
)

# 服务器模拟生成一个token
token=key_pair.create_token(
    subject='dev_user',
    issuer='www.lihao.com',
    audience='my-dev-server',
    scopes=['lihao','hello'],
    expires_in_seconds=3600
)
print(f'tocken：{token}')

server=FastMCP(
    name='lihao',
    instruction='laoli de daima shixian',
    auth=auth
)

# 配置
python_mcp_server_config={
    # 'url':'http://127.0.0.1:8000/stream',
    # 'transport':'streamable_http',
    'url':'http://127.0.0.1:8000/sse',
    'transport':'sse',
}

# w外网配置MCP客户端
out_mcp_server_config={
    'url':'http://127.0.0.1:8000/sse',
    'transport':'sse',
}

# python配置MCP客户端
mcp_client=MultiServerMCPClient(
    {
        'python_mcp':python_mcp_server_config
    }
)



async def create_agent():
    """必须异步创建客户端函数"""
    mcp_tools=await mcp_client.get_tools()  #不给值就是所有的工具都拿
    print(mcp_tools)
    prom= await mcp_client.get_prompt(
        server_name='python_mcp',
        prompt_name='ask_about_topic',
        arguments={'topic':'深度学习'}
    )
    print(prom)
    data= await mcp_client.get_resources(server_name='python_mcp',uris="resource:\\config")
    print(data)
    print(data[0].data)

    return create_react_agent(
        llm,
        tools=mcp_tools,
        prompt='你是一个智能助手，请尽量回答用户问题',
    )

agent=asyncio.run(create_agent())