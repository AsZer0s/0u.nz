# Docker入门系列 (11) - Docker 与系统服务集成

2025-10-01
tags: Linux, 开发, Docker

---

在实际部署中，我们常常希望容器能够像系统服务一样运行：自动启动、守护运行、统一管理

本章将介绍如何将 Docker 容器与系统服务（如 systemd）集成，实现容器的后台运行、开机自启与日志管理

---

## 为什么要集成系统服务

虽然 Docker 本身支持后台运行（`-d` 参数），但在生产环境中，使用系统服务管理容器具有以下优势：

- 容器随系统启动自动运行
- 容器崩溃后自动重启
- 与其他服务统一管理（如 Nginx、PostgreSQL）
- 支持日志收集与权限控制

---

## 使用 systemd 管理容器

### 创建 systemd 服务文件

路径：`/etc/systemd/system/myapp.service`

```ini
[Unit]
Description=My Docker App
After=docker.service
Requires=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run --rm -p 8080:80 --name myapp yourname/myapp
ExecStop=/usr/bin/docker stop myapp

[Install]
WantedBy=multi-user.target
```

说明：

- `ExecStart`：容器启动命令
- `ExecStop`：容器停止命令
- `Restart=always`：容器异常退出后自动重启

---

### 启动与管理服务

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable myapp
sudo systemctl start myapp
```

查看状态：

```bash
sudo systemctl status myapp
```

停止服务：

```bash
sudo systemctl stop myapp
```

---

## 使用 Docker restart 策略

无需 systemd，也可通过 Docker 自带的重启策略实现守护运行：

```bash
docker run -d --restart=always yourname/myapp
```

可选策略：

- `no`：默认，不自动重启
- `on-failure`：仅在非 0 状态退出时重启
- `always`：始终重启
- `unless-stopped`：除非手动停止，否则始终重启

---

## 日志管理建议

- 使用 `docker logs` 查看容器日志
- 将日志输出重定向到文件或日志系统（如 journald、ELK）
- 在 systemd 中添加日志限制：

```ini
StandardOutput=journal
StandardError=journal
```

---

## 与 Supervisor 集成（可选）

除了 systemd，还可以使用 Supervisor 管理容器进程：

```ini
[program:myapp]
command=docker run --rm -p 8080:80 yourname/myapp
autostart=true
autorestart=true
stderr_logfile=/var/log/myapp.err.log
stdout_logfile=/var/log/myapp.out.log
```

---

## 总结

将 Docker 容器与系统服务集成，可以提升部署的稳定性与可维护性

无论是使用 systemd、Supervisor 还是 Docker 自带的重启策略，都能实现容器的自动运行与统一管
