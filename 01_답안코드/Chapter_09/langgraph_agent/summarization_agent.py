from langgraph.checkpoint.sqlite import SqliteSaver 
from langchain_openai import ChatOpenAI
import sqlite3
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(model="gpt-4.1-mini", temperature=0)  

conn = sqlite3.connect("memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents import create_agent

# 1. 요약 미들웨어 설정
summarization_mw = SummarizationMiddleware(
    model=model,  
    trigger=[('tokens', 500)],
    keep=('messages', 5)
)

# 2. Agent 생성 (미들웨어 포함)
agent = create_agent(
    model=model,
    checkpointer=checkpointer,
    middleware=[summarization_mw]
)

# 3. 사용자 설정
user_id = "user_summary"
config = {"configurable": {"thread_id": user_id}}

# 연속 질문 리스트
queries = [
    "AI의 역사에 대해 간략히 설명해줘.",
    "머신러닝과 딥러닝의 차이점은 뭐야?",
    "트랜스포머 모델의 핵심 원리가 뭐지?",
    "BERT 모델은 어떻게 학습해?",
    "GPT 모델의 특징은 무엇이야?",
    "자연어 처리에서 주로 사용하는 데이터셋에는 어떤 것들이 있어?",
    "AI 윤리 문제에 대해 설명해줄 수 있어?",
    "미래의 AI 기술 발전 방향에 대해 어떻게 생각해?",
    "파이썬의 기초 문법에 대해서 알려줄래?",
    "웹 개발에서 프론트엔드와 백엔드의 차이는 뭐야?",
    "데이터베이스의 정규화란 무엇인가?",
    "클라우드 컴퓨팅의 장점은 뭐야?",
    "컨테이너화 기술에 대해 설명해줘.",
    "마이크로서비스 아키텍처의 특징은 뭐지?",
    "지금까지 우리가 무슨 이야기를 했는지 요약해줄래?"
]

# 4. 모든 질문에 대해서
for index, query in enumerate(queries, 1):
    print(f"\n[{index}] 사용자: {query}")
    
    for chunk in agent.stream(
        {"messages": [{"role": "user", "content": query}]}, 
        config, 
        stream_mode="values"
    ):
        # 각 chunk는 해당 시점의 전체 state를 포함
        messages = chunk["messages"]
        print(f"메시지 개수: {len(messages)}")
        
# 마지막 메시지 기준 요약 메시지 확인
for msg in messages:
    if "summary" in str(msg).lower():
        print(f"\n{msg.content}")


