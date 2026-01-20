# Docker入门系列 (4) - Docker Compose详解

2025-09-24
tags: Linux, 开发, Docker

---

在前几章中，我们已经了解了 Docker 的基本命令、镜像与容器管理以及网络原理。本章将深入讲解 Docker Compose —— 一个用于定义和运行多容器 Docker 应用的工具。通过 Compose，你可以用一份配置文件描述整个应用的服务栈，实现一键部署与管理

---

## 什么是 Docker Compose

Docker Compose 是一个用于定义和运行多容器应用的工具。它通过 `docker-compose.yml` 文件描述服务、网络、卷等配置，并通过简单命令完成构建、启动、停止等操作。

---

## Compose 的核心概念

- **服务（services）**：每个服务对应一个容器，可以指定镜像、命令、端口等
- **网络（networks）**：服务之间的通信依赖网络配置，默认自动创建
- **卷（volumes）**：用于持久化数据或共享文件
- **依赖（depends_on）**：定义服务之间的启动顺序

---

## 一个最小的 Compose 示例

```yaml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
```

启动服务：

```bash
docker-compose up -d
```

停止服务：

```bash
docker-compose down
```

---

## 多服务组合示例

以下是一个包含 Web、Redis 和 PostgreSQL 的服务栈：

```yaml
version: '3.8'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
    depends_on:
      - redis
      - db
    networks:
      - backend

  redis:
    image: redis
    networks:
      - backend

  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: example
    networks:
      - backend

networks:
  backend:
```

---

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `docker-compose up` | 构建并启动所有服务 |
| `docker-compose down` | 停止并移除所有服务 |
| `docker-compose ps` | 查看服务状态 |
| `docker-compose logs` | 查看服务日志 |
| `docker-compose exec` | 进入某个容器执行命令 |
| `docker-compose build` | 构建镜像（用于自定义 Dockerfile） |

---

## 使用 Compose 的优势

- **配置集中**：所有服务定义在一个文件中，便于管理
- **环境一致性**：开发、测试、生产环境配置一致
- **快速部署**：一条命令即可启动整个应用栈
- **易于扩展**：支持多个网络、卷、服务拓展

---

## 实战建议

- 将 `docker-compose.yml` 文件纳入版本控制
- 使用 `.env` 文件管理环境变量
- 配合 `Dockerfile` 构建自定义服务
- 在 CI/CD 流程中集成 Compose 实现自动化部署

---

## 总结

Docker Compose 是构建现代微服务架构的利器。它简化了多容器应用的部署流程，使得开发者可以专注于业务逻辑而非环境配置。掌握 Compose，将为后续学习 Docker Swarm 和 Kubernetes 打下坚实基础
