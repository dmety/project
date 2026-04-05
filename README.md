# 基于大模型的个性化资源生成与学习多智能体系统

软件杯赛题项目，采用前后端分离架构。

## 技术栈

- **前端**: Vue3 + TypeScript + TailwindCSS + Vue Router + Pinia + Axios
- **后端**: Python 3.11 + FastAPI + SQLAlchemy + Pydantic
- **数据库**: MySQL 8.0 + Milvus + Redis
- **部署**: Docker + Docker Compose
- **AI服务**: 科大讯飞星火大模型 V4.0 + 讯飞多模态API + 讯飞内容审核API

## 项目结构

```
project/
├── .trae/                  # 系统配置目录
├── frontend/               # Vue3前端工程
├── backend/                # FastAPI后端工程
├── database/               # 数据库初始化脚本
├── deploy/                 # 部署配置
├── docs/                   # 赛事交付文档
├── .env.example            # 环境变量模板
└── README.md               # 项目说明文档
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.11+
- MySQL 8.0+
- Docker (可选)

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 后端启动

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 文件配置数据库和讯飞API
uvicorn app.main:app --reload
```

### Docker部署

```bash
cd deploy
docker-compose up -d
```

## 开发规范

- 所有代码必须加中文注释
- 接口必须有入参校验和异常处理
- 所有开源依赖必须标注来源与协议
- 严格按照「框架搭建→功能开发→智能体嵌入」的顺序执行

## 核心功能

1. 个性化学习路径规划
2. 智能学习资源生成
3. 多智能体学习助手

## 讯飞API使用

所有讯飞API调用已封装在 `backend/app/services/xfyun_sdk/` 目录下，支持环境变量配置。
