# AI Agent 개발환경 구성

Windows 환경에서 Python 3.12, uv, LangChain, Jupyter를 이용해 AI Agent 실습 개발환경을 구성합니다.

---

## 1. Python 3.12 설치

Windows PowerShell에서 `winget`을 이용해 Python 3.12를 설치합니다.

```powershell
winget install Python.Python.3.12
```

설치된 Python 버전과 경로를 확인합니다.

```powershell
py -0p
```

Python 3.12가 정상적으로 실행되는지 확인합니다.

```powershell
py -3.12 --version
```

---

## 2. pip 확인

```powershell
py -3.12 -m pip --version
```

필요한 경우 pip를 업데이트합니다.

```powershell
py -3.12 -m pip install --upgrade pip
```

---

## 3. uv 설치

```powershell
py -3.12 -m pip install uv
```

설치 확인:

```powershell
uv --version
```

---

## 4. 프로젝트 생성

```powershell
uv init myagent --python 3.12
cd myagent
```

---

## 5. Python 3.12 가상환경 생성

```powershell
uv venv --python 3.12
uv run python --version
```

`uv run`을 사용하면 `.venv`를 직접 활성화하지 않고도 프로젝트 가상환경에서 Python을 실행할 수 있습니다.

---

## 6. 필요한 패키지 설치

`.env` 사용:

```powershell
uv add python-dotenv
```

LangChain에서 OpenAI 모델 사용:

```powershell
uv add langchain-openai
```

---

## 7. .env 파일 생성

```powershell
New-Item .env
```

`.env` 파일:

```env
OPENAI_API_KEY=본인의_OpenAI_API_Key
```

API Key는 외부에 공개하거나 GitHub에 Commit하지 않습니다. `.gitignore`에 다음 내용이 포함되어 있는지 확인합니다.

```gitignore
.env
.venv/
```

---

## 8. Jupyter용 ipykernel 설치

```powershell
uv add --dev ipykernel
```

VS Code에서 `.ipynb` 파일을 열고 Kernel을 다음 가상환경으로 선택합니다.

```text
D:\nextaitutor\myagent\.venv\Scripts\python.exe
```

Jupyter에서 확인:

```python
import sys
print(sys.executable)
```

정상적으로 연결되었다면 프로젝트의 `.venv\Scripts\python.exe`가 출력됩니다.

---

## 설치 명령어 요약

```powershell
winget install Python.Python.3.12
py -0p
py -3.12 --version
py -3.12 -m pip --version
py -3.12 -m pip install --upgrade pip
py -3.12 -m pip install uv
uv init myagent --python 3.12
cd myagent
uv venv --python 3.12
uv run python --version
uv add python-dotenv
uv add langchain-openai
New-Item .env
uv add --dev ipykernel
```

여기까지 완료하면 **Python 3.12 + uv + 가상환경 + `.env` + LangChain/OpenAI + Jupyter** 기반의 Agent 개발환경 구성이 완료됩니다.
