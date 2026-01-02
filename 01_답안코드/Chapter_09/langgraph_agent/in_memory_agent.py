from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

load_dotenv()

model = ChatOpenAI(model="gpt-5-nano", temperature=0)

checkpointer = InMemorySaver()

agent = create_agent(model=model, checkpointer=checkpointer)

# 사용자 식별을 위한 thread_id 설정
user_id = "user_123"
config = {"configurable": {"thread_id": user_id}}

# 1. 첫 번째 대화: 이름 정보 제공
query1 = "내 이름은 철수야"
print(f"사용자: {query1}")

result = agent.invoke(
        {"messages": [{"role": "user", "content": query1}]}, 
        config
    )
print(f"Agent: {result['messages'][-1].content}")

# 2. 두 번째 대화: 기억력 테스트 (같은 thread_id 사용)
query2 = "내 이름이 뭐라고 했어?"
print(f"사용자: {query2}")

result = agent.invoke(
        {"messages": [{"role": "user", "content": query2}]}, 
        config
    )
print(f"Agent: {result['messages'][-1].content}")

# 3. 세 번째 대화: 다른 사용자로 설정 (다른 thread_id 사용)
new_user_id = "user_789"
new_config = {"configurable": {"thread_id": new_user_id}}

query3 = "내 이름이 뭐라고 했어?"
print(f"사용자: {query3}")

result = agent.invoke(
        {"messages": [{"role": "user", "content": query3}]},
        new_config
    )
print(f"Agent: {result['messages'][-1].content}")