from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 1. 문서 로드
brief_loader = TextLoader("data/wine_brief.csv", encoding="utf-8")
brief_docs = brief_loader.load()

detail_loader = TextLoader("data/wine_detail.md", encoding="utf-8")
detail_docs = detail_loader.load()

# 2. 청킹
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=30
)

brief_chunks = text_splitter.split_documents(brief_docs)
detail_chunks = text_splitter.split_documents(detail_docs)

# 3. 메타데이터 추가
for chunk in brief_chunks:
    chunk.metadata["source_type"] = "Structured Data"
    chunk.metadata["category"] = "Wine Info"

for chunk in detail_chunks:
    chunk.metadata["source_type"] = "Unstructured Data"
    chunk.metadata["category"] = "Wine Description"

# 4. 벡터 스토어 생성
all_chunks = brief_chunks + detail_chunks
vector_store = Chroma.from_documents(
    documents=all_chunks,
    embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    persist_directory="./vector_store/wine_db"
)

print(f"brief 청크: {len(brief_chunks)}개")
print(f"detail 청크: {len(detail_chunks)}개")