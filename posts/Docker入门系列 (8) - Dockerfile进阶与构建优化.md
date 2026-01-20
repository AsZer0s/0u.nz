# Docker入门系列 (8) - Dockerfile进阶与构建优化

2025-09-28
tags: Linux, 开发, Docker

---

Dockerfile 是构建镜像的核心脚本，它定义了容器的运行环境、依赖、启动方式等内容

本章将深入讲解 Dockerfile 的高级指令、构建优化技巧以及多阶段构建的实战应用，帮助你构建更高效、更安全的镜像

---

## Dockerfile 回顾

一个基础的 Dockerfile 示例：

```dockerfile
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]
```

---

## 常用指令详解

| 指令 | 说明 |
|------|------|
| `FROM` | 指定基础镜像 |
| `RUN` | 执行命令（如安装依赖） |
| `COPY` / `ADD` | 拷贝文件到镜像中 |
| `WORKDIR` | 设置工作目录 |
| `CMD` / `ENTRYPOINT` | 设置容器启动命令 |
| `ENV` | 设置环境变量 |
| `EXPOSE` | 声明端口（仅文档作用） |
| `VOLUME` | 声明挂载点 |
| `LABEL` | 添加元数据 |

---

## 构建优化技巧

### 减少镜像层数

将多个命令合并为一条：

```dockerfile
RUN apt-get update && apt-get install -y curl git
```

### 利用缓存机制

将不常变动的步骤放前面：

```dockerfile
COPY package.json .
RUN npm install
COPY . .
```

### 使用 `.dockerignore`

忽略无关文件，加快构建速度：

```
node_modules
.git
*.log
```

---

## 多阶段构建

用于构建与运行环境分离，减小镜像体积：

```dockerfile
# 构建阶段
FROM node:18 AS builder
WORKDIR /app
COPY . .
RUN npm install && npm run build

# 运行阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

优势：

- 构建依赖不会进入最终镜像
- 更安全、更轻量
- 适用于前端项目、Go、Rust 等编译型语言

---

## 安全性建议

- 使用官方或可信镜像源
- 避免使用 `latest` 标签，锁定版本
- 清理构建缓存与临时文件
- 最小化权限，避免使用 root 用户

---

## 实战演练：构建一个生产级 Node.js 镜像

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

构建并运行：

```bash
docker build -t mynodeapp .
docker run -d -p 3000:3000 mynodeapp
```

---

## 总结

Dockerfile 是连接开发与部署的桥梁

通过合理使用指令、优化构建流程、采用多阶段构建，便可以打造出高效、可维护的镜像结构
