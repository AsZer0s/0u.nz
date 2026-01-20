# Docker入门系列 (5) - Docker Swarm

2025-09-25
tags: Linux, 开发, Docker

---

在前几章中，我们已经掌握了 Docker 的基础命令、网络原理以及 Compose 的服务编排能力

本章将深入讲解 Docker Swarm —— Docker 官方提供的原生容器集群管理工具

Swarm 能够将多台主机组织成一个统一的集群，实现服务的高可用、自动调度与负载均衡

---

## 什么是 Docker Swarm

Docker Swarm 是 Docker 内置的集群管理与编排工具

它允许你将多个 Docker 主机组成一个集群，并在其中部署分布式服务

Swarm 提供了服务发现、负载均衡、滚动更新等功能，是构建生产级容器平台的重要组件

---

## Swarm 的核心概念

- **节点（Node）**：Swarm 集群中的主机，分为管理节点（Manager）和工作节点（Worker）
- **服务（Service）**：Swarm 中运行的容器任务集合，具备副本数、更新策略等配置
- **任务（Task）**：服务的具体运行实例，分配给某个节点执行
- **覆盖网络（Overlay Network）**：用于跨主机容器通信的虚拟网络

---

## 初始化 Swarm 集群

在一台主机上执行：

```bash
docker swarm init
```

输出中会包含加入集群的命令，例如：

```bash
docker swarm join --token <worker-token> <manager-ip>:2377
```

在其他主机上执行该命令即可加入集群

---

## 创建服务

```bash
docker service create --name web --replicas 3 -p 80:80 nginx
```

说明：

- `--name`：服务名称
- `--replicas`：副本数量
- `-p`：端口映射
- `nginx`：使用的镜像

查看服务状态：

```bash
docker service ls
docker service ps web
```

---

## 服务更新与滚动部署

更新服务镜像：

```bash
docker service update --image nginx:latest web
```

Swarm 会自动进行滚动更新，确保服务不中断

---

## 高可用与负载均衡

- Swarm 会自动将任务分配到不同节点，实现负载均衡
- 内置 DNS 服务用于容器间通信
- 可配置健康检查与失败自动恢复

---

## Compose 与 Swarm 集成

使用 `docker-compose.yml` 文件部署到 Swarm：

```bash
docker stack deploy -c docker-compose.yml mystack
```

查看部署状态：

```bash
docker stack services mystack
```

---

## Swarm 与 Kubernetes 对比

| 特性             | Docker Swarm         | Kubernetes             |
|------------------|----------------------|------------------------|
| 安装复杂度       | 简单                 | 较复杂                 |
| 内置支持         | Docker 原生支持      | 需额外安装             |
| 社区生态         | 较小                 | 活跃、成熟             |
| 功能扩展性       | 基础编排能力         | 丰富的插件与控制器     |

---

## 总结

Docker Swarm 提供了轻量级的容器编排能力，适合中小型项目或快速部署场景

它与 Docker Compose 配合使用，可以实现从开发到生产的无缝过渡

虽然 Kubernetes 更为强大，但 Swarm 依然是理解容器编排原理的理想起点
