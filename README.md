# AI 厨神笔记

本项目当前默认运行环境为 `Ubuntu + uv`。

## 运行要求

- `uv`
- `Node.js`
- `npm`
- `ffmpeg`
- `redis-server` 或可用的 Redis 实例

## 首次启动

先确保 Redis 已启动：

```bash
sudo systemctl start redis-server
```

如果你的 Ubuntu 没有使用 `systemd`，也可以执行：

```bash
sudo service redis-server start
```

然后在项目根目录执行：

```bash
bash scripts/start.sh
```

或先赋予执行权限后直接运行：

```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

脚本会自动执行以下流程：

1. 检查 `uv`、`node`、`npm`、`ffmpeg`
2. 检查 Redis 是否运行在 `localhost:6379`
3. 检查 `.env`
4. 执行 `uv sync`
5. 安装前端依赖
6. 启动 TaskIQ Worker
7. 启动 FastAPI 后端
8. 启动 Vue 前端

## 服务地址

- 前端：`http://localhost:3000`
- 后端：`http://localhost:8000`
- API 文档：`http://localhost:8000/docs`

## 配置文件

项目根目录下的 `.env` 用于本地运行。
示例配置见 `.env.example`。

## Ubuntu 部署说明

- 当前仓库已移除 Windows 专用启动入口，统一使用 `scripts/start.sh`
- Python 依赖使用 `uv sync`
- 运行命令使用 `uv run`
- 生产环境建议把前端静态资源单独构建并由 Nginx 代理 FastAPI

## 新 Ubuntu 服务器需要安装的组件

一台全新的 Ubuntu 服务器，至少需要安装以下组件：

- `git`：拉取项目代码
- `curl`：安装 `uv` 时使用
- `ffmpeg`：视频转码与截图
- `redis-server`：TaskIQ 的 Redis Broker
- `nginx`：生产环境反向代理与静态文件服务
- `Node.js` 和 `npm`：构建前端
- `uv`：Python 依赖管理与运行
- `build-essential`、`pkg-config`：常见 Python 包编译依赖

推荐安装命令：

```bash
sudo apt update
sudo apt install -y git curl ffmpeg redis-server nginx nodejs npm build-essential pkg-config
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo ln -sf "$HOME/.local/bin/uv" /usr/local/bin/uv
```

安装完成后建议确认版本：

```bash
uv --version
node -v
npm -v
ffmpeg -version
redis-server --version
nginx -v
```

## Ubuntu 从零部署步骤

以下文档中的 `/home/user/cook-system` 只是示例路径，请按你的实际用户名和部署目录自行替换。

### 1. 拉取项目

```bash
git clone <your-repo-url> /home/user/cook-system
cd /home/user/cook-system
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

然后编辑 `.env`，至少确认这些字段：

- `DASHSCOPE_API_KEY`
- `REDIS_URL`
- `DATABASE_URL`
- `FFMPEG_PATH`

### 3. 安装 Python 依赖

```bash
uv sync
```

### 4. 构建前端

```bash
cd frontend
npm install
npm run build
cd ..
```

### 5. 启动 Redis

```bash
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### 6. 使用 systemd 托管后端和 Worker

仓库已提供模板文件：

- `deploy/systemd/cook-system-api.service`
- `deploy/systemd/cook-system-worker.service`

复制到系统目录：

```bash
sudo cp deploy/systemd/cook-system-api.service /etc/systemd/system/
sudo cp deploy/systemd/cook-system-worker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable cook-system-api
sudo systemctl enable cook-system-worker
sudo systemctl start cook-system-api
sudo systemctl start cook-system-worker
```

检查状态：

```bash
sudo systemctl status cook-system-api
sudo systemctl status cook-system-worker
```

### 7. 使用 Nginx 提供前端并代理 API

仓库已提供模板文件：

- `deploy/nginx/cook-system.conf`

复制配置：

```bash
sudo cp deploy/nginx/cook-system.conf /etc/nginx/sites-available/cook-system
sudo ln -s /etc/nginx/sites-available/cook-system /etc/nginx/sites-enabled/cook-system
sudo nginx -t
sudo systemctl reload nginx
```

## 生产部署结构建议

- 前端静态文件：`frontend/dist`
- 后端 API：`uv run uvicorn backend.main:app --host 127.0.0.1 --port 8000`
- TaskIQ Worker：`uv run taskiq worker backend.broker:broker backend.tasks`
- Redis：本机 `redis-server`
- Nginx：对外暴露 `80/443`，代理 `/api` 和 `/static`

## 部署模板说明

- `deploy/systemd/cook-system-api.service`
  负责托管 FastAPI API 进程
- `deploy/systemd/cook-system-worker.service`
  负责托管 TaskIQ Worker
- `deploy/nginx/cook-system.conf`
  负责对外提供前端静态资源，并把 `/api`、`/static` 转发到后端

## 注意事项

- 当前文档与模板默认示例路径为 `/home/user/cook-system`
- 当前 `systemd` 模板默认运行用户为 `www-data`
- 当前 `systemd` 模板默认 `uv` 路径为 `/usr/local/bin/uv`
- 如果你的部署路径或用户不同，请先修改模板中的 `WorkingDirectory`、`User`、`Group`
- 如果你的 `uv` 没有链接到 `/usr/local/bin/uv`，请同步修改 `ExecStart`
- 首次改完模板后，记得执行 `sudo systemctl daemon-reload`
- 前端每次更新后，需要重新执行 `npm run build`
