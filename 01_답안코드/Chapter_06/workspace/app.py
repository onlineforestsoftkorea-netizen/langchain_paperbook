# app.py
import streamlit as st

# 페이지 생성
main_page = st.Page("main.py", title="메인 페이지", icon="0️⃣")
widget_button = st.Page("widget_button.py", title="위젯 - 버튼", icon="1️⃣")
widget_input = st.Page("widget_input.py", title="위젯 - 입력", icon="2️⃣")
chat = st.Page("chat.py", title="챗 요소", icon="3️⃣") 


# 네비게이션 생성
pg = st.navigation([main_page, widget_button, widget_input, chat])
 
# Run
pg.run() 


