from langchain_core.tools import tool

#工具前面要给的定义,初步定义
@tool('',return_direct=False)
def calculate1(a: float, b: float, operate: str) -> float:
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
print(calculate1.name)
print(calculate1.description)
print(calculate1.args)
print(calculate1.return_direct)
# 参数定义结构
print(calculate1.args_schema.model_json_schema())

