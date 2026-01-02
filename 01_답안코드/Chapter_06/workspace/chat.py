# chat.py
import streamlit as st

st.title('챗 요소 연습')

# 1) 세션 상태 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 2) 사용자 입력 받기
prompt = st.chat_input("무엇을 도와드릴까요?")

# 3) 데이터 저장
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": "저는 AI 입니다."})

# 4) 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    