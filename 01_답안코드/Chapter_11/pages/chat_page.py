import streamlit as st
from agent_builder import create_wine_agent, run_agent
from dotenv import load_dotenv
import asyncio

load_dotenv()

st.subheader("💬 와인 챗봇")

# 1. 대화 기록 저장소 만들기
# 새로고침해도 대화가 유지되도록 session_state를 사용합니다.
if "messages" not in st.session_state:
    st.session_state.messages = []
if "event_loop" not in st.session_state:
    st.session_state.event_loop = asyncio.new_event_loop()
if "agent" not in st.session_state:
    loop = st.session_state.event_loop
    st.session_state.agent = loop.run_until_complete(create_wine_agent())

agent = st.session_state.agent
loop = st.session_state.event_loop

# 2) 사용자 입력
THREAD_ID = "Chapter11"
prompt = st.chat_input("와인에 대해 물어보세요...")
# 입력 처리
if prompt and agent:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("🤔 답변 생성 중..."):
        # 동일한 이벤트 루프 사용
        response = loop.run_until_complete(run_agent(agent, prompt, THREAD_ID))
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

# 3) 메시지 출력
for message in st.session_state.messages:
    speaker = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(speaker):
        st.markdown(message["content"])