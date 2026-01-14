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

# 2. 사용자 입력 받기
THREAD_ID = "Chapter11"
prompt = st.chat_input("와인에 대해 물어보세요...")
if prompt and agent:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    # (임시) 에이전트 답변 자리
    # 아직 에이전트가 없으므로 고정된 텍스트만 보여줍니다.
    # response = "아직 에이전트가 연결되지 않았습니다."

    with st.spinner("🤔 답변 생성 중..."):
        # 동일한 이벤트 루프 사용
        response = loop.run_until_complete(run_agent(agent, prompt, THREAD_ID))
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )

# 3. 이전 대화 내용 화면에 그리기
for message in st.session_state.messages:
    speaker = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(speaker):
        st.markdown(message["content"])