# 思辩乐园 — 开源部署说明（GitHub 托管代码 + 自建服务器）

本项目为**非商业、开源**用途：代码放在 **GitHub** 上公开；你在自己的云服务器（或家用主机）上运行服务即可，**不向 GitHub 支付部署费用**。

推荐方式：**Docker Compose 一键拉起**（同机 Nginx 反代前端 + API，SQLite 持久化，适合个人/小站）。

---

## 一、你需要准备什么

| 项目 | 说明 |
|------|------|
| 服务器 | 一台 **Linux x64**（如 Ubuntu 22.04），有公网 IP 或域名解析到该 IP |
| GitHub | 仓库已公开；在服务器上 `git clone` 你的仓库地址 |
| 域名（可选） | 没有域名也可用 `http://公网IP` 访问；上 HTTPS 时再配证书 |

---

## 二、服务器上安装 Docker（仅需一次）

以 **Ubuntu** 为例（其它发行版见 [Docker 官方文档](https://docs.docker.com/engine/install/)）：

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "${VERSION_CODENAME:-jammy}") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker "$USER"
```

执行完建议 **重新登录 SSH**，使当前用户加入 `docker` 组后无需每次 `sudo docker`。

---

## 三、一键部署（推荐流程）

在服务器上执行（将 `你的GitHub用户名/仓库名` 换成自己的）：

```bash
# 1. 拉代码（公开仓库无需 token）
git clone https://github.com/你的GitHub用户名/仓库名.git debate-paradise
cd debate-paradise

# 2. 生成环境变量文件并编辑（必填 DJANGO_SECRET_KEY、DJANGO_ALLOWED_HOSTS）
cp deploy/env.example .env
nano .env   # 或用 vim / VS Code Remote

# 3. 一键构建并后台启动
chmod +x scripts/one_click_deploy.sh
bash scripts/one_click_deploy.sh
```

说明：

- **第一次**运行脚本时，若还没有 `.env`，会从 `deploy/env.example` 复制一份并提示你先编辑；填好后再执行一次脚本即可完成构建与启动。
- 之后**更新版本**：在同一目录执行 `git pull`，再执行 `bash scripts/one_click_deploy.sh` 即可重新构建并滚动更新。

启动成功后，浏览器访问：`http://<服务器公网IP或域名>`（默认端口 **80**，可在 `.env` 里改 `HTTP_PORT`）。

---

## 四、`.env` 里必填项说明

| 变量 | 含义 |
|------|------|
| `DJANGO_SECRET_KEY` | 随机长串，勿泄露。生成示例：`openssl rand -hex 32` |
| `DJANGO_ALLOWED_HOSTS` | 逗号分隔，须包含你访问时用的 **域名或 IP**，如 `1.2.3.4,localhost` |
| `DJANGO_INSECURE_COOKIES` | 未上 HTTPS 前保持 `1`；配置好 HTTPS 后改为 `0`，并视情况设置 `DJANGO_SECURE_SSL_REDIRECT=1` |
| `VITE_API_BASE_URL` | **同域反代**（本方案默认）保持 `/api/v1/` 即可 |

数据库：Compose 内默认 **SQLite**，数据文件在 Docker 卷 `sqlite_data` 中；媒体上传在卷 `media_data` 中。

---

## 五、HTTPS（可选，建议有域名后做）

思路：在宿主机或另一容器用 **Caddy / Nginx + Let’s Encrypt** 做 443 终止，反代到本机 `HTTP_PORT`（默认 80）。启用 HTTPS 后：

1. 将 `.env` 中 `DJANGO_INSECURE_COOKIES` 改为 `0`；
2. 按需设置 `DJANGO_SECURE_SSL_REDIRECT=1`；
3. 保证反代传入 `X-Forwarded-Proto: https`（生产配置已支持 `SECURE_PROXY_SSL_HEADER`）。

具体 Caddy/Nginx 站点配置因域名而异，此处不展开；社区有大量「Docker 反代 + Let’s Encrypt」模板可参考。

---

## 六、与「仅 GitHub」的关系

- **GitHub**：保存与分发源代码（开源、无收费）。
- **你的服务器**：实际运行 Docker 容器、存储数据库与上传文件。
- 不在 GitHub 上存放 `.env`、`db.sqlite3`、`node_modules` 等（仓库根目录 `.gitignore` 已排除常见敏感与构建产物）。

---

## 七、手动 Compose（不用脚本时）

在仓库根目录：

```bash
cp deploy/env.example .env
# 编辑 .env 后：
docker compose -f deploy/docker-compose.yml --env-file .env up -d --build
docker compose -f deploy/docker-compose.yml --env-file .env ps
```

停止：

```bash
docker compose -f deploy/docker-compose.yml --env-file .env down
```

---

## 八、常见问题

1. **首次访问 502**  
   等待 `api` 容器内 `migrate` 与 Gunicorn 启动完成（约数十秒），再刷新。

2. **改端口**  
   在 `.env` 设置 `HTTP_PORT=8080`，重新执行一键脚本或 `docker compose ... up -d --build`。

3. **生产改用 MySQL**  
   在 `debate_paradise/config/settings/base.py` 中已有通过环境变量切换 MySQL 的逻辑；需自行改 `docker-compose.yml` 增加 `mysql` 服务并挂载，或改用裸机部署；超出本一键方案范围时可单独开 issue 讨论。

4. **管理员 / 数据种子**  
   使用 Django `createsuperuser`、项目内 `management/commands` 等，在 `api` 容器内执行，例如：  
   `docker compose -f deploy/docker-compose.yml --env-file .env exec api python manage.py createsuperuser`

---

维护愉快。若你改进了一键部署流程，欢迎通过 Pull Request 回馈仓库。
