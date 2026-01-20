# 让你的 Git Commit Message 优雅起来

2025-10-02
tags: Git, 编程, 杂谈, 开发

---

> “写代码一分钟，写 Commit Message 两行泪”  
> —— 一位被历史代码支配的程序员

## 为什么要在意 Commit Message ?

想象一下，你正调试一个项目，`git log` 滚动出来的全是这样的信息: 

```

fix bug
update
123
final_final_really_final

```

是不是感觉灵魂受到了暴击? 半年后的你，根本不知道自己当时修了啥 bug，更别提帮别人 review 代码了

Commit Message 就像项目的“日记”，写好它，团队能心有灵犀；写烂它，未来的自己会哭晕在厕所

---

## 一点规范，大大不同

业界其实早有共识，最常见的就是 **Conventional Commits 规范**

它给 Commit Message 设计了一套语法，简单又高效:

```

<type>(<scope>): <subject>

```

例如: 

```

feat(auth): 新增用户登录功能
fix(api): 修复分页接口返回条数错误
docs(readme): 更新使用文档示例

```

这样一眼扫过去，就能知道每个提交是 **新增功能、修 bug、写文档**，还是别的

---

## 常见的 type 类型

- **feat**：新功能
- **fix**：修 bug
- **docs**：文档修改
- **style**：代码格式 (空格、缩进、分号之类，不影响逻辑)
- **refactor**：代码重构 (既不是修 bug，也不是加功能)
- **test**：增加或修改测试
- **chore**：杂项，比如构建流程、依赖管理
- **perf**：性能优化
- **ci**：持续集成相关改动

---

## 为什么要这样？

- **可读性强**：几百个 commit 里，你能迅速找到关键信息
- **自动化友好**：很多工具能根据规范生成 **更新日志 (CHANGELOG)**，甚至触发自动发版
- **团队更和谐**：写清楚做了什么，review 更快，不用互相猜谜
- **利于新人上手**：新人看日志就能快速理解项目演进，不需要到处问

---

## 写得更优雅的小技巧

- **一句话说重点**：不要写“修复问题”，要写“修复分页接口返回数量错误”
- **不要带情绪**：什么“终于搞定了啊啊啊啊”——半年后看只会笑不出来
- **正文可以展开**：第一行简明扼要，必要时换行写详细说明
- **多用英文关键词，正文随意**：`type(scope)` 建议用英文，描述可以中英文结合

---

## 工具加持，让规范变习惯

- **Commitlint**  
  自动校验 commit 格式，不合格直接拦下

- **Husky**  
  Git hooks 工具，可以在 `git commit` 前强制执行校验，让团队所有人都守规范

- **Commitizen (cz-cli)**  
  交互式输入 commit message，手把手帮你填，完全不用担心格式

- **changelog 工具**  
  例如 [standard-version](https://github.com/conventional-changelog/standard-version)，可以根据 commit 自动生成更新日志

---

## 结语

程序员的世界里，代码会老去，Bug 会重生，但 commit log 会一直陪你
所以，下次提交的时候，别再敷衍了事，让你的 commit 规范起来吧

**毕竟：Commit 不规范，队友两行泪；Message 写得好，自己少烦恼。**
