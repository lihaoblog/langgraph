# 该文件为了增加参数，规范化工具，另一种写法Annotated
from typing import Annotated

from langchain_core.tools import tool
# BaseModel帮助你定义结构化的数据模型（类似于数据库表结构或数据类），并自动做类型校验和转换。
# BaseModel 是 Pydantic 提供的基类，用来定义“模型类（Model）
from pydantic import BaseModel, Field

#声明是个工具
@tool('calculate')
def calculate3(a: Annotated[float,'第一个参数'], b:  Annotated[float,'第二个参数'], operate: Annotated[str,'add，subtract，multiply，divide其中之一']) -> float:
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

# 下面是工具的信息，名字啥的
print(calculate3.name)
print(calculate3.description)
print(calculate3.args)
print(calculate3.return_direct)
# 参数定义结构
print(calculate3.args_schema.model_json_schema())

#invoke接受的是字典，或者Basemodel接受赋值
print(calculate3.invoke({'a':10,'b':20,'operate':'add'}))
# print(calculate3.invoke(a=10,b=20,operate='add'))