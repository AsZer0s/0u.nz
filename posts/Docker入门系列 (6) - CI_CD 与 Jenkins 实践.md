# Docker入门系列 (6) - CI/CD 与 Jenkins 实践

2025-09-26
tags: Linux, 开发, Docker

---

在现代软件开发流程中，持续集成（CI）与持续部署（CD）已成为 DevOps 的核心实践

本章将介绍如何使用 Jenkins 与 Docker 构建自动化流水线，实现从代码提交到容器部署的全流程自动化

---

## 什么是 CI/CD

- **持续集成（CI）**：开发者频繁地将代码集成到主分支，并自动进行构建与测试
- **持续部署（CD）**：将通过测试的代码自动部署到生产环境或测试环境

CI/CD 能显著提升开发效率、减少人为错误，并加快产品迭代速度

---

## Jenkins 简介

Jenkins 是一个开源的自动化服务器，支持构建、测试、部署等任务

它拥有丰富的插件生态，能够与 Docker、Git、Kubernetes 等工具无缝集成

---

## 环境准备

1. 安装 Docker
2. 使用 Docker 启动 Jenkins：

```bash
docker run -d \
  --name jenkins \
  -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

3. 访问 Jenkins：`http://localhost:8080`

首次启动会提示输入管理员密码，可通过容器日志获取：

```bash
docker logs jenkins
```

---

## 安装必要插件

在 Jenkins 插件管理中安装以下插件：

- Docker Pipeline
- Git
- Blue Ocean（可选，用于可视化流水线）
- Pipeline Utility Steps

---

## 创建流水线项目

1. 新建项目 → 选择“流水线”
2. 在配置中添加 `Pipeline Script`：

```groovy
pipeline {
    agent any

    stages {
        stage('拉取代码') {
            steps {
                git 'https://github.com/your/repo.git'
            }
        }

        stage('构建镜像') {
            steps {
                script {
                    docker.build('myapp')
                }
            }
        }

        stage('运行容器') {
            steps {
                sh 'docker run -d -p 8080:80 --name myapp myapp'
            }
        }
    }
}
```

---

## 添加凭据与环境变量

- 在 Jenkins 中添加 Git 凭据（如 SSH Key 或用户名密码）
- 使用 `withCredentials` 或 `.env` 文件管理敏感信息

---

## 实现自动触发

- 配置 Git Webhook，使每次提交自动触发构建
- 或使用 Jenkins 的定时触发器（如 `H/5 * * * *` 每 5 分钟执行一次）

---

## 构建通知与回滚机制

- 集成邮件、Slack、Webhook 等通知方式
- 使用标签或版本控制实现回滚部署

---

## 总结

通过 Jenkins 与 Docker 的结合，我们可以构建一个高效、稳定的自动化部署系统

CI/CD 不仅提升了开发效率，也增强了系统的可维护性与可靠性
