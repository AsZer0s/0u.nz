# Docker入门系列 (10) - Docker Registry 镜像仓库管理

2025-09-30
tags: Linux, 开发, Docker

---

镜像是容器的基础，而镜像仓库则是容器生态的核心枢纽

本章将介绍 Docker Registry 的使用方式，包括官方仓库 Docker Hub、自建私有仓库，以及镜像的推送、拉取与版本管理，帮助你构建安全、高效的镜像分发体系

---

## 什么是 Docker Registry

Docker Registry 是用于存储和分发 Docker 镜像的服务。常见类型包括：

- **Docker Hub**：Docker 官方公共仓库，支持公开与私有镜像
- **Harbor**：企业级私有仓库，支持权限控制与镜像扫描
- **自建 Registry**：使用官方 `registry` 镜像快速部署本地仓库

---

## 镜像的命名规范

镜像名称格式：

```
[仓库地址]/[用户名或组织]/[镜像名]:[标签]
```

示例：

```
nginx:latest
yourname/myapp:v1.0
registry.example.com/backend/api:v2
```

---

## 登录与认证

登录 Docker Hub：

```bash
docker login
```

登录私有仓库：

```bash
docker login registry.example.com
```

退出登录：

```bash
docker logout
```

---

## 镜像推送与拉取

推送镜像到远程仓库：

```bash
docker tag myapp yourname/myapp:v1.0
docker push yourname/myapp:v1.0
```

拉取镜像：

```bash
docker pull yourname/myapp:v1.0
```

查看本地镜像：

```bash
docker images
```

---

## 自建私有 Registry

快速部署：

```bash
docker run -d -p 5000:5000 --name registry registry:2
```

推送镜像到本地仓库：

```bash
docker tag myapp localhost:5000/myapp
docker push localhost:5000/myapp
```

拉取镜像：

```bash
docker pull localhost:5000/myapp
```

---

## Harbor 简介

Harbor 是一个企业级镜像仓库，支持：

- 用户与角色权限管理
- 镜像签名与漏洞扫描
- LDAP/AD 集成
- Web UI 与 API 支持

部署方式：

- 使用 Helm 安装到 Kubernetes
- 使用 Docker Compose 本地部署

---

## 镜像版本管理建议

- 使用语义化版本号（如 `v1.0.0`）
- 避免使用 `latest` 标签部署生产环境
- 定期清理过期镜像，节省存储空间
- 使用标签策略区分环境（如 `dev`, `staging`, `prod`）

---

## 总结

镜像仓库是容器化部署的基础设施之一

通过合理使用 Docker Hub、自建 Registry 或 Harbor，你可以实现镜像的集中管理、安全分发与版本控制
