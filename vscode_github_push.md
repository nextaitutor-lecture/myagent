# VS Code에서 GitHub에 Push하기

VS Code에서 로컬 프로젝트 `D:\nextaitutor\myagent`를 GitHub 저장소 `nextaitutor-lecture/myagent`와 연결하고 Push하는 방법입니다.

## 1. VS Code에서 프로젝트 폴더 열기

VS Code에서 다음 메뉴를 선택합니다.

```text
File → Open Folder
```

프로젝트 폴더를 선택합니다.

```text
D:\nextaitutor\myagent
```

VS Code 터미널을 열고 현재 위치를 확인합니다.

```powershell
pwd
```

`D:\nextaitutor\myagent`이면 됩니다.

---

## 2. Git 저장소 초기화

```powershell
git init
```

브랜치 이름을 `main`으로 맞춥니다.

```powershell
git branch -M main
```

---

## 3. GitHub 저장소 연결

GitHub 저장소:

https://github.com/nextaitutor-lecture/myagent

로컬 프로젝트에 원격 저장소를 연결합니다.

```powershell
git remote add origin https://github.com/nextaitutor-lecture/myagent.git
```

연결 상태를 확인합니다.

```powershell
git remote -v
```

---

## 4. GitHub의 기존 내용 가져오기

GitHub 저장소에는 이미 `README.md`, `development_setup.md` 등의 파일이 있으므로 처음 연결할 때는 원격 저장소의 내용을 먼저 가져옵니다.

```powershell
git pull origin main --allow-unrelated-histories
```

로컬 파일과 GitHub 파일의 내용이 서로 다르면 충돌(Conflict)이 발생할 수 있습니다. 이 경우 충돌 내용을 확인하고 필요한 내용을 선택한 뒤 Commit합니다.

---

## 5. `.env`가 Git에서 제외되는지 확인

`.env`에는 OpenAI API Key가 들어 있으므로 GitHub에 Push하면 안 됩니다.

`.gitignore`에 다음 내용이 있는지 확인합니다.

```gitignore
.env
.venv/
```

Git 상태를 확인합니다.

```powershell
git status
```

변경 파일 목록에 `.env`가 나타나지 않아야 합니다.

---

## 6. 변경 파일 추가

```powershell
git add .
```

추가된 파일을 확인합니다.

```powershell
git status
```

---

## 7. Commit

```powershell
git commit -m "Setup myagent development environment"
```

Commit 메시지는 실제 작업 내용에 맞게 변경하면 됩니다.

---

## 8. GitHub에 Push

처음 Push할 때는 다음과 같이 실행합니다.

```powershell
git push -u origin main
```

`-u origin main`을 지정하면 로컬 `main` 브랜치와 GitHub의 `main` 브랜치가 연결됩니다.

이후부터는 다음 명령만 사용해도 됩니다.

```powershell
git push
```

---

## 이후 코드 수정 후 반복하는 작업

처음 GitHub 연결을 완료한 이후에는 일반적으로 다음 3단계를 반복합니다.

```powershell
git add .
git commit -m "작업 내용"
git push
```

흐름으로 보면 다음과 같습니다.

```text
코드 수정
   ↓
git add .
   ↓
git commit
   ↓
git push
   ↓
GitHub 반영
```

VS Code의 **Source Control(소스 제어)** 화면을 이용하면 `git add`와 `git commit`을 UI에서 처리하고, 마지막에 **Sync Changes / Push**를 눌러 GitHub에 반영할 수도 있습니다.
