# VS Code에서 GitHub에 Push하기

VS Code에서 로컬 프로젝트 `D:\nextaitutor\myagent`를 GitHub 저장소 `nextaitutor-lecture/myagent`와 연결하고 Push하는 방법입니다.

## 1. VS Code에서 프로젝트 폴더 열기

```text
File → Open Folder
```

```text
D:\nextaitutor\myagent
```

터미널에서 확인:

```powershell
pwd
```

---

## 2. Git 저장소 초기화

```powershell
git init
git branch -M main
```

---

## 3. GitHub 저장소 연결

```powershell
git remote add origin https://github.com/nextaitutor-lecture/myagent.git
git remote -v
```

---

## 4. GitHub의 기존 내용 가져오기

GitHub 저장소에 기존 파일이 있으므로 처음 연결할 때 원격 내용을 먼저 가져옵니다.

```powershell
git pull origin main --allow-unrelated-histories
```

충돌이 발생하면 VS Code에서 충돌 내용을 확인하고 필요한 내용을 선택한 뒤 Commit합니다.

---

## 5. `.env`가 Git에서 제외되는지 확인

`.gitignore`:

```gitignore
.env
.venv/
```

확인:

```powershell
git status
```

`.env`가 변경 파일 목록에 나타나지 않아야 합니다.

---

## 6. 변경 파일 추가

```powershell
git add .
git status
```

---

## 7. Commit

```powershell
git commit -m "Setup myagent development environment"
```

---

## 8. GitHub에 Push

처음 Push:

```powershell
git push -u origin main
```

이후:

```powershell
git push
```

---

## 이후 코드 수정 후 반복하는 작업

```powershell
git add .
git commit -m "작업 내용"
git push
```

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

VS Code의 **Source Control(소스 제어)** 화면에서도 Stage, Commit, Sync Changes / Push를 이용해 같은 작업을 수행할 수 있습니다.
