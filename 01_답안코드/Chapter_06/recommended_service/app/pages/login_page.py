import streamlit as st

st.subheader("🔐 로그인")
user_id = st.text_input("Id", key="login_id")
password = st.text_input("Password", type="password", key="login_password")

st.button("로그인", key="login_button")
