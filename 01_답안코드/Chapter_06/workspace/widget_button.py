# widget_button.py
import streamlit as st

st.title("위젯 버튼 연습")

btn = st.button("버튼을 눌러보세요")
if btn:
    st.write("버튼이 눌렸습니다!")
else:
    st.write("아직 눌리기 전...")