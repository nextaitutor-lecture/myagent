# myagent

AI Agent 개발 실습을 위한 프로젝트입니다.

## 개발환경 설치

이 프로젝트는 **Python 3.12 + uv** 기반으로 구성합니다.

처음 개발환경을 구성하는 경우 아래 문서를 순서대로 따라 진행하세요.

👉 [개발환경 설치 가이드 (development_setup.md)](./development_setup.md)

설치 가이드에는 다음 내용이 포함되어 있습니다.

- Python 3.12 설치
- pip 확인 및 업데이트
- uv 설치
- 프로젝트 및 Python 3.12 가상환경 구성
- `python-dotenv` 설치
- `langchain-openai` 설치
- `.env` 및 `OPENAI_API_KEY` 설정
- VS Code / Jupyter용 `ipykernel` 설정

## 기본 실행

개발환경 구성이 끝난 후 프로젝트 루트에서 다음과 같이 실행합니다.

```powershell
uv run python main.py
```

> `.env` 파일의 API Key는 GitHub에 커밋하지 않습니다.
