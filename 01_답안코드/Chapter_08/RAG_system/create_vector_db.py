
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from document_chunking import ai_chunks, insurance_chunks

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 임베딩 모델을 설정합니다. 
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")


# 1. 모든 청크를 하나의 리스트로 합칩니다.
# (8.2절에서 생성된 ai_chunks와 insurance_chunks를 사용합니다.)
all_chunks = ai_chunks + insurance_chunks

# 2. Chroma DB를 생성하고 영구적으로 저장할 경로를 지정합니다.
persist_directory = "chroma_data"

# 3. Chroma DB 생성 및 저장 (실행 시간이 다소 걸릴 수 있습니다.)
vectorstore = Chroma.from_documents(
    documents=all_chunks,
    embedding=embedding_model,
    persist_directory=persist_directory
)
