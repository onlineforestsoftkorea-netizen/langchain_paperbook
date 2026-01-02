import os
import streamlit as st
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda


_api_key = st.secrets.get("OPENAI_API_KEY", "")
if _api_key:
    os.environ.setdefault("OPENAI_API_KEY", _api_key)
else:
    st.warning("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

st.subheader("💬 AI Chatbot")

# 1) 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}

SESSION_ID = "chapter6"

def get_memory(session_id):
    session_key = session_id or SESSION_ID
    chat_memories = st.session_state.chat_memory
    if session_key not in chat_memories:
        chat_memories[session_key] = InMemoryChatMessageHistory()
    return chat_memories[session_key]


# 2) 범용 답변용 구성요소 정의와 체인 생성
prompt = ChatPromptTemplate(
    [
        (
            "system",
            """
            너는 친근한 와인 조언가다.
            이전 메시지를 바탕으로 질문 의도를 파악하고, 단계적으로 설명하라.
            """,
        ),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

model = ChatOpenAI(model="gpt-5-nano")
output_parser = StrOutputParser()

chain = prompt | model | output_parser

general_chain = RunnableWithMessageHistory(
    chain,
    get_memory,
    input_messages_key="question",
    history_messages_key="history",
)

router_keywords = {
    "가격검색": ["가격", "price", "비용", "사려면", "구매"],
    "유튜브": ["유튜브", "youtube", "영상", "동영상"],
}

def classify_topic(question):
    for key, values in router_keywords.items():
        if any(keyword in question for keyword in values):
            return key
    return "기타"

def router_step(inputs):
    question = inputs["question"]
    topic = classify_topic(question)
    return {"question": question, "topic": topic}

router_chain = RunnableLambda(router_step)

def route(info):
    topic = info["topic"]
    if topic == "유튜브":
        return "유튜브 검색 기능은 향후 구현될 예정입니다."
    
    if topic == "가격검색":
        return "가격 검색 기능은 향후 구현될 예정입니다."
    
    return general_chain.invoke(
        {"question": info["question"]},
        config={"session_id": SESSION_ID},
    )


# 3) 최종 체인 구성
full_chain = (
    router_chain
    | RunnableLambda(route)
)

# 4) 사용자 입력
prompt = st.chat_input("무엇을 도와드릴까요?")

# 5) 들어온 값 저장
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})   
    with st.spinner("AI가 응답을 생성하는 중입니다..."):
        response = full_chain.invoke({"question": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

# 6) 출력
for message in st.session_state.messages:
    speaker = "user" if message["role"] == "user" else "assistant"

    with st.chat_message(speaker):
        st.markdown(message["content"])