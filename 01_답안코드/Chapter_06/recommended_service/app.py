# app.py
import streamlit as st

st.title("와인 추천 서비스")

index_page = st.Page("app/pages/index_page.py", title="홈페이지", icon="🏠")
# 로그인 페이지 추가
login_page = st.Page("app/pages/login_page.py", title="로그인", icon="🔐")
chat_page = st.Page("app/pages/chat_page.py", title="AI 챗봇", icon="💬")

pg = st.navigation([index_page, login_page, chat_page])
pg.run()
