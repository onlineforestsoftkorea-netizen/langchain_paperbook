# app/pages/index_page.py
import streamlit as st

# 전체 요소를 가운데 정렬. 비율 1:10:1
_, main, _ = st.columns([1, 10, 1])

with main:
    # 이미지를 가운데 정렬. 비율 1:1:1
    _, image, _ = st.columns([1, 1, 1])
    with image:
        st.image("static/logo.svg", width=150)

    # 로고 아래 설명 문구 작성
    st.markdown(
        """
        ### 당신의 특별한 순간을 위한 와인을 찾아드립니다.
        - 와인을 처음 만나는 설렘도, 깊이 있는 여운도 여기에서 시작됩니다.
        """
    )
