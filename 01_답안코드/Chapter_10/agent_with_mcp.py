import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import AIMessage, ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-5-nano", temperature=0)

async def main():
    """스트리밍 모드로 MCP 에이전트 실행"""
    # 1. MCP 클라이언트 생성: 서버 정보 등록
    client = MultiServerMCPClient({
        "file_manager": {
            "transport": "stdio",
            "command": "python",
            "args": ["file_server.py"]
        },
        "time_server": {
                        "transport": "stdio",
            "command": "python",
            "args": ["-m", "mcp_server_time", "--local-timezone=Asia/Seoul"]        
        }
    })

    # 2. 서버와 연결하고 도구 가져오기
    tools = await client.get_tools()
    
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="""
        당신은 유능한 파일 관리자입니다.
        사용자가 파일 생성에 대해 요청하면, 파일을 생성하고,
        파일 요약을 요청하면, 파일을 읽고 요약을 작성합니다.
        그리고 반드시 파일 생성시에는 작성 일자를 포함해야 합니다.
        """
    )

    query = "sample.txt를 읽고 summary.md에 요약을 저장해줄래?"
    
    print(f"사용자: {query}\n")
    
    # astream() 사용 (비동기 스트리밍)
    async for chunk in agent.astream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values"
    ):
        if "messages" not in chunk:
            continue
    
        latest_msg = chunk["messages"][-1]
        
        if latest_msg.__class__.__name__ == "AIMessage":
            # 도구 호출이 있으면 = 사고 과정 (Reasoning)
            if latest_msg.response_metadata.get('finish_reason') == 'tool_calls':
                # 도구 호출 중
                if latest_msg.tool_calls:
                    for tc in latest_msg.tool_calls:
                        print(f"[Reasoning] 도구 호출: {tc['name']}")
                        print(f"    [Acting] {tc['name']} {tc['args']}...\n")
            # 도구 호출이 없고 content가 있으면 = 최종 답변 (Finish)
            elif latest_msg.content:
                print(f"[Finish] {latest_msg.content[:150]}...\n")
        elif latest_msg.__class__.__name__ == "ToolMessage":
            print(f"[Observation] {latest_msg.content[:150]}...\n")

if __name__ == "__main__":
    asyncio.run(main())