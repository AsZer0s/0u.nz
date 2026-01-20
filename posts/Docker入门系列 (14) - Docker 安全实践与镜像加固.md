# Docker入门系列 (14) - Docker 安全实践与镜像加固

2025-10-04
tags: Linux, 开发, Docker

---

容器技术虽然提升了部署效率，但也带来了新的安全挑战

本章将介绍 Docker 的安全实践，包括镜像加固、权限控制、漏洞扫描与网络隔离，帮助你构建更安全的容器运行环境

---

## 容器安全的核心问题

| 问题 | 风险 |
|------|------|
| 镜像来源不可信 | 恶意代码、后门 |
| 使用 root 用户运行 | 权限过高，易被攻击 |
| 镜像体积过大 | 增加攻击面与构建时间 |
| 网络暴露过多端口 | 易遭扫描与攻击 |
| 缺乏漏洞检测 | 隐藏安全隐患 |

---

## 镜像加固建议

### 使用可信镜像源

- 优先使用官方镜像或企业认证镜像
- 避免使用 `latest` 标签，锁定版本号

```bash
FROM nginx:1.25.2
```

### 镜像瘦身

- 使用轻量基础镜像，如 `alpine`

```dockerfile
FROM node:18-alpine
```

- 清理构建缓存与临时文件

```dockerfile
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
```

---

## 最小权限原则

### 避免使用 root 用户

```dockerfile
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
```

### 限制容器能力

```bash
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE ...
```

### 只读文件系统

```bash
docker run --read-only ...
```

---

## 网络隔离与访问控制

- 使用自定义网络，限制服务间通信
- 仅暴露必要端口，避免使用 `--network host`
- 配置防火墙与安全组（如 iptables、cloud firewall）

---

## 镜像漏洞扫描工具

| 工具 | 特点 |
|------|------|
| Trivy | 开源、快速、支持本地与 CI |
| Clair | 支持多种镜像仓库 |
| Snyk | 商业服务，支持依赖分析 |
| Docker Scout | Docker 官方集成工具（Docker Desktop） |

使用 Trivy 示例：

```bash
trivy image yourname/myapp
```

---

## Registry 安全建议

- 使用 HTTPS 加密传输
- 配置访问认证与权限控制
- 定期清理过期镜像与标签
- 启用镜像签名与审计日志

---

## 容器运行时安全

- 使用 AppArmor / SELinux 加强隔离
- 使用 seccomp 限制系统调用
- 使用 rootless Docker 降低权限风险

---

## 总结

安全不是附加项，而是容器部署的基础保障

通过镜像加固、权限控制、漏洞扫描与网络隔离，你可以构建一个更安全、更可靠的容器运行环境

下一章将作为本系列的收官篇，总结 Docker 项目实战经验与部署策略，帮助你从入门走向生产
