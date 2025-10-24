# 用SSE方式调用工具
from agent.mcp_server.tool_server import server

if __name__=='__main__':
    # 调用方式
    server.run(
        # 通信方式指定三选一
        transport='sse',
        host='127.0.0.1',
        port=8000,
        log_level='debug',
    )

# 得到：http://127.0.0.1:8000/sse对外接口，别人就可用这个来使用该工具