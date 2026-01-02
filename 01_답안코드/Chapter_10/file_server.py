from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FileManager")


@mcp.tool('read_file', description="파일을 읽어 내용을 반환합니다.")
def read_file(path):
    """
    지정된 경로의 파일을 읽어 내용을 반환합니다.
    
    Args:
        path: 읽을 파일의 경로 (예: './data/report.txt')
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: '{path}' 파일을 찾을 수 없습니다."
    except Exception as e:
        return f"Error: 파일을 읽는 중 오류가 발생했습니다. {str(e)}"
    
@mcp.tool('write_file', description="지정된 경로에 내용을 파일로 저장합니다.")
def write_file(path, content):
    """
    지정된 경로에 내용을 파일로 저장합니다. 
    (이미 존재하는 파일이면 덮어씁니다.)
    
    Args:
        path: 저장할 파일의 경로
        content: 파일에 작성할 텍스트 내용
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to '{path}'"
    except Exception as e:
        return f"Error: 파일 저장 중 오류가 발생했습니다. {str(e)}"
    

if __name__ == "__main__":
    mcp.run(transport="stdio")