# 为 Linux 服务器配置密钥登录与 VSCode 免密远程连接

2025-11-28
tags: Linux, 安全, 网络

---

如何在本地生成 SSH 密钥并将公钥添加到服务器，实现无密码（密钥）登录 Linux

## 生成密钥
使用工具 `ssh-keygen` 生成一对私钥与公钥

Windows 10/11 理论上已内置 OpenSSH 组件，可以直接使用此命令

没有的话也可以装一个 Git 然后用 Git Bash

或者在 系统设置 -> 应用 -> 可选功能 -> 添加可选功能 中安装 OpenSSH 客户端并重启

使用以下命令生成密钥
```bash
ssh-keygen -t rsa
```
> 想要实现免密登录需要将密码短语（passphrase）留空


执行完成后可以获得一个私钥文件 `id_rsa` 与一个公钥文件 `id_rsa.pub`

将私钥文件备份好，防止遗失或泄露，打开公钥文件，将其中的内容复制到剪切板

## 导入密钥
登录 Linux 服务器，打开 `/etc/ssh/sshd_config` 文件

取消 `PubkeyAuthentication` 的注释（删除 `#`，如不存在此项可以在文件末尾手动添加），并确保其值为 yes，可开启密钥登录
```bash
PubkeyAuthentication yes
```
（可选）将 `PasswordAuthentication` 的值改为 no（如不存在此项可以在文件末尾手动添加），可关闭密码登录

完成后保存文件

打开 `~/.ssh/authorized_keys` 文件（如不存在可手动创建该文件并设置权限为 600）

将之前复制的公钥内容粘贴到文件末尾（另起一行）

完成后保存文件

使用 `systemctl restart sshd` 命令重启 SSH 服务

## 测试远程连接
将私钥文件（`id_rsa`）放置于 `用户主目录/.ssh/` 文件夹中

> Linux 下用户主目录为 `~`
>
> Windows 下用户主目录为 `%homepath%`

打开 VSCode ，连接远程服务器，如未弹出密码登录窗口，则说明密钥登录配置成功
