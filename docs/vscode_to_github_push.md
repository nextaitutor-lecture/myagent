# VS Code 로컬 작업을 GitHub에 Commit / Push하기

VS Code에서 작성하거나 수정한 폴더와 파일을 GitHub 원격 저장소에 반영하는 방법입니다.

이 문서는 로컬 프로젝트가 이미 GitHub 저장소와 연결되어 있는 경우를 기준으로 합니다.

---

## 1. 변경사항 확인

VS Code 터미널에서 프로젝트 루트로 이동한 뒤 확인합니다.

```powershell
git status
```

수정된 파일의 예:

```text
On branch main
Changes not staged for commit:
        modified:   ver_0.1/step_01.ipynb
```

새로 만든 파일이나 폴더는 `Untracked files`로 표시될 수 있습니다.

---

## 2. 변경사항을 Stage에 추가

프로젝트의 변경사항을 모두 Commit 대상으로 추가합니다.

```powershell
git add .
```

다시 확인합니다.

```powershell
git status
```

정상 예:

```text
Changes to be committed:
        modified:   ver_0.1/step_01.ipynb
```

---

## 3. Commit

변경 내용을 로컬 Git 이력에 저장합니다.

```powershell
git commit -m "Update Agent v0.1 step 01"
```

Commit 메시지는 작업 내용을 알아보기 쉽게 작성합니다.

예:

```powershell
git commit -m "Add Agent v0.2 example"
git commit -m "Update README"
git commit -m "Fix transport search example"
```

---

## 4. GitHub에 Push

로컬 `main`이 이미 `origin/main`을 추적하고 있다면 다음 명령만 실행합니다.

```powershell
git push
```

정상적으로 완료되면 로컬 Commit이 GitHub에 반영됩니다.

---

## 5. `no upstream branch` 오류가 발생하는 경우

다음과 같은 오류가 발생할 수 있습니다.

```text
fatal: The current branch main has no upstream branch.
```

처음 한 번 다음 명령을 실행합니다.

```powershell
git push --set-upstream origin main
```

이 명령은 현재 로컬 `main`을 GitHub의 `origin/main`에 Push하면서 앞으로 추적할 원격 브랜치로 설정합니다.

정상 예:

```text
main -> main
branch 'main' set up to track 'origin/main'.
```

이 설정 이후에는 다시 `--set-upstream`을 사용할 필요 없이 다음 명령만 사용하면 됩니다.

```powershell
git push
```

---

## 평소 반복하는 작업

VS Code에서 코드를 작성한 뒤에는 기본적으로 다음 세 단계만 반복합니다.

```powershell
git add .
git commit -m "작업 내용"
git push
```

흐름으로 보면 다음과 같습니다.

```text
VS Code에서 파일 작성/수정
        ↓
git add .
        ↓
git commit
        ↓
git push
        ↓
GitHub origin/main 반영
```

## 반대 방향: GitHub → VS Code

GitHub에서 파일이 수정되거나 추가된 경우 로컬로 가져옵니다.

```powershell
git pull
```

따라서 기본적으로 다음 두 방향을 기억하면 됩니다.

```text
VS Code → GitHub
add → commit → push

GitHub → VS Code
pull
```
