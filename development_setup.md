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

예:

```text
-V:3.12    C:\Users\alice\AppData\Local\Programs\Python\Python312\python.exe
```

Python 3.12가 정상적으로 실행되는지 확인합니다.

```powershell
py -3.12 --version
```

예:

```text
Python 3.12.12
```

---

## 2. pip 확인

Python 3.12에 설치된 `pip`를 확인합니다.

```powershell
py -3.12 -m pip --version
```

필요한 경우 pip를 최신 버전으로 업데이트합니다.

```powershell
py -3.12 -m pip install --upgrade pip
```

---

## 3. uv 설치

Python 3.12의 pip를 이용해 `uv`를 설치합니다.

```powershell
py -3.12 -m pip install uv
```

설치 확인:

```powershell
uv --version
```

`uv`는 이후 Python 가상환경과 프로젝트 패키지를 관리하는 데 사용합니다.

---

## 4. 프로젝트 생성

`myagent`라는 이름으로 새로운 프로젝트를 생성합니다.

```powershell
uv init myagent --python 3.12
```

생성된 프로젝트 폴더로 이동합니다.

```powershell
cd myagent
```

예:

```text
D:\nextaitutor\myagent
```

---

## 5. Python 3.12 가상환경 생성

프로젝트 폴더에서 Python 3.12 기반 가상환경을 생성합니다.

```powershell
uv venv --python 3.12
```

프로젝트 내부에 `.venv` 폴더가 생성됩니다.

```text
myagent/
├── .venv/
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
└── README.md
```

가상환경에서 사용하는 Python 버전을 확인합니다.

```powershell
uv run python --version
```

예:

```text
Python 3.12.12
```

> `uv run`을 사용하면 `.venv`를 직접 활성화하지 않고도 프로젝트의 가상환경에서 Python을 실행할 수 있습니다.

---

## 6. 필요한 패키지 설치

### 6.1 python-dotenv

`.env` 파일에 저장된 환경변수를 Python에서 사용하기 위해 설치합니다.

```powershell
uv add python-dotenv
```

### 6.2 langchain-openai

LangChain에서 OpenAI 모델을 사용하기 위해 설치합니다.

```powershell
uv add langchain-openai
```

설치된 패키지는 `pyproject.toml`에 프로젝트 의존성으로 등록되고, 정확한 버전 정보는 `uv.lock`에 관리됩니다.

---

## 7. .env 파일 생성

프로젝트 루트에 `.env` 파일을 생성합니다.

```powershell
New-Item .env
```

프로젝트 구조:

```text
myagent/
├── .env
├── .venv/
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── uv.lock
└── README.md
```

`.env` 파일에 OpenAI API Key를 설정합니다.

```env
OPENAI_API_KEY=본인의_OpenAI_API_Key
```

> API Key는 외부에 공개하거나 GitHub에 Commit하지 않습니다.

`.gitignore`에 `.env`가 포함되어 있는지도 확인합니다.

```gitignore
.env
```

---

## 8. Jupyter용 ipykernel 설치

VS Code의 Jupyter Notebook에서 프로젝트의 가상환경을 사용하기 위해 `ipykernel`을 설치합니다.

```powershell
uv add --dev ipykernel
```

VS Code에서 `.ipynb` 파일을 연 후 현재 표시된 Python 버전 또는 `Select Kernel`을 클릭합니다.

다음 순서로 선택합니다.

```text
Select Kernel
    ↓
Python Environments
    ↓
D:\nextaitutor\myagent\.venv\Scripts\python.exe
```

표시는 환경에 따라 다음과 같이 나타날 수 있습니다.

```text
Python 3.12.12 (.venv)
```

Jupyter Notebook에서 다음 코드를 실행하여 현재 사용 중인 Python 경로를 확인합니다.

```python
import sys

print(sys.executable)
```

정상적으로 연결되었다면:

```text
D:\nextaitutor\myagent\.venv\Scripts\python.exe
```

가 출력됩니다.

---

## 최종 개발환경

```text
Windows
  │
  └── Python 3.12
        │
        └── pip
              │
              └── uv
                   │
                   └── myagent
                        │
                        ├── .venv
                        │    └── Python 3.12
                        │
                        ├── python-dotenv
                        │    └── .env
                        │         └── OPENAI_API_KEY
                        │
                        ├── langchain-openai
                        │    └── ChatOpenAI
                        │
                        └── ipykernel
                             └── VS Code / Jupyter
```

## 설치 명령어 요약

```powershell
# Python 3.12 설치
winget install Python.Python.3.12

# Python 확인
py -0p
py -3.12 --version

# pip 확인
py -3.12 -m pip --version

# pip 업데이트
py -3.12 -m pip install --upgrade pip

# uv 설치
py -3.12 -m pip install uv

# 프로젝트 생성
uv init myagent --python 3.12
cd myagent

# 가상환경 생성
uv venv --python 3.12

# 가상환경 Python 확인
uv run python --version

# 패키지 설치
uv add python-dotenv
uv add langchain-openai

# .env 생성
New-Item .env

# Jupyter Kernel 설치
uv add --dev ipykernel
```

여기까지 완료하면 **Python 3.12 + uv + 가상환경 + `.env` + LangChain/OpenAI + Jupyter**까지 Agent 개발을 시작하기 위한 기본 환경 구성이 완료됩니다.
