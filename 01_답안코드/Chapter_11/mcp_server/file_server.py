from mcp.server.fastmcp import FastMCP
from pathlib import Path

# FastMCP 서버 인스턴스 생성
mcp = FastMCP("file-server")    # 서버 이름 설정
BASE_DIR = Path("./output")     # 파일 저장 기본 디렉토리
BASE_DIR.mkdir(parents=True, exist_ok=True) # 디렉토리 생성 (없을 경우)

@mcp.tool('write_markdown', description="content의 키워드를 파일명으로 하여 지정된 경로에 내용을 마크다운 파일로 저장합니다.")
def write_markdown(path, content):
    """
    파일 제목은 내용의 키워드로 자동 생성하여 저장합니다. 
    (예: '와인_리뷰.md)
    
    Args:
        path: 저장할 파일의 경로. 단, 추가적인 디렉토리를 생성하지는 않습니다.
        content: 파일에 작성할 텍스트 내용
    """
    try:
        with open(BASE_DIR / path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to '{path}'"
    except Exception as e:
        return f"Error: 파일 저장 중 오류가 발생했습니다. {str(e)}"
    

if __name__ == "__main__":
    mcp.run(transport="stdio")
