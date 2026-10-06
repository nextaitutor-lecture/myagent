# Git 로컬과 원격 저장소가 다를 때 동기화하기

VS Code의 로컬 Git 저장소와 GitHub 원격 저장소의 커밋 이력이 서로 달라졌을 때 확인하고 병합하는 방법입니다.

특히 **로컬에서 먼저 Commit한 상태에서 GitHub에서도 별도로 파일을 추가하거나 수정한 경우** 로컬 `main`과 원격 `origin/main`이 서로 다른 커밋을 가질 수 있습니다.

---

## 1. 현재 브랜치 확인

```powershell
git branch
```

정상 예:

```text
* main
```

현재 작업 브랜치가 `main`인지 먼저 확인합니다.

---

## 2. 원격 저장소 연결 확인

```powershell
git remote -v
```

정상 예:

```text
origin  https://github.com/nextaitutor-lecture/myagent.git (fetch)
origin  https://github.com/nextaitutor-lecture/myagent.git (push)
```

`origin`이 원하는 GitHub 저장소를 가리키는지 확인합니다.

---

## 3. GitHub의 최신 커밋 정보 가져오기

```powershell
git fetch origin
```

정상적으로 완료되면 아무 메시지가 출력되지 않을 수도 있습니다.

`fetch`는 GitHub의 최신 커밋 정보를 가져오지만, 아직 로컬 파일과 병합하지는 않습니다.

---

## 4. 로컬 작업 상태 확인

```powershell
git status
```

예:

```text
On branch main
nothing to commit, working tree clean
```

주의할 점은 `working tree clean`이 **로컬과 GitHub가 동일하다는 의미는 아니라는 것**입니다.

이 메시지는 단지 현재 로컬 작업 폴더에 Commit하지 않은 변경사항이 없다는 의미입니다.

---

## 5. 로컬 main과 원격 main의 커밋 차이 확인

```powershell
git log --oneline --left-right main...origin/main
```

예:

```text
> fe1ad2e (origin/main) Remote commit
> d154ba4 Another remote commit
< 19e5aa0 (HEAD -> main) Local commit
```

기호의 의미:

```text
<  로컬 main에만 있는 커밋
>  원격 origin/main에만 있는 커밋
```

양쪽 기호가 모두 나타난다면 로컬과 원격의 커밋 이력이 서로 갈라진 상태입니다.

```text
          ┌── Local Commit
공통 이력 ┤
          └── Remote Commit → Remote Commit
```

---

## 6. 로컬과 원격 이력 병합

로컬 작업과 GitHub의 변경사항을 모두 유지하려면 다음과 같이 병합합니다.

```powershell
git pull origin main --no-rebase --allow-unrelated-histories
```

옵션 의미:

- `--no-rebase`: rebase 대신 merge 방식으로 병합합니다.
- `--allow-unrelated-histories`: 서로 독립적으로 시작된 Git 이력도 병합할 수 있게 합니다.

`--allow-unrelated-histories`는 일반적인 pull마다 사용하는 옵션이 아니라, **로컬과 원격 저장소가 별도로 초기화되어 공통 이력이 없는 경우** 등에 사용합니다.

파일 내용이 서로 겹치지 않으면 Git이 자동으로 병합합니다.

---

## 7. 충돌이 발생한 경우

같은 파일의 같은 부분을 로컬과 GitHub에서 각각 수정했다면 Merge Conflict가 발생할 수 있습니다.

VS Code에서 충돌 파일을 열면 다음과 같은 선택지를 사용할 수 있습니다.

```text
Accept Current Change
Accept Incoming Change
Accept Both Changes
```

필요한 내용을 선택하고 파일을 저장한 뒤 다음과 같이 처리합니다.

```powershell
git add .
git commit -m "Resolve merge conflict"
```

---

## 8. 최종 상태 확인

```powershell
git status
```

정상 예:

```text
On branch main
nothing to commit, working tree clean
```

필요하면 파일 구조도 확인합니다.

```powershell
dir
```

GitHub에서 추가했던 파일이나 폴더가 로컬에도 생성되어 있는지 확인합니다.

---

## 9. 병합 결과를 GitHub에 Push

Merge 결과가 로컬에만 있는 경우 다음 명령으로 GitHub에도 반영합니다.

```powershell
git push
```

---

## 전체 확인 순서

문제가 발생했을 때는 다음 순서로 확인하면 됩니다.

```powershell
# 1. 현재 브랜치 확인
git branch

# 2. 원격 저장소 확인
git remote -v

# 3. 원격 최신 정보 가져오기
git fetch origin

# 4. 로컬 상태 확인
git status

# 5. 로컬/원격 커밋 차이 확인
git log --oneline --left-right main...origin/main

# 6. 필요한 경우 병합
git pull origin main --no-rebase --allow-unrelated-histories

# 7. 상태 확인
git status

# 8. 필요한 경우 GitHub 반영
git push
```

## 핵심 정리

```text
git status
    ↓
로컬에서 수정 중인 파일이 있는가?


git fetch origin
    ↓
GitHub의 최신 커밋 정보를 가져옴


git log --oneline --left-right main...origin/main
    ↓
로컬과 GitHub의 커밋 차이를 확인


git pull
    ↓
원격 변경사항을 로컬에 병합


git push
    ↓
로컬 변경사항을 GitHub에 반영
```

즉, **`git status`만 보고 로컬과 GitHub가 동일하다고 판단하지 않는 것**이 중요합니다. 로컬과 원격의 실제 차이는 `fetch` 후 `git log --left-right` 등으로 확인할 수 있습니다.
