# myagent

AI Agent 개발 실습을 위한 프로젝트입니다.

## 문서

프로젝트 관련 가이드는 `docs` 폴더에서 관리합니다.

- [개발환경 설치 가이드](./docs/development_setup.md) — Python 3.12, uv, 가상환경, `.env`, LangChain/OpenAI, Jupyter 설정
- [VS Code에서 GitHub에 Push하기](./docs/vscode_github_push.md) — Git 초기화, 원격 저장소 연결, Commit 및 Push 방법

## 기본 실행

개발환경 구성이 끝난 후 프로젝트 루트에서 다음과 같이 실행합니다.

```powershell
uv run python main.py
```

> `.env` 파일의 API Key는 GitHub에 커밋하지 않습니다.
