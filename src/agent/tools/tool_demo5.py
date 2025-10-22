from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from agent.my_llm import llm

#提示词生成
prompt=(
    PromptTemplate.from_template('帮我生成一个简短的关于{topic}的报幕词')
    + '内容搞笑点'
    + '输出语言{language}'
)

chain=prompt | llm | StrOutputParser()

class ToolArgs(BaseModel):
    topic: str = Field(description='报幕词主题')
    language: str = Field(description='报幕词采用语言')


# 变成工具
runnable_tool= chain.as_tool(
    name='prompt_tool',
    description='这是一个专门生成报幕词的工具',
    # args_schema 是一个 参数定义模型，用于规范工具（Tool）的输入格式和参数类型
    args_schema=ToolArgs
)

print(runnable_tool.name)
print(runnable_tool.args_schema.model_json_schema)