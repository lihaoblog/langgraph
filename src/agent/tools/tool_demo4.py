# 该文件为了增加参数，规范化工具，另一种写法
from typing import Annotated

from langchain_core.tools import tool, StructuredTool
# BaseModel帮助你定义结构化的数据模型（类似于数据库表结构或数据类），并自动做类型校验和转换。
# BaseModel 是 Pydantic 提供的基类，用来定义“模型类（Model）
from pydantic import BaseModel, Field






def calculate4(a: Annotated[float,'第一个参数'], b:  Annotated[float,'第二个参数'], operate: Annotated[str,'add，subtract，multiply，divide其中之一']) -> float:
    """用于数学运算的工具函数"""
    print(f"调用运算函数，第一个数{a}，第二个数{b},运算方式：{operate}")

    result = 0.0
    match operate:
        case "add":
            result=a + b
        case "subtract":
            result=a - b
        case "multiply":
            result=a * b
        case "divide":
            if b == 0:
                raise ValueError("0?error")
            else:
                result=a / b
    return result

async def calculate5(a: Annotated[float,'第一个参数'], b:  Annotated[float,'第二个参数'], operate: Annotated[str,'add，subtract，multiply，divide其中之一']) -> float:
    """用于数学运算的工具函数"""
    print(f"调用运算函数，第一个数{a}，第二个数{b},运算方式：{operate}")

    result = 0.0
    match operate:
        case "add":
            result=a + b
        case "subtract":
            result=a - b
        case "multiply":
            result=a * b
        case "divide":
            if b == 0:
                raise ValueError("0?error")
            else:
                result=a / b
    return result

#invoke接受的是字典，或者Basemodel接受赋值，创建的工具
calculater=StructuredTool.from_function(
    func=calculate4,
    name='calculater',
    descrption='用于数学运算的工具函数',
    return_direct=True,
    # 协程，异步经常用到,定义的异步执行，invoke执行同步，ainvoke执行异步。不需分的时候不加这参数
    coroutine=calculate5
)
