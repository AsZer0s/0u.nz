# Docker入门系列 (9) - 容器数据卷与持久化存储

2025-09-29
tags: Linux, 开发, Docker

---

容器是临时的，但数据不是

本章将深入讲解 Docker 的数据管理机制，重点介绍 Volume（数据卷）的使用方式、挂载策略与最佳实践，帮助你实现容器间的数据共享与持久化存储

---

## 为什么需要数据卷

默认情况下，容器中的数据会随着容器销毁而丢失

为了解决数据持久化与共享问题，Docker 提供了三种挂载方式：

- **Volume**：由 Docker 管理的挂载点，推荐使用
- **Bind Mount**：将宿主机目录挂载到容器中，灵活但不隔离
- **tmpfs**：将数据存储在内存中，适用于敏感或临时数据

---

## 使用 Volume 的基本方式

创建数据卷：

```bash
docker volume create mydata
```

查看卷列表：

```bash
docker volume ls
```

挂载卷到容器：

```bash
docker run -d -v mydata:/app/data nginx
```

容器中的 `/app/data` 目录将映射到 `mydata` 卷中

---

## Bind Mount 示例

将宿主机目录挂载到容器：

```bash
docker run -d -v /home/user/config:/etc/nginx nginx
```

适用于配置文件、日志文件等需要直接访问的场景

---

## tmpfs 示例

将数据存储在内存中：

```bash
docker run -d --tmpfs /app/cache nginx
```

适用于缓存、会话等不需要持久化的数据

---

## Volume 与 Compose 集成

在 `docker-compose.yml` 中定义卷：

```yaml
version: '3.8'
services:
  db:
    image: postgres
    volumes:
      - dbdata:/var/lib/postgresql/data

volumes:
  dbdata:
```

Compose 会自动创建并挂载 `dbdata` 卷，实现数据库持久化

---

## 查看与清理卷

查看卷详情：

```bash
docker volume inspect mydata
```

删除未使用的卷：

```bash
docker volume prune
```

删除指定卷：

```bash
docker volume rm mydata
```

---

## 最佳实践

- 使用 Volume 而非 Bind Mount 进行持久化，避免宿主机依赖
- 将数据卷与容器生命周期解耦，提升可维护性
- 定期备份数据卷内容，防止数据丢失
- 对敏感数据使用加密挂载或专用存储插件

---

## 总结

数据卷是容器化部署中不可或缺的一部分

通过合理使用 Volume、Bind Mount 与 tmpfs，你可以实现数据的持久化、共享与隔离
