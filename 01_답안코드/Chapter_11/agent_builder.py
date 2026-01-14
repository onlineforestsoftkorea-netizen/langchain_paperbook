from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from config import MODEL_NAME, TEMPERATURE, SYSTEM_PROMPT, DB_PATH, MCP_SERVERS
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import aiosqlite
from langchain_community.tools import YouTubeSearchTool


async def create_wine_agent():
    conn = await aiosqlite.connect(DB_PATH)
    checkpointer = AsyncSqliteSaver(conn)

    model = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)
        
    # MCP 클라이언트 생성
    client = MultiServerMCPClient(MCP_SERVERS)
    
    # MCP 도구 가져오기
    mcp_tools = await client.get_tools()

    # 도구 설정
    # YouTubeSearchTool 추가
    youtube_tool = YouTubeSearchTool()
    all_tools = mcp_tools + [youtube_tool]

    # 에이전트 생성
    agent = create_agent(
        model=model,
        tools=all_tools,
        checkpointer=checkpointer,  # 체크포인터 추가
        system_prompt=SYSTEM_PROMPT
    )
    
    return agent

async def run_agent(agent, query, thread_id):
    config = {"configurable": {"thread_id": thread_id}}
    
    full_response = ""
    
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": query}]},
        config=config,
        stream_mode="values"
    ):
        if "messages" not in chunk:
            continue
        
        latest_msg = chunk["messages"][-1]
        print(latest_msg)
        
        if latest_msg.__class__.__name__ == "AIMessage":
            if latest_msg.content and latest_msg.response_metadata.get('finish_reason') != 'tool_calls':
                full_response = latest_msg.content
    
    return full_response