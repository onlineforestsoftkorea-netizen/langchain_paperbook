import streamlit as st


# 페이지 정의
index_page = st.Page("pages/index_page.py", title="홈", icon="🏠")
chat_page = st.Page("pages/chat_page.py", title="와인 챗봇", icon="💬")

pg = st.navigation([index_page, chat_page])

pg.run()
