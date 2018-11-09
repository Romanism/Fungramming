# 00. Branch의 원리 소개

- branch는 나무의 가지를 비유적으로 표현한 얘기입니다.
- 컴퓨터 공학에서는 식물에 대한 비유가 많이 등장해요! (root, branch ...)
- 파일을 수정해나간다고 가정해보겠습니다. (report1.hwp - report2.hwp - report3.hwp)
- 만약에 이 리포트를 client에게 제공하려고 한다면 내용을 일부 바꿔서 제공해야 할경우도 생기고 자체내에 있던 파일을 동시에 계속 수정해 나가야 할 경우가 생깁니다.
- 이럴때 client에 관한 branch를 만들어 쉽게 파일을 관리할 수 있습니다.
<br>

---

# 01. Branch 만들기
- **$ git branch** : git branch가 어떤것을 사용하고 있는지 확인합니다.
- **$ git branch <branch로 만들고싶은 이름>** : branch를 생성합니다.
- **$ git checkout <바꿀 branch 이름>** : branch를 변경합니다.
<br>

---

# 02. Branch 정보확인
- **$ git log --branches --decorate** : 모든 branch의 로그기록을 확인할 수 있습니다. 로그 기록을 보게 되면 옆에 (HEAD -> <branch이름>)이 나오는데 지금 사용하고 있는 branch를 의미합니다.
- **$ git log --branches --decorate --graph** : branch별 로그기록을 그래프 형태로 보여줍니다. (branch를 구분하는데 편합니다.)
- **$ git log branch1..branch2** : branch1과 branch2가 어떤 차이가 있었는지 보여줍니다. 순서가 상관 있습니다. branch1에는 없는데 branch2에 있는 로그기록을 보여줍니다.
<br>

---

# 03. Branch 병합

### branch1의 내용을 branch2에 병합하고 싶다면?

- **$ git checkout branch2** 를 통해 branch2로 이동합니다.
- **$ git merge branch1** 을 입력해 branch1의 내용을 branch2에 병합시킵니다.
- **$ git branch -d <만들었던 branch이름>** : branch를 삭제합니다.
<br>

---

# 04. Branch 수련

- [https://git-scm.com/book/ko/v2](https://git-scm.com/book/ko/v2)
- **git checkout -b <만들고 싶은 branch>** : -b를 붙이면 branch를 만들고 이 branch로 변경된다는 것을 의미합니다.
- Fast-forward 방식은  commit을 생성하지 않습니다.
<br>

---

# 05. Stash

### stash란?

- stash는 감추다, 숨기다라는 의미입니다.
- branch를 따서 작업을 하고 있는데 아직 작업이 끝나지 않았는데 다른 branch로 체크아웃해서 작업해야 할 경우가 생깁니다.
- 이럴때 아직 작업하던게 끝나지 않아 commit하기에 애매한 경우가 있습니다. 이럴때 stash를 씁니다. (잠깐 숨겨놓는다는 느낌..)


### stash 활용하기
- **$ git stash** 를 통해 해당 branch 데이터의 변경사항을 잠깐 숨겨놓습니다.
- **$ git stash apply** : 가장 최신 stash가 적요됩니다. 삭제는 하지 않습니다.
- **$ git stash list** : stash한 리스트를 보여줍니다.
- **$ git stash drop** : stash 리스트를 삭제합니다.
- **$ git stash pop** : stash가 apply되고 drop까지 됩니다.
