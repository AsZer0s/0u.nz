# Docker入门系列 (7) - Docker 与 Kubernetes 集成

2025-09-27
tags: Linux, 开发, Docker

---

随着容器技术的发展，Kubernetes（简称 K8s）已成为容器编排的事实标准

本章将介绍如何将 Docker 与 Kubernetes 集成，理解两者的关系，并完成一个基础的容器部署示例

---

## 为什么选择 Kubernetes

虽然 Docker Swarm 提供了基本的容器编排能力，但 Kubernetes 拥有更强大的功能和更广泛的社区支持：

- 自动化部署与回滚
- 服务发现与负载均衡
- 弹性伸缩与资源调度
- 健康检查与自愈机制
- 丰富的生态系统与插件支持

---

## Docker 与 Kubernetes 的关系

- Docker 是容器运行时，负责构建和运行容器
- Kubernetes 是容器编排平台，负责调度和管理容器集群
- Kubernetes 可使用 Docker 作为底层运行时（也支持其他如 containerd）

---

## 环境准备

推荐使用以下方式快速体验 Kubernetes：

1. **Minikube**：本地单节点 Kubernetes 集群
2. **Kind**：基于 Docker 的 Kubernetes 集群
3. **K3s**：轻量级 Kubernetes，适合边缘设备

安装 Minikube 示例：

```bash
brew install minikube
minikube start
```

---

## 部署一个 Docker 镜像到 Kubernetes

1. 编写 Dockerfile 构建镜像：

```dockerfile
FROM nginx
COPY ./index.html /usr/share/nginx/html/index.html
```

2. 构建并推送镜像到镜像仓库：

```bash
docker build -t yourname/nginx-demo .
docker push yourname/nginx-demo
```

3. 编写 Kubernetes 部署文件 `deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-demo
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-demo
  template:
    metadata:
      labels:
        app: nginx-demo
    spec:
      containers:
      - name: nginx
        image: yourname/nginx-demo
        ports:
        - containerPort: 80
```

4. 创建服务 `service.yaml`：

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx-demo
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30080
```

5. 部署到 Kubernetes：

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

访问服务：

```bash
minikube service nginx-service
```

---

## 管理与监控

- 查看 Pod 状态：`kubectl get pods`
- 查看服务状态：`kubectl get svc`
- 查看日志：`kubectl logs <pod-name>`
- 使用 Dashboard 或 Prometheus 进行可视化监控

---

## 总结

Kubernetes 提供了比 Docker Swarm 更强大的容器编排能力，是构建现代微服务架构的首选平台

通过将 Docker 镜像部署到 Kubernetes，你可以实现真正的弹性伸缩、高可用与自动化运维
