from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()
# 임베딩 모델을 설정합니다.
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

# 1. 저장된 데이터베이스를 다시 불러옵니다. (생성이 아님!)
retrieved_vectorstore = Chroma(
    persist_directory="chroma_data",
    embedding_function=embedding_model # 8.4절에서 설정한 모델 사용
)

# 2. 로드가 성공했는지 검증합니다.
collection = retrieved_vectorstore.get()
# print(f"총 {len(collection['ids'])}개 문서 확인.")


# 3.1 필터 조건 설정합니다. (새롭게 추가된 부분)
ai_fliter = {
    'source_type': 'glossary',
}

# 3.2 '검색(Retriever)' 객체를 생성합니다.
retriever = retrieved_vectorstore.as_retriever(
    # search_kwargs={
    #     'filter': ai_fliter
    # },
)


# 4. 검색어를 사용하여 문서를 검색합니다.
query = "보험 약관 정리해 줘"
docs = retriever.invoke(query)

print(f"검색 결과 문서 수: {len(docs)}개")
for i in range(len(docs)):
    print(f"\n--- 문서 {i+1} ---")
    print(docs[i].page_content)


# 5. 검색 타입을 'mmr'로 변경하여 새로운 retriever를 생성합니다.
mmr_retriever = retrieved_vectorstore.as_retriever(
    search_type="mmr",
    # 후보군 10개 중 4개를 MMR 방식으로 선택
    search_kwargs={
        "k": 5, 
        "fetch_k": 30, 
        # 'filter': ai_fliter
    } 
)

# 6. MMR 검색 수행
mmr_query = "보험 약관 정리해 줘"
mmr_docs = mmr_retriever.invoke(mmr_query)

print(f"MMR 검색 결과 문서 수: {len(mmr_docs)}개")
for i in range(len(mmr_docs)):
    print(f"\n--- MMR 문서 {i+1} ---")
    print(mmr_docs[i].page_content)