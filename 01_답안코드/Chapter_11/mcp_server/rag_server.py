from mcp.server.fastmcp import FastMCP
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("wine-rag-server")

# 벡터스토어 초기화
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
vector_store = Chroma(
    persist_directory= "../vector_store/wine_db",
    embedding_function=embedding_model
)

@mcp.tool('search_wine', description="와인 정보를 벡터 검색으로 조회합니다. sourece_type: Structured Data, Unstructured Data, all 지원")
def search_wine(query: str, source_type: str, k: int = 3):
    """와인 RAG 검색 (Structured/Unstructured 데이터 지원)

    source_type 선택 가이드:
    • "Structured Data" → 와인 빈티지,지역,가격,재고량 (정형 데이터)
    • "Unstructured Data" → 리뷰, 맛, 테이스팅 노트 (텍스트 데이터)  
    • "all" → 전체 데이터 (가장 안전, 추천)

    사용 예시:
    • "샤토 마고 2020 가격" → source_type="Structured Data"
    • "피노 누아르 리뷰" → source_type="Unstructured Data"
    • "좋은 레드와인" → source_type="all"

    Args:
        query: 와인 이름, 품종, 키워드
        source_type: 위 3개 중 선택 (기본: "all")
        k: 결과 개수 (1-10)
    """

    # 필터 설정
    if source_type == "all":
        filter_dict = None
    else:
        filter_dict = {"source_type": source_type}
    
    # retriever 객체 생성
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": k,                  # 최종 4개
            "fetch_k": 15,           # 후보 15개
            "lambda_mult": 0.6,      # 유사도 60% + 다양성 40%
            "filter": filter_dict    # source_type 필터
        }
    )
    
    # 검색 실행
    results = retriever.invoke(query)
    if not results:
        return "검색 결과가 없습니다."
    return results

if __name__ == "__main__":
    mcp.run(transport="stdio")