# main.py
import streamlit as st
import numpy as np
import pandas as pd

st.title('메인 페이지')
st.write("Hello world!")
st.markdown("Hello **world!**")
st.title("Streamlit x LangChain") 
st.header("기초 문법") 
st.subheader("Text element")
st.write("write를 활용한 데이터 출력")
 
chart_data = pd.DataFrame(
    np.random.randn(5, 3),
    columns=['a', 'b', 'c']
)

# st.write(chart_data)  기존 코드 주석 처리
st.line_chart(chart_data) # st.write(chart_data) 대신 line_chart 사용 

col1, col2, col3 = st.columns([1,1,1], vertical_alignment="bottom")
 
with col1:
	st.header("A cat")
	st.image("https://static.streamlit.io/examples/cat.jpg")
with col2:
	st.header("A dog")
	st.image("https://static.streamlit.io/examples/dog.jpg")
with col3:
	st.header("An owl")
	st.image("https://static.streamlit.io/examples/owl.jpg") 
