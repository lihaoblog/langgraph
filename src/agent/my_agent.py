from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.prebuilt import create_react_agent
from langgraph.store.postgres import PostgresStore

from agent.env_utils import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY
from agent.tools.tool_demo2 import calculate2
from agent.tools.tool_demo5 import runnable_tool



llm=ChatOpenAI(
    model='deepseek-reasoner',
    temperature = 0.7,
    base_url=DEEPSEEK_BASE_URL,
    api_key=DEEPSEEK_API_KEY,

)
    #用内存来作为存储,没办法启动langgraph平台
    # checkpointer=InMemorySaver()
# 连接postgresql数据库
db_url="postgresql://postgres:201314lh@localhost:5432/langgraph_db"
with (
    PostgresSaver.from_conn_string(db_url) as checkpointer,
    PostgresStore.from_conn_string(db_url) as store
      ):
    # checkpointer.setup()  # 第一次用必须要加这个函数，重新建表
    store.setup()
    agent=create_react_agent(
        llm,
        tools=[calculate2,runnable_tool],
        prompt='你是一个智能助手，请尽量回答用户问题',
        checkpointer=checkpointer,
        store=store
    )

    config={
        "configurable":{
            "thread_id":"lihao"  #必须要这个会话id
        }
    }

    # invoke后面是字典格式
    resp1=agent.invoke(
        {"messages":[{"role":"user","content":"生成关于相声的报幕词,中文输出"}]},
            config,
    )

    resp2=agent.invoke(
        {"messages":[{"role":"user","content":"再给一个关于流行歌曲《无赖》的"}]},
            config,
    )
    #记得这字典输出格式
    print(resp1["messages"][-1].content)
    print(resp2["messages"][-1].content)

    # 取出数据库里面的短期存储
    rest=list(agent.get_state(config))
    print(rest)