from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. AI 용어 로드 (텍스트 파일)
ai_loader = TextLoader("data/Python_AI_Glossary_Guide.txt", encoding="utf-8")
ai_docs = ai_loader.load()

# 2. 펫보험 약관 로드 (PDF 파일)
insurance_loader = PyPDFLoader("data/meritz_pet_insurance.pdf")
insurance_docs = insurance_loader.load()

# print(f"AI 용어: {len(ai_docs)}개 문서 로드")
# print(f"메타데이터: {ai_docs[0].metadata}")
# print(f"내용: {ai_docs[0].page_content[:50]}...")
# print()
# print(f"펫보험 약관: {len(insurance_docs)}개 페이지 로드")
# print(f"메타데이터: {insurance_docs[0].metadata}")
# print(f"내용: {insurance_docs[0].page_content[:50]}...")

# 청킹 설정: 200자씩 자르고, 20자는 겹치게(overlap) 설정
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,     # 청크 크기
    chunk_overlap=20,   # 청크 겹침
)

# AI 용어 청킹
ai_chunks = text_splitter.split_documents(ai_docs)

# 펫보험 청킹
insurance_chunks = text_splitter.split_documents(insurance_docs)

# 청킹 결과 출력
# print(f"AI 용어 청킹: {len(ai_chunks)}개 청크로 분할")
# print(ai_chunks[0].page_content)
# print()
# print(f"펫보험 청킹: {len(insurance_chunks)}개 청크로 분할")
# print(insurance_chunks[0].page_content)

# 1. AI 용어 청크에 메타데이터 추가
for chunk in ai_chunks:
    chunk.metadata["source_type"] = "glossary"
    chunk.metadata["category"] = "AI & Python"

# 2. 펫보험 청크에 메타데이터 추가
for chunk in insurance_chunks:
    chunk.metadata["source_type"] = "insurance"
    chunk.metadata["category"] = "Pet Insurance"

# print(f"{ai_chunks[0].metadata}")