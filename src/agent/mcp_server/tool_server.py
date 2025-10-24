from fastmcp import FastMCP
from fastmcp.prompts.prompt import PromptMessage,TextContent
from langchain_openai import ChatOpenAI


from agent.env_utils import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY

# 初始化、创建MCP客户端
server=FastMCP(name="lihao_mcp",instructions="李浩的代码实现MCP工具")
deepskAI=ChatOpenAI(
    model='deepseek-reasoner',
    temperature = 0.7,
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY,
)

@server.tool(name='deepseekAI')
def my_search(query:str)-> str:
    """搜索互联网的信息，如天气等"""
    try:
        print("执行我的python工具，输入参数为：",query)
        respond=deepskAI.wed_search.wed_search(
            search_engine='search_pro',
            search_query=query
        )
        print(respond)
        if respond.search_result:
            return "\n\n".join([d.content for d in respond.search_result])
        return "没有找到信息"
    except Exception as e:
        print(e)

@server.tool()
def say_hello(username:str)->str:
    return f'{username}666'

@server.prompt
def ask_about_topic(topic:str):
    """生成解释主题的消息模板"""
    return f'解释一下{topic}这个概念'

# 高级提示模板：返回结构化消息对象
@server.prompt
def generate_code_request(language:str,task_description:str)->PromptMessage:
    """生成代码编写请求的用户消息模板"""
    content=f'请用{language}写一个实现{task_description}功能的函数'
    return PromptMessage(
        role="user",
        content=TextContent(type='text',text=content)
    )

# 结构化资源：把序列转换成字典
@server.resource("resource:\\config")
def get_config()->dict:
    """以json形式返回应用配置"""
    return {
        "them":"dark",
        "version":"1.2.0",
        "features":["tool","resource"],  # 已启用的功能模块
    }