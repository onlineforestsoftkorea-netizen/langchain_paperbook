from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from pydantic import BaseModel, Field
from langchain.tools import tool

load_dotenv()
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    persist_directory="chroma_data",
    embedding_function=embedding_model
)

class SearchInput(BaseModel):
    query: str = Field(description="검색할 질문이나 키워드")
    source_type: str = Field(
        default="all",
        description="검색 대상: 'glossary' (AI/파이썬), 'insurance' (펫보험), 'all' (전체)"
    )
    k: int = Field(default=3, description="반환할 결과 개수")


@tool(args_schema=SearchInput, description="RAG 지식베이스에서 관련 문서를 검색합니다.")
def search_docs(query, source_type="all", k=3):
    """RAG 지식베이스에서 관련 문서를 검색합니다.
    
    AI 용어, 파이썬 기초, 펫보험 정보를 검색할 수 있습니다.
    source_type 파라미터로 특정 카테고리만 검색 가능합니다.
    """
    
    # 필터 설정
    if source_type == "all":
        filter_dict = None
    else:
        filter_dict = {"source_type": source_type}
    
    # retriever객체 생성
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": filter_dict
        }
    )
    
    # 검색 실행
    results = retriever.invoke(query)
    
    if not results:
        return "검색 결과가 없습니다."
    return results



from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# LLM 설정
model = ChatOpenAI(model="gpt-5-nano", temperature=0)

tools = [
    search_docs        
]

system_prompt="""
    당신은 AI 기술, 파이썬 프로그래밍, 펫보험에 대해 정보를 제공하는 전문가입니다.

    사용자 질문에 답하기 전에:
    1. search_docs 도구를 사용하여 관련 정보를 찾으세요.
    2. 사용자 질문을 query 파라미터로 전달하세요.
    3. 적절한 source_type을 선택하세요:
    - "glossary": AI/파이썬 관련 질문
    - "insurance": 펫보험 관련 질문
    - "all": 확실하지 않을 때
    4. 찾은 문서의 정보가 부족하면, k 값을 늘려 더 많은 문서를 검색하세요.
    5. 찾은 정보를 기반으로 정확하고 친절하게 답변하세요.
    6. 불확실한 부분은 "문서에는 이 정보가 없습니다"라고 명시하세요.
    """

# RAG Agent 생성
rag_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)

query = "펫보험의 자기부담금은 어떻게 되나요?"
messages = [{
    "role": "user",
    "content": query
}]

print(f"사용자 질문: {query}")

for chunk in rag_agent.stream({
    "messages": messages
}, stream_mode="values"):
    
    latest_msg = chunk["messages"][-1]
    
    if latest_msg.__class__.__name__ == "AIMessage":
        if latest_msg.content:
            print(f"Agent 생각:\n{latest_msg.content[:150]}...\n")
        
        if latest_msg.tool_calls:
            for tc in latest_msg.tool_calls:
                print(f"도구 호출: {tc['name']}")
                print(f"   입력: {tc['args']}\n")
    
    elif latest_msg.__class__.__name__ == "ToolMessage":
        print(f"도구 결과:")
        print(f"   {latest_msg.content[:200]}...\n")

print("\n최종 응답:")
print(chunk["messages"][-1].content)
