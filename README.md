# langchain_paperbook

이 저장소는 도서/강의 자료 "AI 에이전트 마스터 클래스"의 실습 코드를 제공합니다.
LLM 호출을 넘어, 데이터·도구·비즈니스 로직을 연결하는 에이전트 시스템 설계를 다룹니다.

## 대상
- AI 에이전트 서비스를 설계/구현하려는 개발자
- AI 시스템의 구조와 데이터 흐름을 파악해야 하는 기술 리더

## 학습 범위(요약)
- 랭체인 1.0 기반 흐름(LCEL, Runnable, Memory)
- 에이전트 구현(도구 선택, 추론 흐름)
- RAG 기반 지식 검색
- LangGraph 체크포인터를 통한 상태 저장
- MCP 기반 외부 시스템 연동
- 예제 프로젝트(와인 추천 AI 에이전트)

## 폴더 구조
- 00_실습코드: 실습 자료
	- 챕터에 따라 노트북만 제공되거나, 데이터/requirements만 제공될 수 있습니다.
- 01_답안코드: 답안 자료(완성 코드)

## 실행 환경
이 책의 실습은 두 가지 환경을 기준으로 구성되어 있습니다.

- Google Colab: 노트북 기반 실습
- VS Code 로컬 환경: 프로젝트 단위 실습(폴더/파일 구성 포함)

## 설치(Windows)
1) 가상환경 생성

```bat
python -m venv .venv
```

2) 가상환경 활성화

- PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

- CMD

```bat
.\.venv\Scripts\activate.bat
```

3) 패키지 설치

실행하려는 챕터의 `requirements.txt`를 설치합니다.

```bat
pip install -r 00_실습코드\Chapter_08\requirements.txt
```

## API 키
일부 실습은 API 키가 필요합니다.

- 환경변수 `OPENAI_API_KEY`를 사용합니다.
- 키/토큰은 코드/노트북/설정 파일에 직접 기록하지 않습니다.

PowerShell 예시:

```powershell
$env:OPENAI_API_KEY = "여기에_키를_입력"
```

## 실행
- 노트북: 각 챕터의 `*.ipynb`를 실행합니다.
- 프로젝트 예제(답안): 각 챕터의 안내와 `requirements.txt`를 기준으로 실행합니다.

## 문의
코드 실행 문제나 정정 사항은 이 저장소의 GitHub Issue로 남겨주세요.
