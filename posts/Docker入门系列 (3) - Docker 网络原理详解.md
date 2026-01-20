# Docker入门系列 (3) - Docker 网络原理详解

2025-09-23
tags: Linux, 开发, Docker

---

容器之间如何通信？容器如何暴露服务给外部？Docker 网络是容器化部署中不可忽视的一环。本章将深入解析 Docker 的网络模型、常见网络类型及其应用场景，帮助你构建更稳定、可控的容器网络环境。

---

## 网络模型概览

Docker 提供了多种网络驱动，满足不同场景下的容器通信需求：

- **bridge**：默认网络，适用于单主机容器通信
- **host**：容器共享宿主机网络栈，性能高但隔离性弱
- **none**：容器无网络连接，适用于完全隔离场景
- **overlay**：跨主机容器通信，适用于 Swarm 集群
- **macvlan**：容器拥有独立 IP，适用于与物理网络集成

---

## bridge 网络详解

- Docker 默认创建一个名为 `bridge` 的虚拟网桥
- 所有未指定网络的容器都会连接到该网桥
- 容器之间可通过名称互相访问
- 可使用 `docker network inspect bridge` 查看网络详情

示例：

```bash
docker run -d --name web1 nginx
docker run -d --name web2 nginx
docker exec -it web1 ping web2
```

---

## host 网络模式

- 容器与宿主机共享网络栈
- 无需端口映射，直接使用宿主机端口
- 适用于高性能场景，如负载均衡器或代理服务

示例：

```bash
docker run --network host nginx
```

注意：仅适用于 Linux，Docker Desktop 的 host 网络行为不同。

---

## overlay 网络（Swarm 模式）

- 支持跨主机容器通信
- 需启用 Docker Swarm
- 自动实现服务发现与加密传输

创建步骤：

```bash
docker swarm init
docker network create -d overlay my_overlay
docker service create --name web --network my_overlay nginx
```

---

## 自定义网络与 DNS

- 使用 `docker network create` 创建隔离网络
- 容器自动注册 DNS 名称，支持名称解析
- 提升安全性与可维护性

示例：

```bash
docker network create my_net
docker run -d --name db --network my_net postgres
docker run -d --name app --network my_net myapp
```

在 `app` 容器中可通过 `db:5432` 访问数据库。

---

## 端口映射与访问控制

- 使用 `-p` 参数将容器端口映射到宿主机
- 宿主机可通过 `localhost:端口` 访问容器服务

示例：

```bash
docker run -d -p 8080:80 nginx
```

- 可结合防火墙或反向代理实现访问控制

---

## 总结

Docker 网络模型为容器提供了灵活的通信机制

掌握不同网络类型的原理与应用场景，不仅能提升服务稳定性，也能为后续的集群部署与安全策略打下坚实基础
