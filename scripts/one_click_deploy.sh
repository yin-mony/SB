#!/usr/bin/env bash
# 思辩乐园 — 开源部署一键脚本（Docker Compose）
# 适用：Ubuntu / Debian 等已安装 Docker 与 Docker Compose 插件的服务器
# 用法：在「克隆下来的仓库根目录」执行：  bash scripts/one_click_deploy.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v docker >/dev/null 2>&1; then
  echo "未检测到 docker。请先安装：https://docs.docker.com/engine/install/ubuntu/"
  exit 1
fi

if docker compose version >/dev/null 2>&1; then
  DC=(docker compose)
elif command -v docker-compose >/dev/null 2>&1; then
  DC=(docker-compose)
else
  echo "未检测到 docker compose。请安装 Docker Compose 插件。"
  exit 1
fi

ENV_FILE="${ROOT}/.env"
if [[ ! -f "${ENV_FILE}" ]]; then
  cp "${ROOT}/deploy/env.example" "${ENV_FILE}"
  echo "已生成 ${ENV_FILE}，请编辑后填入 DJANGO_SECRET_KEY、DJANGO_ALLOWED_HOSTS 等，再重新执行："
  echo "  bash scripts/one_click_deploy.sh"
  exit 0
fi

"${DC[@]}" -f "${ROOT}/deploy/docker-compose.yml" --env-file "${ENV_FILE}" up -d --build
"${DC[@]}" -f "${ROOT}/deploy/docker-compose.yml" --env-file "${ENV_FILE}" ps

echo ""
echo "部署完成。浏览器访问：http://<服务器IP或域名>:${HTTP_PORT:-80}"
echo "更新代码后重新部署：git pull && bash scripts/one_click_deploy.sh"
