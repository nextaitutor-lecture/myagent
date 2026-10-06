# GitHub 연결 계정 재설정하기

VS Code 또는 PowerShell에서 `git push`를 실행했을 때 다른 GitHub 계정으로 인증되어 권한 오류가 발생하는 경우 Git Credential Manager의 인증 정보를 삭제하고 올바른 계정으로 다시 로그인하는 방법입니다.

---

## 1. 대표적인 증상

Push할 때 다음과 같은 오류가 발생할 수 있습니다.

```text
remote: Permission to nextaitutor-lecture/myagent.git denied to developeralice8790.
fatal: unable to access 'https://github.com/nextaitutor-lecture/myagent.git/':
The requested URL returned error: 403
```

이 경우 Git 저장소 주소가 잘못된 것이 아니라, 현재 Git이 사용하는 GitHub 계정에 해당 저장소의 Push 권한이 없는 경우가 많습니다.

위 예에서는 `developeralice8790` 계정으로 인증되어 있지만 `nextaitutor-lecture/myagent` 저장소에 Push 권한이 없는 상태입니다.

---

## 2. 원격 저장소 주소 확인

먼저 연결된 GitHub 저장소가 맞는지 확인합니다.

```powershell
git remote -v
```

정상 예:

```text
origin  https://github.com/nextaitutor-lecture/myagent.git (fetch)
origin  https://github.com/nextaitutor-lecture/myagent.git (push)
```

원격 저장소 주소가 맞는데도 `403` 권한 오류가 발생한다면 인증 계정을 확인해야 합니다.

---

## 3. 기존 GitHub 인증 정보 삭제

Windows PowerShell에서 다음 명령을 실행합니다.

```powershell
"protocol=https`nhost=github.com`n" | git credential-manager erase
```

정상적으로 처리되어도 별도의 메시지가 출력되지 않을 수 있습니다.

이 명령은 Git Credential Manager에 저장된 `github.com` HTTPS 인증 정보를 제거합니다.

> GitHub 계정 자체를 삭제하거나 로그아웃시키는 작업이 아니라, 로컬 Git이 저장해 둔 GitHub 인증 정보를 제거하는 작업입니다.

---

## 4. 다시 Push하여 GitHub 재인증

현재 브랜치에 upstream이 아직 설정되지 않았다면 다음 명령을 실행합니다.

```powershell
git push --set-upstream origin main
```

이미 upstream이 설정되어 있다면 다음 명령으로도 충분합니다.

```powershell
git push
```

인증 정보가 삭제된 상태라면 다음과 같은 메시지가 나타날 수 있습니다.

```text
info: please complete authentication in your browser...
```

브라우저가 열리면 **해당 GitHub 저장소에 Push 권한이 있는 계정**으로 로그인하고 인증합니다.

---

## 5. 정상 Push 확인

정상적으로 Push되면 다음과 비슷한 결과가 출력됩니다.

```text
To https://github.com/nextaitutor-lecture/myagent.git
   9eaac7b..227386c  main -> main
branch 'main' set up to track 'origin/main'.
```

특히 다음 두 부분을 확인합니다.

```text
main -> main
branch 'main' set up to track 'origin/main'.
```

이제 로컬 `main`과 GitHub의 `origin/main`이 연결되어 이후에는 다음 명령만 사용하면 됩니다.

```powershell
git push
```

---

## 전체 해결 순서

```powershell
# 1. 원격 저장소 확인
git remote -v

# 2. 기존 GitHub HTTPS 인증 삭제
"protocol=https`nhost=github.com`n" | git credential-manager erase

# 3. 다시 Push하고 브라우저에서 올바른 계정으로 로그인
git push --set-upstream origin main
```

이미 upstream이 설정되어 있다면 3번은 다음과 같이 실행합니다.

```powershell
git push
```

## 핵심 정리

```text
Push 실행
   ↓
403 Permission denied
   ↓
오류 메시지에서 사용 중인 GitHub 계정 확인
   ↓
git remote -v 로 저장소 주소 확인
   ↓
Git Credential Manager의 github.com 인증 삭제
   ↓
다시 git push
   ↓
브라우저에서 권한 있는 GitHub 계정으로 인증
   ↓
Push 완료
```

`403 Permission denied`가 발생하면 무조건 소스나 Git 설정부터 수정하기보다 **현재 어떤 GitHub 계정으로 인증되어 있는지와 해당 계정의 저장소 권한을 먼저 확인하는 것**이 중요합니다.
