from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command


@tool
# 自动依赖注入id生成tool_call_id:Annotated[str,InjectedToolCallId]
def get_user_name(tool_call_id:Annotated[str,InjectedToolCallId] ,config:RunnableConfig) -> Command:  #command指令
    """获取用户所有信息"""
    user_name=config['configurable'].get('user_name','zs')

    print(f'调用工具，传入用户名是{user_name}')

    return Command(
        update={
            "username":user_name,
            "message":[
                ToolMessage(
                    content='得到当前用户名',
                    # 这个获取工具id，由上一个id得到
                    tool_call_id=tool_call_id
                )
            ]
        }
    )
