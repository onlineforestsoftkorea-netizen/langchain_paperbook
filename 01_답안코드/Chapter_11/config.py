# 오픈 AI 설정
MODEL_NAME = "gpt-5-nano"
TEMPERATURE = 0
SYSTEM_PROMPT = """
당신은 전문 와인 소믈리에입니다.

사용자의 와인 관련 질문에 다음과 같이 대응하세요:
1. 와인정보는 데이터베이스에서 찾습니다.
2. 필요하면 YouTube 영상 추천하기
3. 최종 추천 리스트는 마크다운 파일로 저장하기

항상 친절하고 전문적으로 답변하세요.
"""

# SQLite 설정
DB_PATH = "wine_chat.db"

# MCP 서버 설정
MCP_SERVERS = {
    "file_manager": {
        "transport": "stdio",
        "command": "python",
        "args": ["mcp_server/file_server.py"]
    },
    "wine_rag": {
        "transport": "stdio",
        "command": "python",
        "args": ["mcp_server/rag_server.py"]
    },
}